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
                      <button type="button" class="btn btn-primary btn-sl btn-block" @click="getChartData()">Zufällige Verbindung suchen</button>
                  </div>
                  <div class="col-sm-auto" style="width: 49%">
                      <button type="button" class="btn btn-primary btn-sl btn-block" @click="copyConnectionToClipBoard()">Link zur Verbindung kopieren</button>
                  </div>
              </div>
              <div class="col-sm-auto" style="padding-bottom: 1em">
                  <form class="searchForm" v-on:submit.prevent="submitSearch()">
                      <input type="text" class="form-control" v-model="searchQuery" placeholder="Suche" @keyup="submitSearch()">
                  </form>
              </div>
              <div class="col-sm-auto" style="overflow-y:scroll; max-height: 50vh">
                  <ul class="list-group" id="connectionSearchResults" v-for="(key, value) in searchresults">
                      <button type="button" class="list-group-item list-group-item-action" @click="getChartData(value)">{{key}}</button>
                  </ul>
              </div>

          </div>
      </div>
      <!-- CARDS -->
      <div class="row" style="display: none;">
          <div class="col row">
              <!-- Card -->
              <div class="col-xl-4 col-md-4 mb-3">
                  <div class="card border-left-success shadow h-100 py-2">
                      <div class="card-body">
                          <div class="row no-gutters align-items-center">
                              <div class="col mr-2">
                                  <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Geringster Preis</div>
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conMinPrice">20,90€</div>
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
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conAvrgPrice">25,90€</div>
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
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conMaxPrice">45,90€</div>
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
                                  <div class="text-xs font-weight-bold text-dark text-uppercase mb-1">Tage bis zur Abfahrt</div>
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conDaysLeft">0</div>
                              </div>
                              <div class="col-auto"> <i class="fas fa-calendar-alt fa-2x text-gray-300"></i> </div>
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
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conSumPrices">10</div>
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
                                  <div class="h5 mb-0 font-weight-bold text-gray-800" id="conPriceJump">43,10€</div>
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
import Vue from 'vue'
import Router from 'vue-router'
export default {
    name: 'home',
    computed: {},
    data() {
        return {
            chart_name: "Bahnpreise",
            disclaimer: 'Diese Seite ist keine Seite der Deutschen Bahn oder eines anderen Bahn-Betreibers. Die aufgeführten Informationen sind unverbindlich und werden zu wissenschaftlichen Zwecken genutzt.',
            searchQuery: '',
            searchresults: {},
            id: null,
        }
    },
    methods: {
        submitSearch() {
            axios.get(this.apiUrl + '/connections/getallconnections').then(response => {
                let result = response.data;
                this.searchresults = {};
                for (let i = 0; i < result.data.length; i++) {
                    let obj = result.data[i];
                    if (typeof obj === 'undefined'){
                        continue;
                    }
                    let name = obj.start + " -> " + obj.end + " @ " + obj.starttime;
                    if (name.toLowerCase().includes(this.searchQuery.toLowerCase())){
                        this.searchresults[obj.connection_id] = name;
                    }
                }
            });
        },
        removeSearchQuery: function () {
            //Make remove button more pretty
            this.searchQuery = '';
            this.searchresults = {};
        },
        getChartData: function (connection_id = null) {
            if (connection_id === null) {
                axios.get(this.apiUrl + '/connections/getrandomconnection').then(response => {
                    this.data = response;
                    this.renderChart();
                });
            } else {
                let axiosparams = new URLSearchParams();
                axiosparams.append('connection_id', connection_id);
                axios.get(this.apiUrl + '/prices', {params: axiosparams}).then(response => {
                    this.data = response;
                    this.renderChart();
                });
            }
            this.data.data.data.prices_days_to_departure
        },
        copyConnectionToClipBoard: function() {
            console.log(this.id);
            this.id.setAttribute('type', 'text');
            this.id.select();
            document.execCommand('copy');
        },
        renderChart: function () {
            // Set new default font family and font color to mimic Bootstrap's default styling
            Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
            Chart.defaults.global.defaultFontColor = '#858796';

            let dates = []; //Dates
            let dates_detailed = []; //Dates with descriptions (e.g. "Tage vor Abfahrt")
            let prices = []; //Price array - in same order as dates and dates_detailed

            //Extract dates from key => value dict/hash
            $.each(this.data.data.data.prices_days_to_departure, function (index, value) {
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
                prices.push(this.data.data.data.prices_days_to_departure[dates[i]]);
            }

            //End of building the arrays for the chart
            this.chart_name = this.data.data.data.start + " -> " + this.data.data.data.end + " @ " + this.data.data.data.starttime;

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
        if (this.$route.params.id !== undefined){
            this.getChartData(this.$route.params.id);
        } else {
            this.getChartData();
        }
    },
}
</script>
