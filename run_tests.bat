@echo off
REM Script untuk menjalankan unit tests di Windows

echo.
echo ========================================
echo BimaRestoAPI Unit Testing
echo ========================================
echo.

REM Check if pytest is installed
pytest --version >nul 2>&1
if errorlevel 1 (
    echo Error: pytest tidak terinstall!
    echo Install dengan: pip install -r requirements-test.txt
    exit /b 1
)

echo OK: pytest terdeteksi
echo.

REM Default command
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=all

if "%COMMAND%"=="all" (
    echo Running all tests...
    pytest -v
    goto end
)

if "%COMMAND%"=="auth" (
    echo Running authentication tests...
    pytest tests/test_authentication.py -v
    goto end
)

if "%COMMAND%"=="user" (
    echo Running user tests...
    pytest tests/test_user.py -v
    goto end
)

if "%COMMAND%"=="role" (
    echo Running role tests...
    pytest tests/test_role.py -v
    goto end
)

if "%COMMAND%"=="session" (
    echo Running booking session tests...
    pytest tests/test_booking_session.py -v
    goto end
)

if "%COMMAND%"=="menu" (
    echo Running menu tests...
    pytest tests/test_menu.py -v
    goto end
)

if "%COMMAND%"=="food" (
    echo Running food package tests...
    pytest tests/test_food_package.py -v
    goto end
)

if "%COMMAND%"=="booking" (
    echo Running booking tests...
    pytest tests/test_booking.py -v
    goto end
)

if "%COMMAND%"=="coverage" (
    echo Running tests with coverage report...
    pytest --cov=. --cov-report=html -v
    echo.
    echo OK: Coverage report tersimpan di htmlcov/index.html
    goto end
)

if "%COMMAND%"=="quick" (
    echo Running tests in quick mode...
    pytest -q
    goto end
)

if "%COMMAND%"=="help" (
    echo Usage: run_tests.bat [command]
    echo.
    echo Commands:
    echo   all       - Run all tests (default^)
    echo   auth      - Run authentication tests
    echo   user      - Run user CRUD tests
    echo   role      - Run role CRUD tests
    echo   session   - Run booking session CRUD tests
    echo   menu      - Run menu CRUD tests
    echo   food      - Run food package CRUD tests
    echo   booking   - Run booking CRUD tests
    echo   coverage  - Run tests with coverage report
    echo   quick     - Run tests in quiet mode
    echo   help      - Show this help message
    goto end
)

echo Error: Unknown command: %COMMAND%
echo Use 'run_tests.bat help' untuk melihat bantuan
exit /b 1

:end
echo.
echo ========================================
echo OK: Testing selesai
echo ========================================
#!/bin/bash
# Script untuk menjalankan unit tests

echo "========================================"
echo "BimaRestoAPI Unit Testing"
echo "========================================"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest tidak terinstall!"
    echo "Install dengan: pip install -r requirements-test.txt"
    exit 1
fi

echo "✓ pytest terdeteksi"
echo ""

# Default command
COMMAND=${1:-"all"}

case $COMMAND in
    "all")
        echo "🧪 Menjalankan semua tests..."
        pytest -v
        ;;
    "auth")
        echo "🧪 Menjalankan authentication tests..."
        pytest tests/test_authentication.py -v
        ;;
    "user")
        echo "🧪 Menjalankan user tests..."
        pytest tests/test_user.py -v
        ;;
    "role")
        echo "🧪 Menjalankan role tests..."
        pytest tests/test_role.py -v
        ;;
    "session")
        echo "🧪 Menjalankan booking session tests..."
        pytest tests/test_booking_session.py -v
        ;;
    "menu")
        echo "🧪 Menjalankan menu tests..."
        pytest tests/test_menu.py -v
        ;;
    "food")
        echo "🧪 Menjalankan food package tests..."
        pytest tests/test_food_package.py -v
        ;;
    "booking")
        echo "🧪 Menjalankan booking tests..."
        pytest tests/test_booking.py -v
        ;;
    "coverage")
        echo "🧪 Menjalankan tests dengan coverage report..."
        pytest --cov=. --cov-report=html -v
        echo "✓ Coverage report tersimpan di htmlcov/index.html"
        ;;
    "quick")
        echo "🧪 Menjalankan tests (quick mode)..."
        pytest -q
        ;;
    "help")
        echo "Usage: ./run_tests.sh [command]"
        echo ""
        echo "Commands:"
        echo "  all       - Run all tests (default)"
        echo "  auth      - Run authentication tests"
        echo "  user      - Run user CRUD tests"
        echo "  role      - Run role CRUD tests"
        echo "  session   - Run booking session CRUD tests"
        echo "  menu      - Run menu CRUD tests"
        echo "  food      - Run food package CRUD tests"
        echo "  booking   - Run booking CRUD tests"
        echo "  coverage  - Run tests with coverage report"
        echo "  quick     - Run tests in quiet mode"
        echo "  help      - Show this help message"
        ;;
    *)
        echo "❌ Unknown command: $COMMAND"
        echo "Use './run_tests.sh help' untuk melihat bantuan"
        exit 1
        ;;
esac

echo ""
echo "========================================"
echo "✓ Testing selesai"
echo "========================================"

