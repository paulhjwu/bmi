function myFunction(num) {
  if (num == -1)
  	return null;
  else
  	return num;
}

var ctx = document.getElementById('myChart').getContext('2d');

$.ajax({
  url:"/chart2",
  type:"POST",
  data: {},
  error: function() {
      alert("Error");
  },
  success: function(data, status, xhr) {

    debugger
    
    var chartDim = {};
    
    var chartDim = data.chartDim;
    var xLabels = data.labels;

    var vLabels = [];
    var vData = [];

    let newValues =[]

    for (const [key, values] of Object.entries(chartDim)) {
      vLabels.push(key);
      let newValues = values.map(myFunction);
      debugger;
      vData.push(newValues);
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

}})
