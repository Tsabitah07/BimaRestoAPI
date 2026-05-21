from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controller import FoodPackageController
from schema.foodPackageResponse import (
    FoodPackageSchema, FoodPackageCreateSchema, FoodPackageUpdateSchema,
    FoodPackageResponseSchema, FoodPackageListResponseSchema
)

router = APIRouter()

@router.get("/", tags=["Food Package"], response_model=FoodPackageListResponseSchema)
def get_all_food_packages(db: Session = Depends(get_db)):
    """Get all food packages"""
    try:
        foods = FoodPackageController.get_all_food_packages(db)
        return {
            "message": "Food packages retrieved successfully",
            "status": 200,
            "data": foods
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{food_id}", tags=["Food Package"], response_model=FoodPackageResponseSchema)
def get_food_package(food_id: int, db: Session = Depends(get_db)):
    """Get a specific food package by ID"""
    try:
        food = FoodPackageController.get_food_package_by_id(db, food_id)
        return {
            "message": "Food package retrieved successfully",
            "status": 200,
            "data": food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", tags=["Food Package"], response_model=FoodPackageResponseSchema, status_code=201)
def create_food_package(payload: FoodPackageCreateSchema, db: Session = Depends(get_db)):
    """Create a new food package"""
    try:
        food = FoodPackageController.create_food_package(
            db,
            payload.name,
            payload.description,
            payload.menu_id,
            payload.session_id,
            payload.available_quantity
        )
        return {
            "message": "Food package created successfully",
            "status": 201,
            "data": food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{food_id}", tags=["Food Package"], response_model=FoodPackageResponseSchema)
def update_food_package(food_id: int, payload: FoodPackageUpdateSchema, db: Session = Depends(get_db)):
    """Update a food package"""
    try:
        food = FoodPackageController.update_food_package(
            db,
            food_id,
            payload.name,
            payload.description,
            payload.menu_id,
            payload.session_id,
            payload.available_quantity
        )
        return {
            "message": "Food package updated successfully",
            "status": 200,
            "data": food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{food_id}", tags=["Food Package"], response_model=FoodPackageResponseSchema)
def delete_food_package(food_id: int, db: Session = Depends(get_db)):
    """Delete a food package"""
    try:
        food = FoodPackageController.delete_food_package(db, food_id)
        return {
            "message": "Food package deleted successfully",
            "status": 200,
            "data": food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/menu/{menu_id}", tags=["Food Package"], response_model=FoodPackageListResponseSchema)
def get_food_packages_by_menu(menu_id: int, db: Session = Depends(get_db)):
    """Get all food packages for a specific menu"""
    try:
        foods = FoodPackageController.get_food_packages_by_menu(db, menu_id)
        return {
            "message": "Food packages retrieved successfully",
            "status": 200,
            "data": foods
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}", tags=["Food Package"], response_model=FoodPackageListResponseSchema)
def get_food_packages_by_session(session_id: int, db: Session = Depends(get_db)):
    """Get all food packages for a specific booking session"""
    try:
        foods = FoodPackageController.get_food_packages_by_session(db, session_id)
        return {
            "message": "Food packages retrieved successfully",
            "status": 200,
            "data": foods
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
