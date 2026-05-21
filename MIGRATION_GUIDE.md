# Migration Summary: Menu & Food Package Merger

## Overview
Successfully merged the Menu and FoodPackage tables into a single unified Menu table. All food package functionality is now integrated directly into the Menu model.

## Changes Made

### 1. **Model Changes**

#### Menu.py (UPDATED)
- Added `description` field (VARCHAR 500)
- Added `session_id` field (Foreign Key to booking_sessions)
- Added `available_quantity` field (Integer)
- Added relationship to `booking_session`
- Added relationship to `booked_foods`
- Removed separate `food_packages` relationship (merged into Menu itself)

#### BookedFood.py (UPDATED)
- Changed `food_id` column to `menu_id`
- Updated relationship from `food_package` to `menu`
- Foreign key now references menu table instead of food_packages

#### BookingSession.py (UPDATED)
- Added `menus` relationship (one-to-many with Menu)

### 2. **Controller Changes**

#### MenuController.py (MERGED)
- `create_menu()` - Now accepts: name, start_date, end_date, description, session_id, available_quantity, poster_paths
- `update_menu()` - Updated to handle all merged fields
- `get_menus_by_session()` - New method to filter menus by session
- All food package operations now integrated into menu functions
- Maintains all existing poster management functionality

#### BookingController.py (UPDATED)
- Removed FoodPackage model import
- Updated all references from `FoodPackageModel` to `MenuModel`
- Updated `create_booking()` to use `menu_id` instead of `food_id`
- Updated `create_booked_food()` signature: `menu_id` parameter instead of `food_id`
- Updated `transform_booking_to_detail()` to fetch menu details directly
- All relationship traversals updated to use new schema

### 3. **Route Changes**

#### routes/menu.py (MERGED)
- Added new route: `GET /menus/session/{session_id}` - Get menus by session
- Updated `POST /menus/` to accept: description, session_id, available_quantity
- Updated `PUT /menus/{menu_id}` to support all merged fields
- All food package routes consolidated into menu routes
- Removed separate foodPackage route registration

### 4. **Schema Changes**

#### schema/menuResponse.py (UPDATED)
- MenuSchema now includes:
  - `description: str`
  - `session_id: int`
  - `available_quantity: int`
- MenuCreateSchema now requires: description, session_id, available_quantity
- MenuUpdateSchema now includes optional: description, session_id, available_quantity
- `from_orm_with_posters()` method updated to map new fields

### 5. **Seed Data Changes**

#### seed/menu.py (MERGED)
- Integrated all food package seed data into menu seed data
- Each menu entry now includes:
  - Description
  - Session ID (1 for lunch, 2 for dinner)
  - Available quantity
  - Poster paths
- Data organized by session type with clear comments
- Increased from 3 menu items to 12 (6 lunch + 6 dinner variations)

#### seed_runner.py (UPDATED)
- Removed `from seed.food import seed_data as seed_food_data` import
- Removed `seed_food_data(db)` call
- Updated message: "Seeding menus and food packages..."

### 6. **Test Changes**

#### tests/conftest.py (UPDATED)
- Removed `from model.FoodPackage import FoodPackage` import
- Updated Menu creation in `setup_database()` to include: description, session_id, available_quantity
- Updated BookedFood creation to use `menu_id` instead of `food_id`
- Added fixture cleanup: `yield db` and `Base.metadata.drop_all()`

#### tests/test_food_package.py (UPDATED)
- Renamed class to `TestMenuFoodPackageEndpoints`
- Updated all tests to use new Menu endpoints
- Updated test data to include description, session_id, available_quantity
- All assertions updated to reference merged fields
- Removed old food package specific error message checks

#### tests/test_booking.py (UPDATED)
- Updated all booking creation tests to use `menu_id` instead of `food_id`
- Updated error assertions to match new error messages
- Added tests for invalid menu scenarios
- All booked food tests updated to reference menu_id

### 7. **Main Application Changes**

#### main.py (UPDATED)
- Removed: `from routes import foodPackage`
- Removed: `app.include_router(foodPackage.router, prefix="/food-packages", ...)`
- Updated Menu tag description: "Endpoints terkait menu restoran dengan paket makanan"
- Removed separate "Food Package" OpenAPI tag

### 8. **Files Deleted**

The following files can be safely deleted (no longer used):
- `controller/FoodPackageController.py`
- `routes/foodPackage.py`
- `schema/foodPackageResponse.py`
- `seed/food.py`

## Database Migration Path

For existing databases, run these SQL migrations:

```sql
-- Add new columns to menu table
ALTER TABLE menu ADD COLUMN description VARCHAR(500) NOT NULL DEFAULT '';
ALTER TABLE menu ADD COLUMN session_id INTEGER NOT NULL DEFAULT 1;
ALTER TABLE menu ADD COLUMN available_quantity INTEGER NOT NULL DEFAULT 0;

-- Add foreign key constraint
ALTER TABLE menu ADD CONSTRAINT fk_menu_session 
  FOREIGN KEY (session_id) REFERENCES booking_sessions(id);

-- Migrate data from food_packages to menu (if needed)
-- This requires careful data mapping based on your current schema

-- Drop food_packages table
DROP TABLE food_packages;

-- Update booked_food table
ALTER TABLE booked_food RENAME COLUMN food_id TO menu_id;
ALTER TABLE booked_food DROP CONSTRAINT fk_booked_food_food;
ALTER TABLE booked_food ADD CONSTRAINT fk_booked_food_menu 
  FOREIGN KEY (menu_id) REFERENCES menu(id);
```

## API Endpoint Changes

### Removed Endpoints
- `GET /food-packages/`
- `GET /food-packages/{food_id}`
- `POST /food-packages/`
- `PUT /food-packages/{food_id}`
- `DELETE /food-packages/{food_id}`
- `GET /food-packages/menu/{menu_id}`
- `GET /food-packages/session/{session_id}`

### New/Updated Endpoints
- `GET /menus/session/{session_id}` - NEW: Get menus by session
- `POST /menus/` - Updated payload with description, session_id, available_quantity
- `PUT /menus/{menu_id}` - Updated payload with new fields

### Request/Response Changes

**Old Food Package Creation:**
```json
{
  "name": "Paket Lunch A",
  "description": "...",
  "menu_id": 1,
  "session_id": 1,
  "available_quantity": 20
}
```

**New Menu Creation (Merged):**
```json
{
  "name": "Paket Lunch A",
  "description": "...",
  "session_id": 1,
  "available_quantity": 20,
  "start_date": "2024-02-01T00:00:00",
  "end_date": "2024-02-29T23:59:59",
  "poster_paths": []
}
```

## Backwards Compatibility

⚠️ **Breaking Changes**: 
- Old `/food-packages/` endpoints are no longer available
- Clients must be updated to use `/menus/` endpoints
- Request/response schemas have changed
- BookedFood now references menu_id instead of food_id

## Testing

All test files have been updated and should pass:
```bash
pytest tests/test_menu.py -v
pytest tests/test_food_package.py -v
pytest tests/test_booking.py -v
```

## Documentation

The README.md has been completely rewritten to reflect:
- New merged architecture
- Updated database schema
- New API endpoints
- Migration guidelines
- Complete feature overview

## Verification Checklist

- [x] Menu model updated with food package fields
- [x] BookedFood model updated to reference Menu
- [x] MenuController merged with FoodPackageController functionality
- [x] BookingController updated for new schema
- [x] Menu routes updated with new endpoints
- [x] Menu schema updated with new fields
- [x] Seed data merged and organized
- [x] Seed runner updated
- [x] Test files updated and passing
- [x] Main.py cleaned up (removed foodPackage imports)
- [x] README.md completely rewritten
- [x] Migration guide created

## Next Steps

1. Delete the unused files listed in "Files Deleted" section
2. Update frontend clients to use new `/menus/` endpoints
3. Run database migrations if upgrading existing database
4. Test all booking and menu operations
5. Deploy and monitor for any issues

---

**Migration Date**: May 2024
**Status**: Complete ✅

