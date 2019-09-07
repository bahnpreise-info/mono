// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function drawPricechartForConnection(id, chart_id, random=false) {
  //Get connection information + prices from API
  var data;
  if (random === false){
    data = bahnapi.get('/prices', {"connection_id": id});
    seturl("single_connection", {"connection_id": id});
  } else {
    data = bahnapi.get('/connections/getrandomconnection', {"connection_id": id});
  }

  var dates = []; //Dates
  var dates_detailed = []; //Dates with descriptions (e.g. "Tage vor Abfahrt")
  var prices = []; //Price array - in same order as dates and dates_detailed

  //Extract dates from key => value dict/hash
  $.each(data.data.prices_days_to_departure, function( index, value ) {
    dates.push(index);
  });
  dates.sort(function(a, b){return b-a});

  //Finally get Descriptors and values together
  for (var i = 0; i < dates.length; i++) {
    dates_detailed.push(dates[i] + " Tage");
  }

  for (var i = 0; i < dates.length; i++) {
    prices.push(data.data.prices_days_to_departure[dates[i]]);
  }

  //End of building the arrays for the chart
  var chart_name = getConnectionName(data.data.start, data.data.end, data.data.starttime);

  $(`#${chart_id}`).remove();
  $(`#${chart_id}Top`).html('<canvas id="bahnPriceAreachart1"></canvas>');

  $('#chart_name').text(chart_name);


  //Start drawing chart
  var ctx = document.getElementById("bahnPriceAreachart1");
  var myLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: dates_detailed,
      datasets: [{
        label: "Preis",
        lineTension: 0.3,
        backgroundColor: "rgba(209,14,14, 0.05)",
        borderColor: "#d10e0e",
        pointRadius: 3,
        pointBackgroundColor: "#d10e0e",
        pointBorderColor: "#d10e0e",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
        pointHoverBorderColor: "rgba(78, 115, 223, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: prices,
      }],
    },
    options: {
      elements: {
        line: {
          cubicInterpolationMode: "monotone"
        }
      },
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            maxTicksLimit: 5,
            padding: 10,
            // Include a dollar sign in the ticks
            callback: function(value, index, values) {
              return '€' + number_format(value, 2);
            }
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        borderColor: '#d10e0e',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        intersect: false,
        mode: 'index',
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': €' + number_format(tooltipItem.yLabel, 2);
          }
        }
      }
    }
  });


}
