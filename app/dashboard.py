from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from app import db

dashboard = Blueprint('dashboard', __name__)

class CHART(db.Document):  
    
    meta = {'collection': 'chart'}
    fdate = db.DateTimeField()
    ldate = db.DateTimeField()
    readings = db.DictField()
    
    def get_dict_from_csv(self, file):
        data = file.read().decode('utf-8')
        dict_reader = csv.DictReader(io.StringIO(data), delimiter=',', quotechar='"')
        file.close()
        return(list(dict_reader))

    def insert_reading_data_into_database(self, data):

        readings = {}
        # fDate = datetime(3000, 1, 1)
        # lDate = datetime(2000, 12, 31)
        fDate = datetime(3000, 1, 1)
        lDate = datetime(2000, 12, 31)

        for item in data:
            parts = [int(x) for x in item['Date'].split('-')]
            # myDate = datetime(parts[0], parts[1], parts[2])
            myDate = datetime(parts[0], parts[1], parts[2])

            if myDate <= fDate:
                fDate = myDate

            if myDate >= lDate:
                lDate = myDate
            
            # BMI(name=item['User'], date=myDate, bmi=item['BMI']).save()
            if readings.get(item['User']):
                readings[item['User']].append([item['Date'], item['BMI']])            
            else:
                readings[item['User']] = [[item['Date'], item['BMI']]]
            
        # dbd.readings.insert_one({"readings": readings, "fDate": fDate, "lDate": lDate})
        self.update(__raw__={'$set': {'readings': readings,'fdate': fDate, 'ldate': lDate}})
        
    def prepare_chart_dimension_and_label(self):

        chartDim = {}
        labels = []

        start_date = self.fdate
        end_date = self.ldate
        delta = timedelta(days=1)

        while start_date <= end_date:
            month = str(start_date.month) # months from 1-12
            day = str(start_date.day)
            year = str(start_date.year)

            aDateString = year + "-" + month + "-" + day
            labels.append(aDateString);

            for key, values in self.readings.items():
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

    def get_average(self):
        aveDict = {}
        sum=0
        count=0
        # resCursor = db.readings.find({})  
        readings = self["readings"]
        
        for key, values in readings.items():
            for value in values:
                sum += float(value[1])
                count += 1

            aveDict[key]=sum/count

        return aveDict

# it is possible to use pluggable view
@dashboard.route('/chart2', methods=['GET', 'POST'])
def chart2():
    if request.method == 'GET':
            #I want to get some data from the service
        return render_template('bmi_chart2.html', name=current_user.name, panel="BMI Chart")    #do nothing but to show index.html
    elif request.method == 'POST':
        #Chart is indexed by first date and last date
        #And we are going to plot the period from 2021-01-17 to 2021-01-23
        fDate = datetime(2021,1,17,0,0)
        lDate = datetime(2021,1,23,0,0) 
        chartobjects=CHART.objects(fdate=fDate, ldate=lDate)
        
        if len(chartobjects) >= 1:
            
            readings = {}

            #readings, bDate, lDate = getReadings(listOfDict)
            readings = chartobjects[0]["readings"]
            fDate = chartobjects[0]["fdate"]
            lDate = chartobjects[0]["ldate"]

            chartDim = {}
            labels = []
            chartDim, labels = chartobjects[0].prepare_chart_dimension_and_label()
            return jsonify({'chartDim': chartDim, 'labels': labels})

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
        if len(chartobjects) >= 1:
            aveDict = chartobjects[0].get_average()
            return jsonify({'averages': aveDict})
   
@dashboard.route('/dashboard')
@login_required
def render_dashboard():
    return render_template('dashboard.html', name=current_user.name, panel="Dashboard")


@dashboard.route('/chart')
@login_required
def chart():
    return render_template('bmi_chart.html', name=current_user.name, panel="BMI Chart")
