from sqlalchemy.orm import Session
from app.crud.auth_crud import  create_user, get_user_by_email, get_user_details_by_email
from fastapi import HTTPException
from app.core.security import get_hash_password,verify_password



def login_from_userdetailstable(db: Session,  email: str, password: str):
    user = get_user_details_by_email(db, email)

    if not user:
        return None
    if not verify_password(password, user.password):
        return None

    # Business logic can be expanded here if needed
    print("login success")
    return user
    #return {"message": "Login success"}





def register_service(db, name, email, password, nic, address, phone):
    
    existing_user = get_user_by_email(db, email)
    if existing_user:
        return None

    hashed_pwd = get_hash_password(password)

    user_data = {
        "name": name,
        "email": email,
        "password": hashed_pwd,
        "nic": nic,
        "address": address,
        "phone": phone
    }

    return create_user(db, user_data)