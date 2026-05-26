from typing import TypedDict, Literal

Level = Literal["junior", "middle", "senior"]

class InterviewState(TypedDict):
	position: str
	level: Level
	tech_stack: list[str]
	