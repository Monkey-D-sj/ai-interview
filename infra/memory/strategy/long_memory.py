from typing import Callable

from infra.db import VectorDB
from infra.memory.strategy.base import MemoryRecord


class LongMemoryStrategy:
	def __init__(
		self,
		vector_db: VectorDB,
		collection_name: str,
		embedding_func: Callable[[str], list[float]],
		default_top_k: int = 10,
	):
		self._vector_db = vector_db
		self.collection_name = collection_name
		self.embedding_func = embedding_func
		self.default_top_k = default_top_k

	def add_memory(self, memory: MemoryRecord):
		self._vector_db.insert(
			self.collection_name,
			document=memory.content,
			embedding=self.embedding_func(memory.content),
			metadata={
				"session_id": memory.session_id,
				"timestamp": memory.timestamp,
				"importance": memory.importance,
			},
		)

	def query_memory(self, query_text: str, top_k: int | None = None) -> list[MemoryRecord]:
		query_embedding = self.embedding_func(query_text)
		results = self._vector_db.query(
			self.collection_name,
			query_texts=[query_text],
			query_embeddings=[query_embedding],
			top_k=top_k or self.default_top_k,
		)
		documents = (results.get("documents") or [[None]])[0]
		metadatas = (results.get("metadatas") or [[None]])[0]
		records = []
		for i, doc in enumerate(documents):
			if doc is None:
				continue
			meta = metadatas[i] if metadatas and i < len(metadatas) else {}
			records.append(MemoryRecord(
				session_id=meta.get("session_id", ""),
				content=doc,
				timestamp=meta.get("timestamp", 0),
				importance=meta.get("importance", 0.5),
			))
		return records
	
