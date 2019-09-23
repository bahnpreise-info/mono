// Set new default font family and font color to mimic Bootstrap's default styling


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
