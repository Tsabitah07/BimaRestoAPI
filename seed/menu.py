from model.Menu import Menu as menu_model
from model.MenuPoster import MenuPoster as menu_poster_model
from sqlalchemy.orm import Session
from datetime import datetime

data = [
    {
        "name": "Kalimantan Menu",
        "start_date": "2024-02-01T00:00:00",
        "end_date": "2024-02-29T23:59:59",
        "poster_path": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTc6OKcNakCZK3XwAzylxjh-e0UUiXGIkISgQ&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3bqI38XG5ElnAezm2PCkMSxH9gKrndM-Gjw&s"
        ]
    },
    {
        "name": "Sumatra Menu",
        "start_date": "2024-03-01T00:00:00",
        "end_date": "2024-03-31T23:59:59",
        "poster_path": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_SGy0ihWZ5BHyL7nRsQqQQ0ouz4bw7ILWZw&s"
        ]
    },
    {
        "name": "Javanese Menu",
        "start_date": "2024-04-01T00:00:00",
        "end_date": "2024-03-31T23:59:59",
        "poster_path": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQRzQF0DmrCUqZ88srHXQ8bTLftS6LhWmei5A&s"
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