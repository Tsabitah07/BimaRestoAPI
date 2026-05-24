from model.Menu import Menu as menu_model
from model.MenuPoster import MenuPoster as menu_poster_model
from sqlalchemy.orm import Session
from datetime import datetime

data = [
    {
        "name": "Kalimantan Menu",
        "start_date": "2026-03-01T00:00:00",
        "end_date": "2026-03-31T23:59:59",
        "poster_path": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc6OKcNakCZK3XwAzylxjh-e0UUiXGIkISgQ&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3bqI38XG5ElnAezm2PCkMSxH9gKrndM-Gjw&s"
        ]
    },
    {
        "name": "Sumatra Menu",
        "start_date": "2026-04-01T00:00:00",
        "end_date": "2026-04-30T23:59:59",
        "poster_path": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_SGy0ihWZ5BHyL7nRsQqQQ0ouz4bw7ILWZw&s"
        ]
    },
    {
        "name": "Javanese Menu",
        "start_date": "2026-05-01T00:00:00",
        "end_date": "2026-05-31T23:59:59",
        "poster_path": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRzQF0DmrCUqZ88srHXQ8bTLftS6LhWmei5A&s"
        ]
    },
    {
        "name": "Balinese Menu",
        "start_date": "2026-06-01T00:00:00",
        "end_date": "2026-06-30T23:59:59",
        "poster_path": [
            "https://blog.thewonderspace.com/wp-content/uploads/2025/04/1._Nasi-Campur-Bali-1024x683.jpg",
            "https://thewonderspace.com/_next/image?url=https%3A%2F%2Fblog.thewonderspace.com%2Fwp-content%2Fuploads%2F2025%2F04%2Fmakanan-tradisional-bali.jpg&w=2048&q=75"
        ]
    },
        {
            "name": "Papua Menu",
            "start_date": "2026-06-01T00:00:00",
            "end_date": "2026-06-30T23:59:59",
            "poster_path": [
                "https://asset.kompas.com/crops/5oTNU_nt56puZ7u-m5eoNmW7BrA=/0x384:4608x3456/750x500/data/photo/2019/12/05/5de8cd983fce7.jpg",
                "https://awsimages.detik.net.id/community/media/visual/2019/09/06/001e9ac1-7ec1-49dd-8b22-eb09f65a6a6d_169.jpeg?w=1200"
            ]
        }
]

def seed_data(db: Session):
    if not db.query(menu_model).first():
        for item in data:
            menu_entry = menu_model(
                name=item["name"],
                start_date=datetime.fromisoformat(item["start_date"]),
                end_date=datetime.fromisoformat(item["end_date"])
            )
            db.add(menu_entry)
        db.commit()
        print("Database seeded with initial menus.")
    else:
        print("Menus already exist, skipping seeding.")

    if not db.query(menu_poster_model).first():
        for item in data:
            menu = db.query(menu_model).filter_by(name=item["name"]).first()
            if menu:
                for poster_path in item["poster_path"]:
                    poster = menu_poster_model(
                        menu_id=menu.id,
                        poster_path=poster_path
                    )
                    db.add(poster)
        db.commit()
        print("Database seeded with initial menu posters.")
    else:
        print("Menu posters already exist, skipping seeding.")