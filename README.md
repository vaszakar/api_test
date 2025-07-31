# API Test Automation Framework for Petstore

This is a sample project demonstrating a test automation framework for the [Swagger Petstore API](https://petstore.swagger.io/).

## 🚀 Technologies Used

* **Language:** Python 3.11
* **Test Runner:** pytest
* **HTTP Client:** requests
* **CI/CD:** GitHub Actions

## ✨ Features

* Clear separation of layers (API clients, tests, configuration).
* Positive and negative test cases.
* Use of pytest fixtures for test setup and teardown.
* Automated test execution via GitHub Actions.

## ⚙️ How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/vaszakar/api_test.git](https://github.com/vaszakar/api_test.git)
    cd api_tester
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run tests:**
    ```bash
    pytest
    ```