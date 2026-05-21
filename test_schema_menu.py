from schema.menuResponse import MenuSchema
from schema.foodPackageResponse import FoodPackageSchema

# Mock ORM-like objects
class MockPoster:
    def __init__(self, poster_path):
        self.poster_path = poster_path

class MockFoodPackage:
    def __init__(self, id, name, description, menu_id, session_id, available_quantity):
        self.id = id
        self.name = name
        self.description = description
        self.menu_id = menu_id
        self.session_id = session_id
        self.available_quantity = available_quantity

class MockMenu:
    def __init__(self, id, name, start_date, end_date, posters, food_packages):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.posters = posters
        self.food_packages = food_packages

mock_posters = [MockPoster('uploads/menu_posters/a.jpg'), MockPoster('uploads/menu_posters/b.jpg')]
mock_foods = [
    MockFoodPackage(1, 'Package A', 'Desc A', 1, 1, 10),
    MockFoodPackage(2, 'Package B', 'Desc B', 1, 2, 5)
]

mock_menu = MockMenu(1, 'Menu 1', '2024-01-01T00:00:00', '2024-01-07T00:00:00', mock_posters, mock_foods)

schema = MenuSchema.from_orm_with_posters(mock_menu)
print(schema.json(indent=2))

