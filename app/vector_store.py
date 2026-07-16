from abc import ABC, abstractmethod
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from app.retrieve import rank_chunks_by_similarity
from app.storage import get_chunks_by_document, update_chunk_embedding
from app.config import settings

class VectorStore(ABC):
    """
    VectorStore abstract boundary.

    Functions:
        store and retrieve relevant chunks with query embeddings, 
        and do not need to concern the details of the vector database.

    Main methods:
        upsert_embedding(chunks): save chunk embedding; if chunk already exist, update its embedding.
        search(document_id, query_embedding, top_k): search chunks by query embedding, retrieve the top_k chunks in document_id.
    
    RAG process position:
        When saving or updating chunk embedding, and when retrieving chunks by query embedding.
    """
    
    @abstractmethod
    def upsert_embedding(self, chunks: list[dict]) -> None:
        """
        chunks: list[dict], a list of chunks, each chunk is a dict with chunk_id and embedding
                [
                    {
                        "chunk_id": "123",
                        "embedding": [0.1, 0.2, 0.3],
                        ...
                    },
                ]
        return: None
                later calls update_chunk_embedding(), update embedding_json, finally save the embedding_json to embedding filed in database
        """
    
    @abstractmethod
    def search(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int,
        filters: dict | None = None,
    ) -> list[dict]:
        """
        document_id: str, 要查找的文档id
        query_embedding: list[float], 待查询向量
        top_k: int, 返回的相似度最高的k个chunk

        return: list[dict], 一个chunks，包含相似度最高的top_k个chunk
                [
                    {
                        "chunk_id": "123",
                        "embedding": [0.1, 0.2, 0.3],
                        ...
                    },
                ]
        """
    

class SQLiteVectorStore(VectorStore):
    """SQLite版本的向量库实现：先复用当前chunks表，不引入外部向量数据库"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
    
    def upsert_embedding(self, chunks: list[dict]) -> None:
        for chunk in chunks:
            embedding = chunk.get("embedding")
            if not isinstance(embedding, list):
                # 没有向量就不能写入向量库，抛出错误
                raise ValueError("chunk embedding is required")
            
            update_chunk_embedding(
                db_path=self.db_path, 
                chunk_id=chunk["chunk_id"], 
                embedding=embedding,
            )

    def search(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int,
        filters: dict | None = None,
        ) -> list[dict]:
        """
        document_id: str, 要查找的文档id
        query_embedding: list[float], 待查询向量
        top_k: int, 返回的相似度最高的k个chunk

        return: list[dict], 一个chunks，包含相似度最高的top_k个chunk
        """
        chunks = get_chunks_by_document(
            db_path=self.db_path,
            document_id=document_id,
            filters=filters,
        )
        
        return rank_chunks_by_similarity(
            query_embedding=query_embedding,
            chunks=chunks,
            top_k=top_k,
        )


class QdrantVectorStore(VectorStore):
    """Qdrant implementation for local vector storage and retrieval."""

    def __init__(self, url: str, collection_name: str):
        from qdrant_client import QdrantClient

        self.client = QdrantClient(url=url)
        self.collection_name = collection_name

    def _point_id(self, chunk_id: str) -> str:
        """Convert project chunk_id into a stable UUID string accepted by Qdrant."""
        return str(uuid5(NAMESPACE_URL, chunk_id))

    def _ensure_collection(self, vector_size: int) -> None:
        """Create the Qdrant collection lazily when the first embedding is written."""
        from qdrant_client import models

        if self.client.collection_exists(collection_name=self.collection_name):
            return

        self.client.create_collection( #创建Collection(向量表)
            collection_name=self.collection_name, #表名
            vectors_config=models.VectorParams(
                size=vector_size, #每条embedding的维度, BGE是512
                distance=models.Distance.COSINE, #相似度算法
            ),
        )

    def upsert_embedding(self, chunks: list[dict]) -> None:
        """
        Save chunk embeddings into Qdrant and keep retrievable chunk fields in payload.
        """
        from qdrant_client import models

        points = []
        for chunk in chunks:
            embedding = chunk.get("embedding")
            if not isinstance(embedding, list):
                raise ValueError("chunk embedding is required")

            self._ensure_collection(vector_size=len(embedding))

            payload = {
                "chunk_id": chunk["chunk_id"],
                "document_id": chunk["document_id"],
                "chunk_index": chunk["chunk_index"],
                "text": chunk["text"],
                "start_char": chunk["start_char"],
                "end_char": chunk["end_char"],
                "created_at": chunk["created_at"],
                "source": chunk.get("source"),
                "document_type": chunk.get("document_type"),
            }

            points.append(
                models.PointStruct( #Point = 一条向量记录s
                    id=self._point_id(chunk["chunk_id"]),
                    vector=embedding,
                    payload=payload,
                )
            )

        if not points:
            return

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int,
        filters: dict | None = None,
        ) -> list[dict]:
        """
        Search Qdrant by query embedding and restrict matches to one document_id.
        """
        from qdrant_client import models

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        if not self.client.collection_exists(collection_name=self.collection_name):
            return []

        must_conditions = [
            models.FieldCondition(
                key="document_id",
                match=models.MatchValue(value=document_id),
            )
        ]
        allowed_filters = {"source", "document_type"}
        for key in allowed_filters:
            value = filters.get(key) if filters else None
            if value:
                must_conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value),
                    )
                )

        result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=models.Filter(
                must=must_conditions
            ),
            limit=top_k,
            with_payload=True,
        )

        matches = []
        for point in result.points:
            payload = point.payload or {}
            match = dict(payload)
            match["score"] = point.score
            matches.append(match)

        return matches


def get_vector_store() -> VectorStore:
    """
    return: VectorStore, selected by settings.vector_store_provider.
            Default is SQLiteVectorStore for local development and CI.

    RAG process position:
        Used by upload and retrieve flows when they need to persist or search embeddings.
    """
    provider = settings.vector_store_provider.lower()

    if provider == "sqlite":
        return SQLiteVectorStore(db_path=settings.database_path)
    
    if provider == "qdrant":
        return QdrantVectorStore(
            url=settings.qdrant_url, 
            collection_name=settings.qdrant_collection,
        )
    
    raise ValueError(f"Unsupported vector store provider: {provider}")
