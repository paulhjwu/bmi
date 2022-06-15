# BMI

This is an example flask app for ICT 239 - web programming for SUSS.

# Student Details
> Student Name: 
> Student ID: 

# Getting started
```
cd app
export FLASK_APP=app.py; export PYTHONPATH=.; export FLASK_ENV=development
flask run
```


## FAQ

1. The backend chart is producing an error when I load the page. 

A. First, check if you have a MongoDB connection. Next, does your database contains the necessary data? If not, you will need to upload dataset2.csv from `assets/js/` before the backend chart will work. 

2. Populating the chart collection with /populate
> This is needed for the chart2 & chart3 to work