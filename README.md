
# Expense Application [CM 3050 Mobile Development] - Backend

Expense application backend is created using FastApi and SQL Model under the hood.






### Run Locally

Go to the project directory

```bash
  cd backend/expense_app
```

Install dependencies

```bash
  poetry install
```

Start the server

```bash
  poetry run uvicorn ExpenseApp.main:app --reload
```
__It is assumed that Poetry is already installed in the system. If it is not installed then please follow the installation guide from official documentation before executing the above commands. [Peotry Installation](https://python-poetry.org/docs/#installation)__

Alternative procedure to run using __PIP__

Create a virtual envoirnment

```bash
  python -m venv expense_app
```

Go to the project directory

```bash
  cd my-project [It should be /expense_app or any preceding directory]
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn ExpenseApp.main:app --reload
```


[FastApi - Official Documentation](https://fastapi.tiangolo.com/)__

### Database

Database (sqlite3) is also included for ease to refer the existing data already created while testing the application. You can access the user **test1** with the following credentials:

- **Username**: test1
- **Passwrod**: test1 

New users could be easily created using the signup screen from the front end and user specific expense/income transaction could also be posted once user is created and backend is live on a local host.
### Demo



