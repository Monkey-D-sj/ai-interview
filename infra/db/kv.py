import json
from abc import ABC, abstractmethod
from typing import Any


class KVDB(ABC):
	"""
	Key-Value Database
	"""
	@abstractmethod
	def insert(self, table: str, key: str, value: Any): ...
	
	@abstractmethod
	def get(self, table: str, key: str): ...
	
	@abstractmethod
	def delete(self, table: str, key: str): ...
	
	@abstractmethod
	def close(self): ...
	
	@abstractmethod
	def connect(self, db_path: str): ...
	

class Sqlite(KVDB):
	def __init__(self):
		self._conn = None

	def connect(self, db_path: str):
		import sqlite3
		if self._conn:
			return
		self._conn = sqlite3.connect(db_path)
		self._conn.execute("PRAGMA journal_mode=WAL")

	def insert(self, table: str, key: str, value):
		self._conn.execute(
			f"CREATE TABLE IF NOT EXISTS [{table}] (key TEXT PRIMARY KEY, value TEXT)"
		)
		self._conn.execute(
			f"INSERT OR REPLACE INTO [{table}] (key, value) VALUES (?, ?)",
			(key, json.dumps(value, ensure_ascii=False)),
		)
		self._conn.commit()

	def get(self, table: str, key: str):
		cursor = self._conn.execute(
			f"SELECT value FROM [{table}] WHERE key = ?", (key,)
		)
		row = cursor.fetchone()
		if row is None:
			return None
		return json.loads(row[0])

	def delete(self, table: str, key: str):
		self._conn.execute(f"DELETE FROM [{table}] WHERE key = ?", (key,))
		self._conn.commit()

	def close(self):
		if self._conn:
			self._conn.close()
			self._conn = None
