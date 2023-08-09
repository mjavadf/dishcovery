
# Dishcovery: Recipe Sharing Platform

Dishcovery is a web-based Recipe Sharing Platform built using Django and Django Rest Framework. Users can create, explore, and interact with recipes, categories, and ratings.

## Features

- User registration and authentication.
- Recipe creation, editing, and deletion.
- Recipe categorization and tagging.
- Recipe rating and review system.
- User profiles and activity tracking.
- API endpoints for seamless integration.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dishcovery.git
   ```

2. Navigate to the project directory:
   ```sh
   cd dishcovery
   ```

3. Install project dependencies using Pipenv:
   ```sh
   pipenv install
   ```

4. Activate the virtual environment:
   ```sh
   pipenv shell
   ```

5. Apply database migrations:
   ```sh
   python manage.py migrate
   ```

6. Create a superuser for admin access:
   ```sh
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```sh
   python manage.py runserver
   ```

8. Access the application in your browser at `http://localhost:8000/`.

## Contributing

Contributions are welcome! If you find any bugs or want to add new features, feel free to fork the repository and submit a pull request.

---

Enjoy exploring and sharing delicious recipes with Dishcovery!
