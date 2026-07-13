from abc import ABC, abstractmethod
from pathlib import Path

from app.retrieve import rank_chunks_by_similarity
from app.storage import get_chunks_by_document, update_chunk_embedding

class VectorStore(ABC):
    """向量库边界：上层只依赖这个接口，不关心底层是SQLite还是Qdrants."""
    
    @abstractmethod
    def upsert_embedding(self, chunks: list[dict]) -> None:
        """保存chunk embedding; 如果chunk已经存在，则更新对应的embedding。"""
    
    @abstractmethod
    def search(
        self,
        document_id: str,
        query_embedding: list[float],
        top_k: int,
        ) -> list[dict]:
        """根据query emedding返回最相似的chunks"""
    

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
        )

        return rank_chunks_by_similarity(
            query_embedding=query_embedding,
            chunks=chunks,
            top_k=top_k,
        )
