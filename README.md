# Ecommerce Project

## Introduction

This project is an E-commerce project, allowing users to buy and sell products. The application is built with Django, Django REST Framework, HTML, CSS and uses external APIs for currency data.

## How to Use the Project

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/ShahdElmahallawy/ecommerce.git
   ```


2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```


3. **Apply Migrations and run the server:**

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

   Visit `http://localhost:8000` in your browser.

4. **To run the test:**

   ```bash
   pytest
   ```

5. **To see manage.py available commands:**
   ```bash
   python manage.py
   ```
   - There are some commands to seed the database with currency.

## Usage

- To use the site access `http://127.0.0.1:8000/app/`
- For the documentmentation of existing rest apis visit `http://127.0.0.1:8000/api/schema/swagger-ui/`
