# BMI

This is a example flask app for ICT 239 - web programming for SUSS.

# Getting started
```
cd app
export FLASK_APP=app.py; export PYTHONPATH=.; export FLASK_ENV=development
flask run
```


## FAQ

1. The backend chart is producing error when I load the page. 

A. First, check if you have a mongoDB connection. Next, does your database contains the necessary data? If not, you will need to upload dataset2.csv from `assets/js/` before the backend chart will work. 
