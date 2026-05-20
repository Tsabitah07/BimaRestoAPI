from sqlalchemy.orm import Session
from model.Role import Role as RoleModel
from fastapi import HTTPException


def get_all_roles(db: Session):
    """Get all roles"""
    return db.query(RoleModel).all()


def get_role_by_id(db: Session, role_id: int):
    """Get role by ID"""
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role tidak ditemukan")
    return role


def create_role(db: Session, name: str):
    """Create new role"""
    # Check if role name already exists
    if db.query(RoleModel).filter(RoleModel.name == name).first():
        raise HTTPException(status_code=400, detail="Role sudah ada")

    # Create role
    role = RoleModel(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def update_role(db: Session, role_id: int, name: str):
    """Update role"""
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role tidak ditemukan")

    # Check if new name is unique
    if name and name != role.name:
        if db.query(RoleModel).filter(RoleModel.name == name).first():
            raise HTTPException(status_code=400, detail="Role sudah ada")
        role.name = name

    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role_id: int):
    """Delete role"""
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role tidak ditemukan")

    db.delete(role)
    db.commit()
    return role

