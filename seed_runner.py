from database import SessionLocal
from seed.role import seed_data as seed_role_data
from seed.user import seed_data as seed_user_data
from seed.menu import seed_data as seed_menu_data
from seed.booking_status import seed_data as seed_booking_status_data
from seed.booking_session import seed_data as seed_booking_session_data
from seed.booking import seed_data as seed_booking_data
from seed.food import seed_data as seed_food_data



def run():
    db = SessionLocal()
    try:
        print("Seeding roles...")
        seed_role_data(db)

        print("Seeding users...")
        seed_user_data(db)

        print("Seeding menus and posters...")
        seed_menu_data(db)

        print("Seeding booking statuses...")
        seed_booking_status_data(db)

        print("Seeding booking sessions...")
        seed_booking_session_data(db)

        print("Seeding food packages...")
        seed_food_data(db)

        print("Seeding bookings...")
        seed_booking_data(db)

        print("Seeding completed")
    except Exception as e:
        print("ERROR SEED:", e)
    finally:
        db.close()

if __name__ == "__main__":
    run()