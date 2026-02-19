# Fintech Automation Suite

This repository contains a professional-grade, high-concurrency end-to-end automation suite for the **Visionsofme** financial allocation application. Built with **Playwright** and **TypeScript**, the suite is engineered to handle complex state management, multi-user isolation, and rapid parallel execution.

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

The suite is optimized for high-performance hardware, utilizing the logical processors of modern CPUs (like the **Ryzen 5 5600X** or **Intel i3-1215U**).

* **Parallel Workers**: Configured to run 4 simultaneous workers by default to match the test account pool.
* **Automatic Server Orchestration**: The `playwright.config.ts` manages the Flask development server lifecycle automatically via the `webServer` hook.

---

## Project Structure

```text
├── fixtures/
│   └── pom-fixtures.ts   # Centralized Multi-Tenant & Auth Logic
├── pages/                # Page Object Models
│   ├── BasePage.ts       # Shared navigation logic
│   ├── HomePage.ts       # Dashboard & Transaction elements
│   └── LoginPage.ts      # Auth selectors & methods
├── tests/                # Functional Test Suites
│   ├── tx.test.ts        # Transactional logic tests
│   ├── allocation.test.ts # Budgeting & percent logic
│   └── balances.test.ts   # Direct balance update tests
└── playwright.config.ts  # Global Settings & Parallelization
