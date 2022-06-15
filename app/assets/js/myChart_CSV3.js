var ctx = document.getElementById('myChart').getContext('2d');

$.ajax({
  url:"/chart3",
  type:"POST",
  data: {},
  error: function() {
      console.log("hello")  
      // console.log(error)
      alert("Error");
  },

  success: function(data, status, xhr) {

    debugger

    var averages = data.averages;
    var vLabels = [];
    var vData = [];

    for (const [key, values] of Object.entries(averages)) {
      vLabels.push(key);
      vData.push(values);
    } 

    var myChart = new Chart(ctx, {
      data: {
      labels: vLabels,
      datasets: []
      },
      options: {
          responsive: false
      }
    });

    debugger
    myChart.data.datasets.push({
    label: "Average",
    type: "bar",
    borderColor: '#'+(0x1ff0000+Math.random()*0xffffff).toString(16).substr(1,6),
    borderColor: '#'+(0x1100000+Math.random()*0xffffff).toString(16).substr(1,6),
    backgroundColor: "rgba(249, 238, 236, 0.74)",
    data: vData,
    spanGaps: true
    });
    myChart.update();
    }

})
