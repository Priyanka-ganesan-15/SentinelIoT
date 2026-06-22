from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.devices import router as devices_router
from app.db.database import check_database_connection

app = FastAPI(title="SentinelIoT API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(devices_router, tags=["devices"])


@app.get("/")
def root() -> dict[str, str]:
	return {"message": "SentinelIoT API"}


@app.get("/health/db")
def db_health() -> dict[str, str]:
	is_connected, message = check_database_connection()
	if not is_connected:
		raise HTTPException(status_code=503, detail=message)

	return {"status": "ok", "message": message}