"""ChromaDB-backed vector store for trading strategy concepts."""
import chromadb, hashlib
from sentence_transformers import SentenceTransformer
from loguru import logger

class KnowledgeGraph:
    def __init__(self, persist_path: str = './data/chroma_db'):
        self.client = chromadb.PersistentClient(path=persist_path)
        self.collection = self.client.get_or_create_collection('trading_concepts')
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info('KnowledgeGraph ready')

    def add_concept(self, concept: dict) -> str:
        text = f"{concept['concept']}: {concept['entry_condition']}"
        emb = self.embedder.encode(text).tolist()
        uid = hashlib.md5(text.encode()).hexdigest()
        self.collection.upsert(embeddings=[emb], metadatas=[concept], ids=[uid])
        return uid

    def query(self, query_text: str, style: str | None = None,
              n: int = 5) -> list[dict]:
        emb = self.embedder.encode(query_text).tolist()
        where = {'style': style} if style else None
        result = self.collection.query(
            query_embeddings=[emb], n_results=n, where=where)
        return result['metadatas'][0] if result['metadatas'] else []

    def ingest_paper(self, pdf_path: str) -> int:
        from knowledge.paper_parser import PaperParser
        concepts = PaperParser().extract_concepts(pdf_path)
        for c in concepts:
            self.add_concept(c)
        logger.success(f'Ingested {len(concepts)} concepts from {pdf_path}')
        return len(concepts)
