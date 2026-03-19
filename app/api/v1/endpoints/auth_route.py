from fastapi import APIRouter, Depends, Request,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.auth_schema import LoginRequest
from app.services.auth_service import register_service, login_from_userdetailstable
from app.core.templates import templates
from app.core.security import create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})



@router.post("/login-form")
def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = login_from_userdetailstable(db, email,password)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    token = create_access_token({"sub": str(user.id),"email": user.email})

    response = RedirectResponse(url="/items/dashboard", status_code=303)

    # ✅ STORE TOKEN IN COOKIE
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,   # True in production (HTTPS)
        samesite="lax"
    )

    return response



@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@router.post("/register-form")
def register_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    nic: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    user = register_service(
        db=db,
        name=name,
        email=email,
        password=password,
        nic=nic,
        address=address,
        phone=phone
    )

    if not user:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "error": "User already exists",
                "error": f"*{email}* already exists",
                "user": email
            }
        )

    return RedirectResponse(url="/", status_code=303)






@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")  # ✅ remove token
    return response