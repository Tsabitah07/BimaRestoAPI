from database import SessionLocal
from seed.role import seed_data as seed_role_data
from seed.user import seed_data as seed_user_data
from seed.table import seed_data as seed_table_data
from seed.menu import seed_data as seed_menu_data
from seed.booking_status import seed_data as seed_booking_status_data
from seed.booking_session import seed_data as seed_booking_session_data
from seed.booking import seed_data as seed_booking_data

from model import BookedTable


def run():
    db = SessionLocal()
    try:
        print("Seeding role...")
        seed_role_data(db)

        print("Seeding user...")
        seed_user_data(db)

        print("Seeding Table...")
        seed_table_data(db)

        print("Seeding Menu...")
        seed_menu_data(db)

        print("Seeding Booking Status...")
        seed_booking_status_data(db)

        print("Seeding Booking Session...")
        seed_booking_session_data(db)

        print("Seeding Booking...")
        seed_booking_data(db)

        print("Seeding selesai")
    except Exception as e:
        print("ERROR SEED:", e)
    finally:
        db.close()

if __name__ == "__main__":
    run()