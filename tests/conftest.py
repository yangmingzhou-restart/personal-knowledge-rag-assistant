import pytest
from app.embeddings import reset_embedding_provider_cache

@pytest.fixture(autouse=True)
def reset_embedding_cache_between_tests():
    reset_embedding_provider_cache()
    yield
    reset_embedding_provider_cache()
