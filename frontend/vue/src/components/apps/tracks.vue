<template>
  <div>
      <div class="alert alert-danger col" role="alert">
          {{disclaimer}}
      </div>
      <div class="row">
          <div class="col-xl-9">
              <!-- Chart -->
              <div class="card shadow mb-4">
                  <div class="card-header py-3">
                      <h6 class="m-0 font-weight-bold text-primary" id="chart_name">{{chart_name}}</h6> </div>
                  <div class="card-body card-nopadding">
                      <div class="chart-area" id="bahnPriceAreachart1Top">
                          <canvas id="bahnPriceAreachart1"></canvas>
                      </div>
                  </div>
              </div>
          </div>
          <!-- Search beside chart -->
          <div class="col-xl-3">
              <div class="row" style="padding-bottom: 1em">
                  <div class="col-sm-auto" style="width: 49%">
                      <button type="button" class="btn btn-primary btn-sl btn-block" @click="setChartData()" style="background-color: #d10e0e">Zufällige Strecke auswählen</button>
                  </div>
                  <div class="col-sm-auto" style="width: 49%">
                      <button type="button" class="btn btn-primary btn-sl btn-block" v-clipboard:copy="track_url" style="background-color: #f50202">Link zur Strecke kopieren</button>
                  </div>
              </div>
              <div class="col-sm-auto" style="padding-bottom: 1em">
                  <form class="searchForm" v-on:submit.prevent="submitSearch()">
                      <input type="text" class="form-control" v-model="searchQuery" placeholder="Suche" @keyup="submitSearch()">
                  </form>
              </div>
              <div class="col-sm-auto" style="overflow-y:scroll; max-height: 50vh">
                  <ul class="list-group" id="connectionSearchResults" v-for="(key, value) in searchresults">
                      <button type="button" class="list-group-item list-group-item-action" @click="setChartData(key['id'])">{{key["start"]}} -> {{key["end"]}}</button>
                  </ul>
              </div>

          </div>
      </div>
      <!-- CARDS -->
      <div class="row">
          <div class="col row">
              <!-- Card -->
              <div class="col-xl-4 col-md-4 mb-3">
                  <div class="card border-left-success shadow h-100 py-2">
                      <div class="card-body">
                          <div class="row no-gutters align-items-center">
                              <div class="col mr-2">
                                  <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Geringster Preis</div>
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conMinPrice">{{minimum}}€</div>
                              </div>
                              <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div>
                          </div>
                      </div>
                  </div>
              </div>
              <!-- Card -->
              <div class="col-xl-4 col-md-4 mb-3">
                  <div class="card border-left-warning shadow h-100 py-2">
                      <div class="card-body">
                          <div class="row no-gutters align-items-center">
                              <div class="col mr-2">
                                  <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Durchschnittlicher Preis</div>
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conAvrgPrice">{{average}}€</div>
                              </div>
                              <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div>
                          </div>
                      </div>
                  </div>
              </div>
              <!-- Card -->
              <div class="col-xl-4 col-md-4 mb-3">
                  <div class="card border-left-primary shadow h-100 py-2">
                      <div class="card-body">
                          <div class="row no-gutters align-items-center">
                              <div class="col mr-2">
                                  <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Maximaler Preis</div>
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conMaxPrice">{{maximum}}€</div>
                              </div>
                              <div class="col-auto"> <i class="fas fa-coins fa-2x text-gray-300"></i> </div>
                          </div>
                      </div>
                  </div>
              </div>
              <!-- Card -->
              <div class="col-xl-4 col-md-4 mb-3">
                  <div class="card border-left-dark shadow h-100 py-2">
                      <div class="card-body">
                          <div class="row no-gutters align-items-center">
                              <div class="col mr-2">
                                  <div class="text-xs font-weight-bold text-dark text-uppercase mb-1">Gesammelte Datenpunkte</div>
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conSumPrices">{{datapoints}}</div>
                              </div>
                              <div class="col-auto"> <i class="fas fa-chart-bar fa-2x text-gray-300"></i> </div>
                          </div>
                      </div>
                  </div>
              </div>
              <!-- Card -->
              <div class="col-xl-4 col-md-4 mb-3">
                  <div class="card border-left-dark shadow h-100 py-2">
                      <div class="card-body">
                          <div class="row no-gutters align-items-center">
                              <div class="col mr-2">
                                  <div class="text-xs font-weight-bold text-dark text-uppercase mb-1">Größter Preissprung</div>
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conPriceJump">{{maximumpricejump_up}}€</div>
                              </div>
                              <div class="col-auto"> <i class="fas fa-arrows-alt-v fa-2x text-gray-300"></i> </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>'
  </div>
</template>
<script>
function number_format(number, decimals, dec_point, thousands_sep) {
    // *     example: number_format(1234.56, 2, ',', ' ');
    // *     return: '1 234,56'
    number = (number + '').replace(',', '').replace(' ', '');
    var n = !isFinite(+number) ? 0 : +number,
        prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
        sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
        dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
        s = '',
        toFixedFix = function(n, prec) {
            var k = Math.pow(10, prec);
            return '' + Math.round(n * k) / k;
        };
    // Fix for IE parseFloat(0.55).toFixed(0) = 0;
    s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

import axios from 'axios'
export default {
    name: 'home',
    computed: {},
    data() {
        return {
            chart_name: "Bahnpreise",
            disclaimer: 'Diese Seite ist keine Seite der Deutschen Bahn oder eines anderen Bahn-Betreibers. Die aufgeführten Informationen sind unverbindlich und werden zu wissenschaftlichen Zwecken genutzt.',
            searchQuery: '',
            searchresults: [],
            all_connections: [],
            track_url: "",
            prices: {},
            start: "",
            end: "",
            average: 0.0,
            maximum: 0.0,
            minimum: 0.0,
            datapoints: 0,
            maximumpricejump_up: 0.0,

        }
    },
    methods: {
        submitSearch() {
            if (this.searchQuery === ''){
                this.searchresults = [];
                return;
            }
            this.searchresults = [];
            for (let i = 0; i < this.all_connections.length; i++) {
                let obj = this.all_connections[i];
                if (typeof obj === 'undefined'){
                    continue;
                }
                let name = obj.start + " -> " + obj.end;
                if (name.toLowerCase().includes(this.searchQuery.toLowerCase())){
                    this.searchresults.push({id: i, start: obj.start, end: obj.end})
                }
            }
        },
        setChartData: function (id = null) {
            if (id === null) {
                id = Math.floor(Math.random() * this.all_connections.length);
                this.start = this.all_connections[id]["start"];
                this.end = this.all_connections[id]["end"];
            } else {
                this.start = this.all_connections[id]["start"];
                this.end = this.all_connections[id]["end"];
            }

            let axiosparams = new URLSearchParams();
            axiosparams.append('start', this.start);
            axiosparams.append('end', this.end);
            axios.get(this.apiUrl + '/connections/getaveragetrackprice', {params: axiosparams}).then(response => {
                this.prices = response.data.data.days_with_prices;
                this.maximum = response.data.data.maximum.toFixed(2);
                this.minimum = response.data.data.minimum.toFixed(2);
                this.average = response.data.data.average.toFixed(2);
                this.maximumpricejump_up = response.data.data.maximumpricejump_up.toFixed(2);
                this.datapoints = response.data.data.datapoints;
                this.renderChart();
            });
        },
        renderChart: function () {
            //When drawing a new chart we want to set the proper url to copy
            this.track_url = encodeURI("https://bahnpreise.info/#/tracks/" + this.start + "+" + this.end);

            // Set new default font family and font color to mimic Bootstrap's default styling
            Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
            Chart.defaults.global.defaultFontColor = '#858796';

            let dates = []; //Dates
            let dates_detailed = []; //Dates with descriptions (e.g. "Tage vor Abfahrt")
            let prices = []; //Price array - in same order as dates and dates_detailed

            //Extract dates from key => value dict/hash
            $.each(this.prices, function (index, value) {
                dates.push(index);
            });
            dates.sort(function (a, b) {
                return b - a
            });

            //Finally get Descriptors and values together
            for (var i = 0; i < dates.length; i++) {
                dates_detailed.push(dates[i] + " Tage");
            }

            for (var i = 0; i < dates.length; i++) {
                prices.push(this.prices[dates[i]]);
            }

            //End of building the arrays for the chart
            //Set chart name
            this.chart_name = this.start + " -> " + this.end;

            $("#bahnPriceAreachart1").remove();
            $("#bahnPriceAreachart1Top").html('<canvas id="bahnPriceAreachart1"></canvas>');

            //Start drawing chart
            let ctx = document.getElementById("bahnPriceAreachart1");
            new Chart(ctx, {
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
                                callback: function (value, index, values) {
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
                            label: function (tooltipItem, chart) {
                                var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
                                return datasetLabel + ': €' + number_format(tooltipItem.yLabel, 2);
                            }
                        }
                    }
                }
            });
        },
    },
    mounted() {
        axios.get(this.apiUrl + '/connections/getalltracks').then(response => {
            this.all_connections = response.data.data;
            if (this.$route.params.startendslug !== undefined){
                this.start = this.$route.params.startendslug.split('+')[0];
                this.end = this.$route.params.startendslug.split('+')[1];
                let axiosparams = new URLSearchParams();
                axiosparams.append('start', this.start);
                axiosparams.append('end', this.end);
                axios.get(this.apiUrl + '/connections/getaveragetrackprice', {params: axiosparams}).then(response => {
                    if (Object.keys(response.data.data.days_with_prices).length > 0){
                        this.prices = response.data.data.days_with_prices;
                        this.maximum = response.data.data.maximum.toFixed(2);
                        this.minimum = response.data.data.minimum.toFixed(2);
                        this.average = response.data.data.average.toFixed(2);
                        this.maximumpricejump_up = response.data.data.maximumpricejump_up.toFixed(2);
                        this.datapoints = response.data.data.datapoints;
                        this.renderChart();
                    } else{
                        this.setChartData();
                    }
                });
            } else {
                this.setChartData();
            }
        });
    },
}
</script>
