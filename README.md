# Bangazon API
&copy; 2020 - Sophia Hoffman, Melody Stern, Guy Cherkesky, Jesie Oldenburg, Ryan Bishop  

Built using Python/Django REST framework  

## Installation
1. Clone this repo and `cd` into the directory it creates
1. From the root folder, run `python -m venv bangazonEnv` to create the virtual environment
1. Activate the virtual env:  
 `source ./bangazonEnv/bin/activate` (Mac)  
 `source ./bangazonEnv/Scripts/activate` (PC)  
1. Install dependencies using `pip install -r requirements.txt`
1. Run `python manage.py migrate` to create base table schema

## Running the Server
1. From the root folder, run `python manage.py runserver`
1. Navigate to `http://127.0.0.1:8000/` to view the Browsable API

<!-- TODO: loading fixtures (maybe?) -->
<!-- TODO: instructions for testing endpoints -->
## Testing the API
1. You have the following endpoints available
```sh
/customer
/product
/orderproduct
/order
/paymenttype
/producttype
```