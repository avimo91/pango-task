# Parkly - QA Automation Assignment

## How to Run

**Prerequisites:** Python 3.8+, Google Chrome, Docker

**1. Start the application:**
```bash
docker run --platform linux/amd64 -d -p 5000:5000 --name parking-manager doringber/parking-manager:3.1.0
```

**2. Install dependencies:**
```bash
pip install pytest selenium webdriver-manager
```

**3. Run the tests:**
```bash
pytest test_cases/test_parking_flows.py -v
```

## Scenarios Chosen and Why

**Test 1 — Start parking and verify active session**
Login → Start parking with dynamically generated data → Verify the session appears in the active table. This is the core business flow of the product.

**Test 2 — Invalid plate validation**
Submit a sequential plate (12345678) → Verify the system rejects it. Confirms that invalid data cannot create a parking session.

## Architecture

- `extensions/` — Selenium action wrappers with explicit waits
- `page_objects/` — UI locators and actions only, no business logic
- `workflows/` — Business flow orchestration, no assertions
- `test_cases/` — Tests with assertions only
- `utils/` — Dynamic test data generation
- `configuration/` — Shared config and URLs
