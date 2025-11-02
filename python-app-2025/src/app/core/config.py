"""
Central settings and environment loader.

This module exposes a single `settings` instance (typed) which reads values
from a `.env` file and the environment. It also normalises `BACKEND_CORS_ORIGINS`
so callers can always work with a List[str].

Usage:
	from app.core.config import settings
	print(settings.DATABASE_URL)
"""
from __future__ import annotations

import json
from typing import List, Any

from pydantic_settings import BaseSettings


def _parse_cors(value: Any) -> List[str]:
	"""Accept a JSON list, comma-separated string, or a Python list and return List[str]."""
	if not value:
		return []
	if isinstance(value, (list, tuple)):
		return [str(v) for v in value]
	s = str(value).strip()
	# Try JSON first
	try:
		parsed = json.loads(s)
		if isinstance(parsed, list):
			return [str(v) for v in parsed]
	except Exception:
		pass
	# Fallback: comma separated
	return [p.strip() for p in s.split(",") if p.strip()]


class Settings(BaseSettings):
	API_V1_PREFIX: str = "/api/v1"
	PROJECT_NAME: str = "Python App 2025"
	DEBUG: bool = True
	SECRET_KEY: str = "changeme"
	ALGORITHM: str = "HS256"
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
	DATABASE_URL: str = "sqlite:///./app.db"
	BACKEND_CORS_ORIGINS: List[str] = []

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"

	# pydantic will call this for values when creating the model; keep simple
	@classmethod
	def _parse_env_var(cls, name: str, value: Any) -> Any:
		if name == "BACKEND_CORS_ORIGINS":
			return _parse_cors(value)
		return value


# Create a single global settings instance used across the app
settings = Settings()

# Normalise BACKEND_CORS_ORIGINS if it came in as a raw string
try:
	settings.BACKEND_CORS_ORIGINS = _parse_cors(settings.BACKEND_CORS_ORIGINS)
except Exception:
	settings.BACKEND_CORS_ORIGINS = []

