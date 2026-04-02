from model.FoodPackage import FoodPackage as food_package_model
from sqlalchemy.orm import Session

data = [
    {
        'name': 'Paket Lunch A',
        'description': 'Nasi, Ikan Goreng, Sayur, dan Teh Manis',
        'menu_id': 1,
        'session_id': 1,
        'available_quantity': 20
    },
    {
        'name': 'Paket Lunch B',
        'description': 'Nasi, Ikan Bakar, Sayur, dan Es Teh',
        'menu_id': 1,
        'session_id': 1,
        'available_quantity': 15
    },
    {
        'name': 'Paket Lunch A',
        'description': 'Nasi, Ayam Goreng, Sayur, dan Teh Manis',
        'menu_id': 2,
        'session_id': 1,
        'available_quantity': 20
    },
    {
        'name': 'Paket Lunch B',
        'description': 'Nasi, Ayam Bakar, Sayur, dan Es Teh',
        'menu_id': 2,
        'session_id': 1,
        'available_quantity': 15
    },
    {
        'name': 'Paket Dinner A',
        'description': 'Nasi, Daging Sapi, Sayur, dan Air Mineral',
        'menu_id': 1,
        'session_id': 2,
        'available_quantity': 20
    },
    {
        'name': 'Paket Dinner B',
        'description': 'Nasi, Ayam Bakar, Sayur, dan Es Teh',
        'menu_id': 1,
        'session_id': 2,
        'available_quantity': 15
    },
    {
        'name': 'Paket Dinner A',
        'description': 'Nasi, Daging Sapi, Sayur, dan Air Mineral',
        'menu_id': 2,
        'session_id': 2,
        'available_quantity': 20
    },
    {
        'name': 'Paket Dinner B',
        'description': 'Nasi, Ayam Bakar, Sayur, dan Es Teh',
        'menu_id': 2,
        'session_id': 2,
        'available_quantity': 15
    }
]

from model.FoodPackage import FoodPackage as food_package_model
from sqlalchemy.orm import Session

data = [
    # ==================== LUNCH SESSION ====================

    # MENU 1 - Kalimantan
    {
        'name': 'Paket Lunch A - Kalimantan',
        'description': 'Nasi, Ikan Goreng, Sayur, Teh Manis',
        'menu_id': 1,
        'session_id': 1,
        'available_quantity': 20
    },
    {
        'name': 'Paket Lunch B - Kalimantan',
        'description': 'Nasi, Ikan Bakar, Sayur, Es Teh',
        'menu_id': 1,
        'session_id': 1,
        'available_quantity': 20
    },

    # MENU 2 - Sumatra
    {
        'name': 'Paket Lunch A - Sumatra',
        'description': 'Nasi, Ayam Goreng, Sayur, Teh Manis',
        'menu_id': 2,
        'session_id': 1,
        'available_quantity': 20
    },
    {
        'name': 'Paket Lunch B - Sumatra',
        'description': 'Nasi, Ayam Bakar, Sayur, Es Teh',
        'menu_id': 2,
        'session_id': 1,
        'available_quantity': 20
    },

    # MENU 3 - Javanese
    {
        'name': 'Paket Lunch A - Javanese',
        'description': 'Nasi, Ayam Penyet, Sayur, Teh Manis',
        'menu_id': 3,
        'session_id': 1,
        'available_quantity': 20
    },
    {
        'name': 'Paket Lunch B - Javanese',
        'description': 'Nasi, Ayam Bakar, Sayur, Es Teh',
        'menu_id': 3,
        'session_id': 1,
        'available_quantity': 20
    },

    # ==================== DINNER SESSION ====================

    # MENU 1 - Kalimantan
    {
        'name': 'Paket Dinner A - Kalimantan',
        'description': 'Nasi, Daging Sapi, Sayur, Air Mineral',
        'menu_id': 1,
        'session_id': 2,
        'available_quantity': 20
    },
    {
        'name': 'Paket Dinner B - Kalimantan',
        'description': 'Nasi, Ayam Bakar, Sayur, Es Teh',
        'menu_id': 1,
        'session_id': 2,
        'available_quantity': 20
    },

    # MENU 2 - Sumatra
    {
        'name': 'Paket Dinner A - Sumatra',
        'description': 'Nasi, Rendang, Sayur, Air Mineral',
        'menu_id': 2,
        'session_id': 2,
        'available_quantity': 20
    },
    {
        'name': 'Paket Dinner B - Sumatra',
        'description': 'Nasi, Ayam Pop, Sayur, Es Teh',
        'menu_id': 2,
        'session_id': 2,
        'available_quantity': 20
    },

    # MENU 3 - Javanese
    {
        'name': 'Paket Dinner A - Javanese',
        'description': 'Nasi, Gudeg, Sayur, Air Mineral',
        'menu_id': 3,
        'session_id': 2,
        'available_quantity': 20
    },
    {
        'name': 'Paket Dinner B - Javanese',
        'description': 'Nasi, Ayam Goreng, Sayur, Es Teh',
        'menu_id': 3,
        'session_id': 2,
        'available_quantity': 20
    },
]


def seed_data(db: Session):
    if not db.query(food_package_model).first():
        for item in data:
            food_package = food_package_model(
                name=item["name"],
                description=item["description"],
                menu_id=item["menu_id"],
                session_id=item["session_id"],
                available_quantity=item["available_quantity"]
            )
            db.add(food_package)
        db.commit()
        print("Database seeded with initial food package.")
    else:
        print("Food packages already exist, skipping seeding.")