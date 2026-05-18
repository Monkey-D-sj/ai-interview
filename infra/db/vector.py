from abc import ABC, abstractmethod
from typing import Any


class VectorDB(ABC):
	"""
	Vector Database
	"""
	@abstractmethod
	def connect(self): ...

	@abstractmethod
	def insert(
		self,
		collection_name: str,
		document: str,
		embedding: list[float],
		metadata: dict | None = None,
	): ...

	@abstractmethod
	def query(
		self,
		collection_name: str,
		query_texts: list[str] | None,
		query_embeddings: list[list[float]] | None,
		top_k: int,
		where: dict | None,
	): ...

	@abstractmethod
	def delete(
		self,
		collection: str,
		ids: list[str] | None = None,
		where: dict | None = None
	): ...

	@abstractmethod
	def close(self): ...


class Chroma(VectorDB):
	def __init__(self, db_path: str = "./chroma_data"):
		self._client = None
		self.db_path = db_path
		self.connect()

	def connect(self):
		import chromadb
		if self._client:
			return
		self._client = chromadb.PersistentClient(path=self.db_path)

	def insert(
		self,
		collection_name: str,
		document: str,
		embedding: list[float],
		metadata: dict | None = None,
	):
		import uuid
		col = self._client.get_or_create_collection(name=collection_name)
		col.add(
			ids=[str(uuid.uuid4())],
			documents=[document],
			embeddings=[embedding],
			metadatas=[metadata] if metadata else None,
		)

	def query(
		self,
		collection_name: str,
		query_texts: list[str] | None = None,
		query_embeddings: list[list[float]] | None = None,
		top_k: int = 10,
		where: dict | None = None,
	):
		col = self._client.get_or_create_collection(name=collection_name)
		kwargs: dict[str, Any] = dict(n_results=top_k)
		if query_texts is not None:
			kwargs["query_texts"] = query_texts
		if query_embeddings is not None:
			kwargs["query_embeddings"] = query_embeddings
		if where is not None:
			kwargs["where"] = where
		return col.query(**kwargs)

	def delete(
		self,
		collection: str,
		ids: list[str] | None = None,
		where: dict | None = None
	):
		col = self._client.get_collection(name=collection)
		kwargs = {}
		if ids is not None:
			kwargs["ids"] = ids
		if where is not None:
			kwargs["where"] = where
		col.delete(**kwargs)

	def close(self):
		self._client = None
