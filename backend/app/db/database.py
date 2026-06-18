from __future__ import annotations

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()


class Base(DeclarativeBase):
	pass


def _normalize_database_url(url: str) -> str:
	if url.startswith("postgres://"):
		return url.replace("postgres://", "postgresql+psycopg2://", 1)
	if url.startswith("postgresql://"):
		return url.replace("postgresql://", "postgresql+psycopg2://", 1)
	return url


def _get_database_url() -> str | None:
	raw_url = os.getenv("SUPABASE_DB_URL") or os.getenv("DATABASE_URL")
	if raw_url:
		return _normalize_database_url(raw_url)

	host = os.getenv("SUPABASE_DB_HOST")
	password = os.getenv("SUPABASE_DB_PASSWORD")
	if not host or not password:
		return None

	username = os.getenv("SUPABASE_DB_USER", "postgres")
	database_name = os.getenv("SUPABASE_DB_NAME", "postgres")
	port = int(os.getenv("SUPABASE_DB_PORT", "5432"))

	return str(
		URL.create(
			drivername="postgresql+psycopg2",
			username=username,
			password=password,
			host=host,
			port=port,
			database=database_name,
			query={"sslmode": "require"},
		)
	)


DATABASE_URL = _get_database_url()

engine = None
if DATABASE_URL:
	engine_kwargs: dict[str, object] = {"pool_pre_ping": True}
	if "sslmode=" not in DATABASE_URL:
		engine_kwargs["connect_args"] = {"sslmode": "require"}
	engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
	bind=engine,
	autoflush=False,
	autocommit=False,
	expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
	if engine is None:
		raise RuntimeError(
			"Database is not configured. Set SUPABASE_DB_URL (or DATABASE_URL), "
			"or use SUPABASE_DB_HOST and SUPABASE_DB_PASSWORD."
		)

	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


def check_database_connection() -> tuple[bool, str]:
	if engine is None:
		return False, (
			"Database is not configured. Set SUPABASE_DB_URL (or DATABASE_URL), "
			"or use SUPABASE_DB_HOST and SUPABASE_DB_PASSWORD."
		)

	try:
		with engine.connect() as connection:
			connection.execute(text("SELECT 1"))
		return True, "Connected to Supabase successfully."
	except Exception as exc:  # noqa: BLE001
		error_text = str(exc)
		hint = ""
		if "could not translate host name" in error_text:
			hint = (
				" Hint: your database URL appears malformed. "
				"If your password contains special characters like @ or :, "
				"URL-encode it, or use SUPABASE_DB_HOST/SUPABASE_DB_PASSWORD instead."
			)
		return False, f"Database connection failed: {exc}{hint}"