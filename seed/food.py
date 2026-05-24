from model.FoodPackage import FoodPackage as food_package_model
from sqlalchemy.orm import Session

data = [
    {
        "name": "Soto Banjar Mantap",
        "description": "Nasi, soto banjar ayam kampung, perkedel, dan sate ayam",
        "menu_id": 1,
        "session_id": 1,
        "available_quantity": 20
    },
    {
        "name": "Ikan Patin Bakar",
        "description": "Nasi, patin bakar bambu, sayur asam kutai, dan sambal raja",
        "menu_id": 1,
        "session_id": 1,
        "available_quantity": 20
    },
    {
        "name": "Nasi Kuning Banjar",
        "description": "Nasi kuning, haruan (ikan gabus) masak habang, dan telur",
        "menu_id": 1,
        "session_id": 2,
        "available_quantity": 20
    },
    {
        "name": "Mie Sagu Pontianak",
        "description": "Mie sagu goreng, bakwan udang, dan kerupuk ikan",
        "menu_id": 1,
        "session_id": 2,
        "available_quantity": 20
    },
{
        "name": "Rendang Padang Set",
        "description": "Nasi, rendang daging, gulai nangka, dan sambal ijo",
        "menu_id": 2,
        "session_id": 1,
        "available_quantity": 20
      },
      {
        "name": "Sate Padang Pariaman",
        "description": "Sate lidah sapi, ketupat, dan keripik singkong pedas",
        "menu_id": 2,
        "session_id": 1,
        "available_quantity": 20
      },
      {
        "name": "Pempek Komplit",
        "description": "Kapal selam, lenjer, adaan, dan mie kuning",
        "menu_id": 2,
        "session_id": 2,
        "available_quantity": 20
      },
      {
        "name": "Mie Aceh Spesial",
        "description": "Mie aceh tumis daging, emping, dan acar bawang",
        "menu_id": 2,
        "session_id": 2,
        "available_quantity": 20
      },
{
        "name": "Gudeg Jogja",
        "description": "Nasi, gudeg, krecek pedas, dan opor ayam",
        "menu_id": 3,
        "session_id": 1,
        "available_quantity": 20
      },
      {
        "name": "Rawon Surabaya",
        "description": "Nasi, rawon daging sapi, telur asin, dan tauge pendek",
        "menu_id": 3,
        "session_id": 1,
        "available_quantity": 20
      },
      {
        "name": "Nasi Liwet Solo",
        "description": "Nasi gurih, ayam suwir, sayur labu siam, dan areh",
        "menu_id": 3,
        "session_id": 2,
        "available_quantity": 20
      },
      {
        "name": "Pecel Madiun",
        "description": "Nasi, sayuran rebus, bumbu kacang, rempeyek, dan tahu tempe",
        "menu_id": 3,
        "session_id": 2,
        "available_quantity": 20
      },
    {
        "name": "Nasi Campur Bali",
        "description": "Nasi, sate lilit, ayam betutu suwir, dan lawar",
        "menu_id": 4,
        "session_id": 1,
        "available_quantity": 20
      },
      {
        "name": "Bebek Bengil Set",
        "description": "Nasi, bebek goreng krispi, sambal matah, dan sayur urap",
        "menu_id": 4,
        "session_id": 1,
        "available_quantity": 20
      },
      {
        "name": "Ayam Betutu Utuh",
        "description": "Nasi, ayam betutu bumbu genep, kacang goreng, dan sambal embe",
        "menu_id": 4,
        "session_id": 2,
        "available_quantity": 20
      },
      {
        "name": "Tipat Cantok",
        "description": "Ketupat, sayuran, bumbu kacang bali, dan kerupuk",
        "menu_id": 4,
        "session_id": 2,
        "available_quantity": 20
      },
  {
    "name": "Paket Papeda Kuah Kuning",
    "description": "Papeda, Ikan Mubara kuah kuning, dan sayur tumis kangkung bunga pepaya",
    "menu_id": 5,
    "session_id": 1,
    "available_quantity": 20
  },
  {
    "name": "Ikan Bakar Manokwari",
    "description": "Ikan tongkol bakar bumbu rempah khas Manokwari, nasi putih, dan sambal mentah",
    "menu_id": 5,
    "session_id": 1,
    "available_quantity": 20
  },
  {
    "name": "Nasi Sagu Komplit",
    "description": "Nasi sagu, sate ulat sagu (opsional/ayam), dan tumis daun pakis",
    "menu_id": 5,
    "session_id": 2,
    "available_quantity": 20
  },
  {
    "name": "Udang Selingkuh Wamena",
    "description": "Udang air tawar saus tiram pedas, nasi putih, dan keladi rebus",
    "menu_id": 5,
    "session_id": 2,
    "available_quantity": 20
  }
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