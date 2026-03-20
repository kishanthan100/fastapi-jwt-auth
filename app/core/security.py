from datetime import datetime, timedelta
from fastapi import Request, HTTPException, status
from passlib.context import CryptContext
#import jwt
from jose import JWTError, ExpiredSignatureError
from jose import jwt

from app.core.config import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES =  settings.ACCESS_TOKEN_EXPIRE_MINUTES
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=102400,
    argon2__parallelism=8,
)

def get_hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password (str): Plain password to hash
    
    Returns:
        str: Hashed password
    """

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password (str): Password to verify
        hashed_password (str): Hashed password to compare against
    
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)
# ========================
# JWT CREATION
# ========================
def create_access_token(data: dict):

    """
    Create a JWT access token.
    
    Args:
        data (dict): Data to encode in token
    
    Returns:
        str: Encoded JWT token
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire,
                     "type": "access"
                      })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):

    """
    Create a JWT refresh token.
    
    Args:
        data (dict): Data to encode in token
    
    Returns:
        str: Encoded JWT token
    """

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    # try:
    #     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #     return payload
    # except jwt.ExpiredSignatureError:
    #     raise HTTPException(status_code=401, detail="Token expired")
    # except jwt.InvalidTokenError:
    #     raise HTTPException(status_code=401, detail="Invalid token")


# def get_current_user(request: Request):
#     token = request.cookies.get("access_token")

#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated"
#         )

#     payload = decode_access_token(token)

#     user_id = payload.get("sub")
#     email = payload.get("email")
#     if user_id is None:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     return {"id": user_id, "email": email}


def get_current_user(request: Request):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    # 🔹 1. Try access token (your existing logic)
    if access_token:
        try:
            payload = decode_access_token(access_token)

            user_id = payload.get("sub")
            email = payload.get("email")

            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token")

            return {"id": user_id, "email": email}

        except (JWTError, ExpiredSignatureError):
            pass  # expired → fallback to refresh

    # 🔹 2. Try refresh token (NEW)
    if refresh_token:
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

            if payload.get("type") != "refresh":
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            user_id = payload.get("sub")
            email = payload.get("email")

            # 🔥 generate new access token
            new_access_token = create_access_token({
                "sub": user_id,
                "email": email
            })

            # 🔥 attach to request (important)
            request.state.new_access_token = new_access_token

            return {"id": user_id, "email": email}

        except (JWTError, ExpiredSignatureError):
            pass

    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated"
    )
