from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.openai import OpenAIEmbedding
from typing import List

from app.core.config import settings, ModelType
from app.schemas.freezer_data import ObjectDB, Manuals
from app.db.mysql import mysql_db
from app.utils.pdf_tools import process_pdf

class VectorDBService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.dims = 1536
        self.spec = ServerlessSpec(cloud="aws", region="us-east-1")
        self.embed_model = OpenAIEmbedding(
            model=ModelType.embedding,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.index = None
        self.vector_store = None
        self._initialize()

    def _initialize(self):
        existing_indexes = self.pc.list_indexes()
        
        if settings.PINECONE_INDEX_NAME not in [item["name"] for item in existing_indexes]:
            self.pc.create_index(
                name=settings.PINECONE_INDEX_NAME,
                dimension=self.dims,
                metric='cosine',
                spec=self.spec
            )
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
        self.vector_store = PineconeVectorStore(
            pinecone_index=self.index
        )
        self.pipeline = IngestionPipeline(
            transformations=[
                SemanticSplitterNodeParser(
                    buffer_size=1,
                    breakpoint_percentile_threshold=95, 
                    embed_model=self.embed_model,
                ),
                self.embed_model,
            ],
            vector_store=self.vector_store
        )

    def upsert_manual(self, manual: Manuals):
        object_ids = mysql_db.query(f"SELECT object_id FROM ObjectManual WHERE manual_id = {manual['id']}")
        metadata = {
            "manual_id": manual["id"],
            "object_ids": [str(id["object_id"]) for id in object_ids]
        }
        self.pipeline.run(documents=process_pdf(f"dataset/{manual['pdf_file_name']}.pdf", metadata))

    def query(self, query_text: str, top_k: int = 5) -> List[ObjectDB]:
        vector = self.embed_model.embed_documents([query_text])[0]
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
        return [ObjectDB(**match['metadata']) for match in results['matches']]

vector_db = VectorDBService()