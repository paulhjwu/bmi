var ctx = document.getElementById('myChart').getContext('2d');

//Read the data
var f = "static/js/DataSet1.2.csv";
// var f = "./Data35.csv";

function getReadings(data) {

  debugger

  var readings = {};
  var bDate = new Date(3000, 0, 1);
  var lDate = new Date(2000, 11, 31);

  for (let i = 0; i < data.length -1; i++) {

    var parts = data[i].date.split('-');
    var myDate = new Date(parts[0], parts[1]-1, parts[2]);

    if (myDate <= bDate) {
        bDate = myDate;
    }

    if (myDate >= lDate) {
        lDate = myDate;
    }
    
    if ( readings[data[i].group] != null ) {
        readings[data[i].group].push([data[i].date, data[i].value]);            
    } else {
        readings[data[i].group]=[[data[i].date, data[i].value]];
    }
    
  }

  // https://stackoverflow.com/questions/10221445/return-multiple-variables-from-a-javascript-function
  //debugger
  return [readings, bDate, lDate];

}

function dataPrep(readings, bDate, lDate) {

  var chartDim = {};
  var labels = [];

  for (var d = bDate; d <= lDate; d.setDate(d.getDate() + 1)) {

      var month = d.getUTCMonth() + 1; //months from 1-12
      var day = d.getUTCDate() + 1;
      var year = d.getUTCFullYear();

      //debugger
      var aDateString = year + "-" + month + "-" + day;
      labels.push(aDateString);

      for (const [key, value] of Object.entries(readings)) {

          debugger
          // https://stackoverflow.com/questions/455338/how-do-i-check-if-an-object-has-a-key-in-javascript 
          if (!(key in chartDim)) {
              chartDim[key]=[];
          }
          
          i = 0;

          let filled = false;

          //debugger
          for (const item of value) {

              let parts=item[0].split('-');
              let mydate = new Date(parts[0], parts[1] - 1, parts[2]); 
              if (+mydate === +d) {
                  debugger
                  console.log(`${key}:${item[1]}`);
                  chartDim[key].push(Number(item[1]));
                  filled = true;
              } else {
                  if (+mydate > +d) {
                      if (!filled) {
                          chartDim[key].push(null);
                      } 
                      break;
                  }
              }
          }
      }
  }

  return [chartDim, labels];
}


d3.csv(f,
  // When reading the csv, I must format variables:
  function(d){
    return { group : d.User, value : d.BMI, date: d.Date }
  },
  // Now I can use this dataset:
  function(data) {

    var bDate = new Date();
    var lDate = new Date();
    var readings = {};
    var labels = [];

    // https://stackoverflow.com/questions/10221445/return-multiple-variables-from-a-javascript-function
    var aData = getReadings(data);
    readings = aData[0];
    bDate = aData[1];
    lDate = aData[2];
    
    var chartDim = {};
    debugger
    var aData = dataPrep(readings, bDate, lDate);
    chartDim = aData[0];
    xLabels = aData[1];

    var vLabels = [];
    var vData = [];

    for (const [key, value] of Object.entries(chartDim)) {
      vLabels.push(key);
      vData.push(value);
    } 

    debugger
    var myChart = new Chart(ctx, {
      data: {
      labels: xLabels,
      datasets: []
      },
      options: {
          responsive: true,
          maintainaspectratio: false 
      }
    });

    debugger
    for (i= 0; i < vLabels.length; i++ ) {
      myChart.data.datasets.push({
      label: vLabels[i],
      type: "line",
      // borderColor: '#'+(0x1ff0000+Math.random()*0xffffff).toString(16).substr(1,6),
      borderColor: '#'+(0x1100000+Math.random()*0xffffff).toString(16).substr(1,6),
      backgroundColor: "rgba(249, 238, 236, 0.74)",
      data: vData[i],
      spanGaps: true
      });
      myChart.update();
    }

})
