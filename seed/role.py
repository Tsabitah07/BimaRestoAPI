from model.Role import Role as role_model
from sqlalchemy.orm import Session

data = [
    {
        "name": "Admin"
    },
    {
        "name": "Manager"
    },
    {
        "name": "Employee"
    },
    {
        "name": "User"
    }
]

def seed_data(db: Session):
    if not db.query(role_model).first():
        for item in data:
            role = role_model(
                name=item["name"]
            )
            db.add(role)
        db.commit()
        print("Database seeded with initial roles.")
    else:
        print("Roles already exist, skipping seeding.")