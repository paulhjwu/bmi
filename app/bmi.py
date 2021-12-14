from flask import Blueprint, render_template, request, jsonify

from app import db, dbd

from flask_login import current_user

from datetime import datetime, timedelta

import csv
import io
import math

bmi = Blueprint('bmi', __name__)

class BMI(db.Document):
    
    meta = {'collection': 'readings'}
    name = db.StringField(max_length=30)
    date = db.DateTimeField()
    weight = db.FloatField()
    height = db.FloatField()
    bmi = db.FloatField()
    
    def computeBMI(self, unit):
        
        if unit == 'm':
            bmi = self.weight / math.pow(self.height, 2)
        else:
            bmi = self.weight / math.pow(self.height/100, 2)
        
        return bmi
        

def csv_to_dict(file):
    
    # input_file = csv.DictReader(open(file))
    # file.close
    # return input_file

    data = file.read().decode('utf-8')
    dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
    file.close()
    return(list(dict_reader))
    
    # with data as read_obj:
    #     # pass the file object to DictReader() to get the DictReader object
    #     dict_reader = csv.DictReader(read_obj)
    #     # get a list of dictionaries from dct_reader
    #     list_of_dict = list(dict_reader)
    #     # print list of dict i.e. rows
    #     file.close()
    #     return list_of_dict

def storeReadings(data, db):
    
    readings = {}
    fDate = datetime(3000, 1, 1)
    lDate = datetime(2000, 12, 31)

    for item in data:

        parts = [int(x) for x in item['Date'].split('-')]
        myDate = datetime(parts[0], parts[1], parts[2])

        if myDate <= fDate:
            fDate = myDate

        if myDate >= lDate:
            lDate = myDate
        
        BMI(name=item['User'], date=myDate, bmi=item['BMI']).save()
        if readings.get(item['User']):
            readings[item['User']].append([item['Date'], item['BMI']])            
        else:
            readings[item['User']] = [[item['Date'], item['BMI']]]
        
    dbd.readings.insert_one({"readings": readings, "fDate": fDate, "lDate": lDate})

def dataPrep(readings, bDate, lDate):
    
    chartDim = {}
    labels = []

    start_date = bDate
    end_date = lDate
    delta = timedelta(days=1)

    while start_date <= end_date:

        month = str(start_date.month) # months from 1-12
        day = str(start_date.day)
        year = str(start_date.year)

        aDateString = year + "-" + month + "-" + day
        labels.append(aDateString);

        for key, values in readings.items():

            if not chartDim.get(key):
                chartDim[key]=[];   
          
            filled = False

            for item in values:

                parts=[ int(x) for x in item[0].split('-') ]
                mydate = datetime(parts[0], parts[1], parts[2]) 
                
                if mydate == start_date:
                    
                    chartDim[key].append(item[1])
                    filled = True

                else:

                    if mydate > start_date:
                        if not filled:
                            chartDim[key].append(-1)
                        break

        start_date += delta

    return chartDim, labels

def getAverage(db):

    aveDict = {}
    sum=0
    count=0
    resCursor = db.readings.find({})  
    readings = resCursor[0]["readings"]
    
    for key, values in readings.items():

        for value in values:
            sum += float(value[1])
            count += 1
        
        aveDict[key]=sum/count
    
    return aveDict

@bmi.route('/chart2', methods=['GET', 'POST'])
def chart2():
    # return render_template('BMI_Chart.html')
    if request.method == 'GET':
            #I want to get some data from the service
        return render_template('BMI_Chart2.html', name=current_user.name, panel="BMI Chart")    #do nothing but to show index.html

    elif request.method == 'POST':

        #Get the values passed from the Front-end, do the BMI calculation, return the BMI back to front-end
        # f1 = open("static/DataSet2.csv", "r")
        #listOfDict = csv_to_dict(f1)

        dbCursor = dbd.readings.find({})

        readings = {}
        fDate = datetime.now()
        lDate = datetime.now()

        #readings, bDate, lDate = getReadings(listOfDict)
        readings = dbCursor[0]["readings"]
        fDate = dbCursor[0]["fDate"]
        lDate = dbCursor[0]["lDate"]

        chartDim = {}
        labels = []

        chartDim, labels = dataPrep(readings, fDate, lDate)

        #print(chartDim, labels)

        return jsonify({'chartDim': chartDim, 'labels': labels})

@bmi.route('/chart3', methods=['GET', 'POST'])
def chart3():
    # return render_template('BMI_Chart.html')
    if request.method == 'GET':
            #I want to get some data from the service
        return render_template('BMI_Chart3.html', name=current_user.name, panel="BMI Chart")    #do nothing but to show index.html

    elif request.method == 'POST':

        #Get the values passed from the Front-end, do the BMI calculation, return the BMI back to front-end
        # f1 = open("static/DataSet2.csv", "r")
        #listOfDict = csv_to_dict(f1)

        #db2 = connection['bmi']
        aveDict = getAverage(dbd)

        return jsonify({'averages': aveDict})
    
@bmi.route('/process',methods= ['POST'])
def process():

    weight  = float(request.form['weight'])
    height = float(request.form['height'])

    toDay = datetime.now()
    aBmi = BMI(name=current_user.name, date=toDay, weight=weight, height=height)
    aBmi.bmi = aBmi.computeBMI(request.form['unit'])
    aBmi.save()
    
    if request.form['unit'] == 'm':
        bmi = weight / math.pow(height, 2)
    else:
        bmi = weight / math.pow(height/100, 2)

    return jsonify({'bmi' : bmi})

@bmi.route('/chart')
def chart():
    # return render_template('BMI_Chart.html')
    return render_template('BMI_Chart.html', name=current_user.name, panel="BMI Chart")
