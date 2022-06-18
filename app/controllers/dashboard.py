from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

import csv
import io

from models.bmidaily import BMIDAILY
from models.chart import CHART

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/chart2', methods=['GET', 'POST'])
def chart2():
    if request.method == 'GET':
            #I want to get some data from the service
        return render_template('bmi_chart2.html', name=current_user.name, panel="BMI Chart")    #do nothing but to show index.html
    elif request.method == 'POST':
        
        # To populate the CHART database first using BMIDAILY database
        listOfDict=[]  
            
        #Chart is indexed by first date and last date
        #And we are going to plot the period from 2021-01-17 to 2021-01-23
        fDate = datetime(2021,1,17,0,0)
        lDate = datetime(2021,1,23,0,0) 
        chartobjects=CHART.objects(fdate=fDate, ldate=lDate)
        
        for item in BMIDAILY.objects():
            #existing_user = User.objects(email=item['User_email']).first()
            measure_date=item['date']
            if fDate <= measure_date <= lDate:
                bmi=item['averageBMI']
                listOfDict.append({'Date': measure_date, 'User': item.user.name, 'BMI':bmi})
        
        a_chart = CHART(fdate=None, ldate=None, readings=None).save()
        a_chart.insert_reading_data_into_database(listOfDict)
        
        if len(chartobjects) >= 1:
            
            readings = {}

            #readings, bDate, lDate = getReadings(listOfDict)
            readings = chartobjects[0]["readings"]
            fDate = chartobjects[0]["fdate"]
            lDate = chartobjects[0]["ldate"]

            chartDim = {}
            labels = []
            chartDim, labels = chartobjects[0].prepare_chart_dimension_and_label()
            print(chartDim)
            
            return jsonify({'chartDim': chartDim, 'labels': labels})

# it is possible to use pluggable view
# @dashboard.route('/chart2', methods=['GET', 'POST'])
# def chart2():
#     if request.method == 'GET':
#             #I want to get some data from the service
#         return render_template('bmi_chart2.html', name=current_user.name, panel="BMI Chart")    #do nothing but to show index.html
#     elif request.method == 'POST':
#         print("reach here?")
#         # To populate the CHART database first using BMIDAILY database
#         listOfDict=[]      
        
#         fDate = datetime(2021,1,17,0,0)
#         lDate = datetime(2021,1,23,0,0) 
#         #Chart is indexed by first date and last date
#         #And we are going to plot the pre-set fixed period from 2021-01-17 to 2021-01-23
#         #As DataSet2.csv has this range
        
#         CHART.objects(fdate=fDate, ldate=lDate).delete()
                         
#         for item in BMIDAILY.objects():
#             #existing_user = User.objects(email=item['User_email']).first()
#             measure_date=item['date']
#             if fDate <= measure_date <= lDate:
#                 bmi=item['averageBMI']
#                 listOfDict.append({'Date': measure_date, 'User': item.user.name, 'BMI':bmi})
        
#         a_chart = CHART(fdate=None, ldate=None, readings=None).save()
#         a_chart.insert_reading_data_into_database(listOfDict)
        
#         chartobjects=CHART.objects(fdate=fDate, ldate=lDate)
#         print(chartobjects)
#         print(len(chartobjects))
#         if len(chartobjects) >= 1:
#             print(chartobjects)
#             print("=======================================")
#             readings = {}

#             #readings, bDate, lDate = getReadings(listOfDict)
#             readings = chartobjects[0]["readings"]
#             fDate = chartobjects[0]["fdate"]
#             lDate = chartobjects[0]["ldate"]

#             chartDim = {}
#             labels = []
#             chartDim, labels = chartobjects[0].prepare_chart_dimension_and_label()
            
#             return jsonify({'chartDim': chartDim, 'labels': labels})

@dashboard.route('/chart3', methods=['GET', 'POST'])
def chart3():
    if request.method == 'GET':
        #I want to get some data from the service
        return render_template('bmi_chart3.html', name=current_user.name, panel="BMI Chart")    #do nothing but to show index.html
    
    elif request.method == 'POST':
    
        #Get the values passed from the Front-end, do the BMI calculation, return the BMI back to front-end
        fDate = datetime(2021,1,17,0,0)
        lDate = datetime(2021,1,23,0,0) 
        chartobjects=CHART.objects(fdate=fDate, ldate=lDate)
        print(chartobjects)
        if len(chartobjects) >= 1:
            aveDict = chartobjects[0].get_average()
            print(aveDict)
            print("---------------------------------------------")
            print(jsonify({'averages': aveDict}))
        
        return jsonify({'averages': aveDict})
   
@dashboard.route('/dashboard')
@login_required
def render_dashboard():
    return render_template('dashboard.html', name=current_user.name, panel="Dashboard")


@dashboard.route('/chart')
@login_required
def chart():
    return render_template('bmi_chart.html', name=current_user.name, panel="BMI Chart")
