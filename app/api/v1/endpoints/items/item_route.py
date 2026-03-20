from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.database import SessionLocal
from app.services.item_service import fetch_items, get_item_id_details
from app.schemas.item_schema import ItemsResponse
from app.core.templates import templates
from app.core.security import get_current_user

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ItemsResponse])
def read_items(db: Session = Depends(get_db)):

    return fetch_items(db)





# @router.get("/dashboard")
# def dashboard(
#     request: Request,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user)):
#     items = fetch_items(db)

#     return templates.TemplateResponse(
#         "items/dashboard.html",
#         {
#             "request": request,
#             "items": items,
#             "user": current_user
#         }
#     )



@router.get("/dashboard")
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    items = fetch_items(db)

    response = templates.TemplateResponse(
        "items/dashboard.html",
        {
            "request": request,
            "items": items,
            "user": current_user
        }
    )

    # 🔥 if refreshed → update cookie
    if hasattr(request.state, "new_access_token"):
        response.set_cookie(
            key="access_token",
            value=request.state.new_access_token,
            httponly=True
        )

    return response




@router.get("/item_details/{item_id}")
def item_details(item_id: int, 
                 request: Request, 
                 db: Session = Depends(get_db),
                 current_user: dict = Depends(get_current_user)
                 ):
    item = get_item_id_details(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return templates.TemplateResponse(
        "items/item_details.html",
        {"request": request, 
         "item": item},
         status_code=200
    )