from model.User import User as user_model
from sqlalchemy.orm import Session
from passlib.context import CryptContext

data = [
    {
        "name": "Admin User",
        "username": "admin",
        "email": "admin@gmail.com",
        "phone_number": "1234567890",
        "password": "admin123",
        "role_id": 1
    },
    {
        "name": "William Brown",
        "username": "william",
        "email": "william.brown@gmail.com",
        "phone_number": "1234567891",
        "password": "employee123",
        "role_id": 2
    },
    {
        "name": "Mary Johnson",
        "username": "mary",
        "email": "mary.johnson@gmail.com",
        "phone_number": "1234567892",
        "password": "user123",
        "role_id": 3
    },
    {
        "name": "Eric Smith",
        "username": "eric",
        "email": "eric.smith@gmail.com",
        "phone_number": "1234567893",
        "password": "employee123",
        "role_id": 2
    },
    {
        "name": "John Doe",
        "username": "user",
        "email": "john.doe@gmail.com",
        "phone_number": "1234567894",
        "password": "user123",
        "role_id": 3
    },
    {
        "name": "Jane Anderson",
        "username": "jane",
        "email": "jane.anderson@gmail.com",
        "phone_number": "1234567895",
        "password": "user123",
        "role_id": 3
    }
]

def hash_password(password):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def seed_data(db: Session):
    if not db.query(user_model).first():
        for item in data:
            user = user_model(
                name=item["name"],
                username=item["username"],
                email=item["email"],
                phone_number=item["phone_number"],
                password=hash_password(item["password"]),
                role_id=item["role_id"]
            )
            db.add(user)
        db.commit()
        print("Database seeded with initial users.")
    else:
        print("Database already seeded.")
