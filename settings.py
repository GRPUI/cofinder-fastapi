from dataclasses import dataclass
from typing import List


@dataclass
class Settings:
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    cors_allowed_origins: List[str]
    cors_allowed_methods: List[str]
    cors_allowed_headers: List[str]
    redis_host: str
    redis_port: int
