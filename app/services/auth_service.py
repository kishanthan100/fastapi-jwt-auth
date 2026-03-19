from sqlalchemy.orm import Session
from app.crud.auth_crud import check_user, create_user, get_user_by_email, check_user_from_userdetailstable
from fastapi import HTTPException
from app.core.security import hash_password,verify_password

# def login(db: Session, user_id: int, email: str):
#     user = check_user(db, user_id, email)

#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     # Business logic can be expanded here if needed
#     print("login success")
#     return user
#     #return {"message": "Login success"}



def login_from_userdetailstable(db: Session,  email: str, password: str):
    user = check_user_from_userdetailstable(db, email)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Business logic can be expanded here if needed
    print("login success")
    return user
    #return {"message": "Login success"}





def register_service(db, name, email, password, nic, address, phone):
    
    # 🔍 Check if user exists
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return None

    # 🔐 Hash password
    hashed_pwd = hash_password(password)

    # 🧱 Prepare data
    user_data = {
        "name": name,
        "email": email,
        "password": hashed_pwd,
        "nic": nic,
        "address": address,
        "phone": phone
    }

    return create_user(db, user_data)