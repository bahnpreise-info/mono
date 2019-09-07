$(function() {
  searchBoxListener();
  bahnapi = new api();

  //Initial content switching based on URL
  variables = getQueryVariables();
  if (variables["site"] == null){
    switchContent("main");
  } else {
    switchContent(variables["site"]);
  }

  var data = bahnapi.get('/stats', {})["data"];
  $("#totalConnections").text(data["connections"]);
  $("#activeConnections").text(data["activeconnections"]);
  $("#stations").text(data["stationcount"]);
  $("#hourlyRequests").text(data["hourlyrequests"]);
  $("#dailyRequests").text(data["dailyrequests"]);
  $("#averageCosts").text(data["globalaverageprice"] + "€");

  //Draw a Demo chart (If nothing precise was requested
  if (variables["connection_id"] === null || variables["connection_id"] === undefined){
    drawPricechartForConnection(0, 'bahnPriceAreachart1', true);
  } else {
    drawPricechartForConnection(variables["connection_id"], 'bahnPriceAreachart1', false);
  }
});

function debounce(func, wait, immediate) {
  var timeout;

  return function executedFunction() {
    var context = this;
    var args = arguments;

    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };

    var callNow = immediate && !timeout;

    clearTimeout(timeout);

    timeout = setTimeout(later, wait);

    if (callNow) func.apply(context, args);
  };
}


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

function switchContent(content_id, parameters) {
  var pages = ["main", 'single_connection', 'imprint'];
  pages.splice( $.inArray(content_id, pages) ,1 );

  $.each(pages, function( i, val ){
    $(`#${val}`).hide();
  });

  $(`#${content_id}`).show();
  seturl(content_id);
}

function seturl(content_id, parameters = {}) {
  var params = "";
  $.each(parameters, function( index, value ) {
    params = index + "=" + value + "&";
  });
  window.history.pushState('Bahnpreise.info', 'Bahnpreise.info', '?site=' + content_id + "&" + params);
}

function getQueryVariables() {
  var variables = {};
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    variables[pair[0]] = pair[1];
  }
  return variables;
}

function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if (pair[0] == variable) {
      var value = pair[1].replace("#", "");
      return value;
    }
  }
  return null;
}

function searchBoxListener() {
  var input = $('input[id="connectionSearchBar"]');
  input.on('keyup change click', debounce(function () {
    var searchterm = $(this).val();
    if (searchterm.length <= 2) {
      return;
    }
    ShowConnections(searchterm)
  }, 200));
}

function ShowConnections(searchterm) {
  if (typeof connections == 'undefined') {
    bahnapi = new api();
    connections = bahnapi.get('/connections/getallconnections', {});
  }
  $("#connectionSearchResults").html("");

  for (var i = 0; i < connections["data"].length; i++) {
    var obj = connections["data"][i];
    if (typeof obj === 'undefined'){
      continue;
    }
    var name = getConnectionName(obj.start, obj.end, obj.starttime);
    if (name.toLowerCase().includes(searchterm.toLowerCase())){
      $("#connectionSearchResults").append(`<button type="button" class="list-group-item list-group-item-action" onclick="getConnectionData(${obj.connection_id});">${name}</button>`);
    }
  }
}

function getConnectionData(id) {
  drawPricechartForConnection(id, 'bahnPriceAreachart1', false);
}

function getConnectionName(start, end, starttime) {
  return start + " -> " + end + " @ " + starttime;
}
