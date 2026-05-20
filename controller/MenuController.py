from sqlalchemy.orm import Session
from model.Menu import Menu as MenuModel
from model.MenuPoster import MenuPoster as MenuPosterModel
from fastapi import HTTPException
from datetime import datetime
import os
import shutil
from pathlib import Path

# Define the uploads folder
UPLOADS_FOLDER = "uploads/menu_posters"
Path(UPLOADS_FOLDER).mkdir(parents=True, exist_ok=True)

def get_all_menus(db: Session):
    return db.query(MenuModel).all()

def get_menu_by_id(db: Session, menu_id: int):
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu

def create_menu(db: Session, name: str, start_date: datetime, end_date: datetime, poster_paths: list = None):
    menu = MenuModel(name=name, start_date=start_date, end_date=end_date)
    db.add(menu)
    db.commit()
    db.refresh(menu)

    if poster_paths:
        for path in poster_paths:
            poster = MenuPosterModel(menu_id=menu.id, poster_path=path)
            db.add(poster)
        db.commit()

    return menu

def update_menu(db: Session, menu_id: int, name: str = None, start_date: datetime = None, end_date: datetime = None):
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    if name:
        menu.name = name
    if start_date:
        menu.start_date = start_date
    if end_date:
        menu.end_date = end_date

    db.commit()
    db.refresh(menu)
    return menu

def delete_menu(db: Session, menu_id: int):
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    # Delete associated poster files from disk
    posters = db.query(MenuPosterModel).filter(MenuPosterModel.menu_id == menu_id).all()
    for poster in posters:
        delete_poster_file(poster.poster_path)

    # Delete associated posters from database
    db.query(MenuPosterModel).filter(MenuPosterModel.menu_id == menu_id).delete()
    db.delete(menu)
    db.commit()
    return menu

def get_all_menu_posters(db: Session):
    return db.query(MenuPosterModel).all()

def get_menu_poster_by_id(db: Session, poster_id: int):
    poster = db.query(MenuPosterModel).filter(MenuPosterModel.id == poster_id).first()
    if not poster:
        raise HTTPException(status_code=404, detail="Menu poster not found")
    return poster

def get_menu_posters_by_menu(db: Session, menu_id: int):
    # Verify menu exists
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return db.query(MenuPosterModel).filter(MenuPosterModel.menu_id == menu_id).all()

def create_menu_poster(db: Session, menu_id: int, poster_path: str):
    # Verify menu exists
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    poster = MenuPosterModel(menu_id=menu_id, poster_path=poster_path)
    db.add(poster)
    db.commit()
    db.refresh(poster)
    return poster

def delete_menu_poster(db: Session, poster_id: int):
    poster = db.query(MenuPosterModel).filter(MenuPosterModel.id == poster_id).first()
    if not poster:
        raise HTTPException(status_code=404, detail="Menu poster not found")

    # Delete poster file from disk
    delete_poster_file(poster.poster_path)

    db.delete(poster)
    db.commit()
    return poster

def delete_poster_file(poster_path: str):
    """Delete poster image file from disk"""
    try:
        if os.path.exists(poster_path):
            os.remove(poster_path)
    except Exception as e:
        print(f"Error deleting file {poster_path}: {str(e)}")

def save_poster_file(file_content: bytes, filename: str) -> str:
    """Save uploaded poster file to disk and return the file path"""
    try:
        # Create uploads folder if it doesn't exist
        Path(UPLOADS_FOLDER).mkdir(parents=True, exist_ok=True)

        # Save file with timestamp to avoid conflicts
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        safe_filename = timestamp + filename
        file_path = os.path.join(UPLOADS_FOLDER, safe_filename)

        with open(file_path, 'wb') as f:
            f.write(file_content)

        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
