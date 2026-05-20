from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controller import RoleController
from schema.roleResponse import (
    RoleSchema, RoleCreateSchema, RoleUpdateSchema,
    RoleResponseSchema, RoleListResponseSchema
)

router = APIRouter()

@router.get("/", tags=["Role"], response_model=RoleListResponseSchema)
def get_all_roles(db: Session = Depends(get_db)):
    """Get all roles"""
    try:
        roles = RoleController.get_all_roles(db)
        return {
            "message": "Roles retrieved successfully",
            "status": 200,
            "data": roles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{role_id}", tags=["Role"], response_model=RoleResponseSchema)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """Get a specific role by ID"""
    try:
        role = RoleController.get_role_by_id(db, role_id)
        return {
            "message": "Role retrieved successfully",
            "status": 200,
            "data": role
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", tags=["Role"], response_model=RoleResponseSchema)
def create_role(payload: RoleCreateSchema, db: Session = Depends(get_db)):
    """Create a new role"""
    try:
        role = RoleController.create_role(db, payload.name)
        return {
            "message": "Role created successfully",
            "status": 201,
            "data": role
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{role_id}", tags=["Role"], response_model=RoleResponseSchema)
def update_role(role_id: int, payload: RoleUpdateSchema, db: Session = Depends(get_db)):
    """Update a role"""
    try:
        role = RoleController.update_role(db, role_id, payload.name)
        return {
            "message": "Role updated successfully",
            "status": 200,
            "data": role
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{role_id}", tags=["Role"], response_model=RoleResponseSchema)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """Delete a role"""
    try:
        role = RoleController.delete_role(db, role_id)
        return {
            "message": "Role deleted successfully",
            "status": 200,
            "data": role
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

