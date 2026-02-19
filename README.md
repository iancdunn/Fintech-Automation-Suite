# Fintech Automation Suite

This repository contains a professional-grade, high-concurrency end-to-end automation suite for the **Visionsofme** financial application. Built with **Playwright** and **TypeScript**, the suite is engineered to handle complex state management, multi-user isolation, and rapid parallel execution.

---

## Key Features

* **Multi-Tenant Worker Isolation**: Implements a custom worker-scoped architecture that maps each Playwright worker to a unique test account (`demo1`–`demo4`). This eliminates race conditions during parallel execution.
* **On-Demand Authentication**: Features a "lazy-loading" authentication strategy where workers generate and reuse session storage states (`.json`) only when needed.
* **API-Driven State Management**: Utilizes a dedicated Flask reset route (`reset_data`) in the `beforeEach` hook to clear database records in milliseconds, ensuring a "Clean Slate" for every test.
* **Page Object Model (POM)**: Implements an extensible class hierarchy with a `BasePage` and specialized objects for Login, Signup, and Dashboard interactions to maximize code reusability.

---

## Tech Stack

* **Framework**: [Playwright](https://playwright.dev/)
* **Language**: TypeScript
* **Backend Support**: Flask (Python)
* **Design Pattern**: Page Object Model (POM)

---

## Test Coverage

### Transactions
Validates the core financial engine, including:
* Standard deposits and withdrawals.
* Edge-case handling for large amounts ($999,999,999.99).
* Validation logic to prevent non-positive transaction amounts.
* Real-time balance updates and verification of the most recent transaction entry.

### Allocations
Ensures the budget distribution logic remains precise:
* Updating percentages to specific decimal values (e.g., 0.01%).
* Strict enforcement of the "Must add up to 100%" rule.
* Bounds checking to prevent negative values or totals exceeding 100%.

### Authentication
Comprehensive security flow testing:
* Successful login and session persistence.
* Error handling for incorrect passwords and existing usernames.

---

## Configuration & Parallelism

The suite is optimized for high-performance hardware, utilizing the logical processors of modern CPUs.

* **Parallel Workers**: Configured to run 4 simultaneous workers by default to match the test account pool.
* **Automatic Server Orchestration**: The `playwright.config.ts` manages the Flask development server lifecycle automatically via the `webServer` hook.

---

## Project Structure

```text
Fintech_Automation_Suite/
├── Automation_Suite/            # Playwright Testing Framework
│   ├── fixtures/
│   │   └── pom-fixtures.ts      # Multi-tenant worker logic & custom fixtures
│   ├── pages/                   # Page Object Models (POM)
│   │   ├── BasePage.ts          # Parent class for shared navigation
│   │   ├── HomePage.ts          # Dashboard, transactions, and settings logic
│   │   ├── LoginPage.ts         # Authentication selectors and methods
│   │   └── SignupPage.ts        # User registration interaction
│   ├── tests/                   # End-to-End Test Suites
│   │   ├── allocation.test.ts   # Budget distribution & percent logic
│   │   ├── auth.test.ts         # Login/Signup security flows
│   │   ├── balances.test.ts     # Direct balance update validation
│   │   ├── delete-tx.test.ts    # Transaction removal and state cleanup
│   │   └── tx.test.ts           # Core deposit and withdrawal engine
│   ├── playwright.config.ts     # Global test runner & webServer configuration
│   └── .dockerignore            # Build optimization to exclude local artifacts
│
├── Visionsofme/                 # Flask Backend (System Under Test)
│   ├── templates/               # Jinja2 HTML files (Source of UI locators)
│   ├── app.py                   # Main Flask server & database reset API
│   └── ...                      # SQLite database and backend logic
│
├── Dockerfile                   # Blueprint for containerized environment
├── docker-compose.yml           # Service orchestration for Backend & Tests
├── package.json                 # Node.js dependencies (Playwright, TS)
├── package-lock.json            # Deterministic dependency lock file
└── requirements.txt             # Python dependencies (Flask, SQLAlchemy)
