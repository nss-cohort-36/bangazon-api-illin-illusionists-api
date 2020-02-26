# Bangazon API
&copy; 2020 - Sophia Hoffman, Melody Stern, Guy Cherkesky, Jesie Oldenburg, Ryan Bishop  

*Built using Python/Django REST framework*  

## Installation
1. Clone this repo and `cd` into the directory it creates
1. From the root folder, run `python -m venv bangazonEnv` to create the virtual environment
1. Activate the virtual env using one of the following commands:  
 `source ./bangazonEnv/bin/activate` (Mac)  
 `source ./bangazonEnv/Scripts/activate` (PC)  
1. Install dependencies using `pip install -r requirements.txt`
1. Run `python manage.py makemigrations`
1. Run `python manage.py migrate` to create base table schema

## Running the Server
1. From the root folder, run `python manage.py runserver`
1. Navigate to `http://127.0.0.1:8000/` to view the Browsable API

## Loading Test Data
1. From the root folder, run `python manage.py loaddata bangazonAPI/fixtures/bangazon.json`

## Browsing the API
1. You have the following endpoints available:
```sh
/customers
/products
/orderproducts
/orders
/paymenttypes
/producttypes
```
2. In the browsable API, click on any of the interactive URLs to see the respective data