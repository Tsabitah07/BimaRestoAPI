from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from controller import MenuController
from schema.menuResponse import (
    MenuSchema, MenuCreateSchema, MenuUpdateSchema,
    MenuResponseSchema, MenuListResponseSchema,
    MenuPosterSchema, MenuPosterResponseSchema, MenuPosterListResponseSchema,
    MenuPosterCreateSchema
)

router = APIRouter()

# Menu endpoints
@router.get("/", tags=["Menu"], response_model=MenuListResponseSchema)
def get_all_menus(db: Session = Depends(get_db)):
    """Get all menus with their posters"""
    try:
        menus = MenuController.get_all_menus(db)
        menu_schemas = [MenuSchema.from_orm_with_posters(menu) for menu in menus]
        return {
            "message": "Menus retrieved successfully",
            "status": 200,
            "data": menu_schemas
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{menu_id}", tags=["Menu"], response_model=MenuResponseSchema)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Get a specific menu by ID with all its posters"""
    try:
        menu = MenuController.get_menu_by_id(db, menu_id)
        menu_schema = MenuSchema.from_orm_with_posters(menu)
        return {
            "message": "Menu retrieved successfully",
            "status": 200,
            "data": menu_schema
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", tags=["Menu"], response_model=MenuResponseSchema, status_code=201)
def create_menu(payload: MenuCreateSchema, db: Session = Depends(get_db)):
    """Create a new menu"""
    try:
        menu = MenuController.create_menu(
            db,
            payload.name,
            payload.start_date,
            payload.end_date,
            payload.poster_paths
        )
        menu_schema = MenuSchema.from_orm_with_posters(menu)
        return {
            "message": "Menu created successfully",
            "status": 201,
            "data": menu_schema
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{menu_id}", tags=["Menu"], response_model=MenuResponseSchema)
def update_menu(menu_id: int, payload: MenuUpdateSchema, db: Session = Depends(get_db)):
    """Update a menu"""
    try:
        menu = MenuController.update_menu(
            db,
            menu_id,
            payload.name,
            payload.start_date,
            payload.end_date
        )
        menu_schema = MenuSchema.from_orm_with_posters(menu)
        return {
            "message": "Menu updated successfully",
            "status": 200,
            "data": menu_schema
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{menu_id}", tags=["Menu"], response_model=MenuResponseSchema)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Delete a menu and all its associated poster images"""
    try:
        menu = MenuController.delete_menu(db, menu_id)
        menu_schema = MenuSchema.from_orm_with_posters(menu)
        return {
            "message": "Menu deleted successfully",
            "status": 200,
            "data": menu_schema
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Menu Poster endpoints
@router.get("/posters/all", tags=["Menu"], response_model=MenuPosterListResponseSchema)
def get_all_menu_posters(db: Session = Depends(get_db)):
    """Get all menu posters"""
    try:
        posters = MenuController.get_all_menu_posters(db)
        return {
            "message": "Menu posters retrieved successfully",
            "status": 200,
            "data": posters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posters/{poster_id}", tags=["Menu"], response_model=MenuPosterResponseSchema)
def get_menu_poster(poster_id: int, db: Session = Depends(get_db)):
    """Get a specific menu poster by ID"""
    try:
        poster = MenuController.get_menu_poster_by_id(db, poster_id)
        return {
            "message": "Menu poster retrieved successfully",
            "status": 200,
            "data": poster
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{menu_id}/posters", tags=["Menu"], response_model=MenuPosterListResponseSchema)
def get_menu_posters(menu_id: int, db: Session = Depends(get_db)):
    """Get all posters for a specific menu"""
    try:
        posters = MenuController.get_menu_posters_by_menu(db, menu_id)
        return {
            "message": "Menu posters retrieved successfully",
            "status": 200,
            "data": posters
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{menu_id}/posters/upload", tags=["Menu"], response_model=MenuPosterResponseSchema)
def upload_menu_poster(menu_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a new menu poster image file to a specific menu"""
    try:
        # Read file content
        content = file.file.read()

        # Save file to disk
        file_path = MenuController.save_poster_file(content, file.filename)

        # Create poster record in database
        poster = MenuController.create_menu_poster(db, menu_id, file_path)
        return {
            "message": "Menu poster uploaded successfully",
            "status": 201,
            "data": poster
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/posters", tags=["Menu"], response_model=MenuPosterResponseSchema, status_code=201)
def create_menu_poster(payload: MenuPosterCreateSchema, db: Session = Depends(get_db)):
    """Create a new menu poster with file path (legacy endpoint)"""
    try:
        poster = MenuController.create_menu_poster(db, payload.menu_id, payload.poster_path)
        return {
            "message": "Menu poster created successfully",
            "status": 201,
            "data": poster
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/posters/{poster_id}", tags=["Menu"], response_model=MenuPosterResponseSchema)
def delete_menu_poster(poster_id: int, db: Session = Depends(get_db)):
    """Delete a menu poster and remove its image file"""
    try:
        poster = MenuController.delete_menu_poster(db, poster_id)
        return {
            "message": "Menu poster deleted successfully",
            "status": 200,
            "data": poster
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
