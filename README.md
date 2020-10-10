# Loan Calculator
By default, make sure to run commands in the ROOT directory of the project. 
 

<!-- ## Frontend setup
```
npm install
npm run build
``` -->

## Setup
Entering a python virtual environment (venv) beforehand is recommended.

Whether you're in a venv or not, start by installing the python dependencies:
```
pip install -r requirements.txt
```
### Database
You can generate a new SQLite database using the following commands from the root directory:
```
python manage.py migrate
```

### Frontend
You should find a `db.sqlite3` file in the project's root directory. 
That file serves as the project's database. 
Frontend Files
 You can build the frontend files by running these commands from the `/frontend` directory:
```
npm install
npm run build
```
Check the `/frontend/dist` directory for the frontend build files. You should find an `index.html` and its respective css and js folders there.

# Running the project
Enter this command from the root directory:
```
python manage.py runserver
```
The main page will be located in http://localhost:8000/

## API
While the server is running, the project's API can be found in http://localhost:8000/calculator/

### GET Requests
A blank GET request will have the API return a list of every loan inquiry saved in the database. e.g.
```
curl -x GET http://localhost:8000/calculator/
```
will yield an array of results:
```
[
    {
        "id": 3,
        "loan_type": "B",
        "principal_amount": "10850.30",
        "monthly_amortization": "1026.00",
        "total_interest": "1461.70",
        ...
        "inquirer": {
            "full_name": "Mori Jin"
            ...
        }
    },
    ...
]
```
Adding the `type` query parameter filters the list to the specified loan type. e.g.

```
curl -x GET http://localhost:8000/calculator/?type=B
```

### POST Requests
POST requests to the API will trigger its calculation functions and save the results to an SQLITE database. POST requests expect data in the form of a JSON with proper key names:
```
curl -x POST --data '{
	"loan_type": "B",
    "monthly_amortization": 945.6,
    "loan_term": 12,
    "loan_start_date": "2020-10-12"
}' -H 'Content-Type: application/json' http://localhost:8000/calculator/
```
A successfull calculation will return a JSON with extra key names filled with the calculated results:
```
{
    "loan_type": "B",
    "monthly_amortization": 945.6,
    "loan_term": 12,
    "loan_start_date": "2020-10-12",
    "principal_amount": 10000.042658499291,
    "sum_payments": 11347.2,
    "total_interest": 1347.1573415007097,
    "first_payment_date": "2020-11-07",
    "loan_maturity_date": "2021-10-07"
}
```
