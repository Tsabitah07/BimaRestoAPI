from model.Table import Table as table_model
from sqlalchemy.orm import Session

data = [
    {
        "number": "Table 1",
        "capacity": 4
    },
    {
        "number": "Table 2",
        "capacity": 4
    },
    {
        "number": "Table 3",
        "capacity": 6
    },
    {
        "number": "Table 4",
        "capacity": 6
    },
    {
        "number": "Table 5",
        "capacity": 8
    }
]

def seed_data(db: Session):
    if not db.query(table_model).first():
        for item in data:
            role = table_model(
                number=item["number"],
                capacity=item["capacity"]
            )
            db.add(role)
        db.commit()
        print("Database seeded with initial roles.")
    else:
        print("Roles already exist, skipping seeding.")