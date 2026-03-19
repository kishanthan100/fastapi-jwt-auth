from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
import jwt

# ========================
# CONFIG
# ========================
SECRET_KEY = "i67dYLCRNauBvBFB7REnCcHqL5lMgmHuQ5rwUIFvRV4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=102400,
    argon2__parallelism=8,
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
# ========================
# JWT CREATION
# ========================
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ========================
# JWT DECODE

# ========================
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ========================
# AUTH DEPENDENCY (COOKIE BASED)
# ========================
def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    payload = decode_access_token(token)

    user_id = payload.get("sub")
    email = payload.get("email")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"id": user_id, "email": email}



