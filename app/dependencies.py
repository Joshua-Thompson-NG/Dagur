import os
import secrets
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.database import SessionLocal

load_dotenv()
EXPECTED_API_KEY = os.getenv("API_SECRET_KEY")

# Defines the header name
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# api_key validation
def verify_api_key(incoming_key: str = Security(api_key_header)) -> str:
    if (
        not incoming_key
        or not EXPECTED_API_KEY
        or not secrets.compare_digest(incoming_key, EXPECTED_API_KEY)
    ):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect API key")
    return incoming_key


SessionDep = Annotated[Session, Depends(get_db)]
VerifyAPIKey = Annotated[Security, Depends(verify_api_key)]