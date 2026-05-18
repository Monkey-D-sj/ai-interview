from dataclasses import dataclass, field


@dataclass
class MemoryRecord:
	session_id: str
	content: str
	timestamp: int
	importance: float = 0.5
	meta_data: dict = field(default_factory=lambda: {})
