var api = function(access_token){

  this.construct = function(){
  };

  this.get = function(endpoint, formData){
    var result = null;
    var url = `https://api.bahnpreise.info${endpoint}`;
    console.log("GET " + endpoint);
    console.log(formData);
    $.ajax({
      url: url,
      crossDomain: true,
      dataType: "JSON",
      data: formData,
      type: "GET",
      encode : true,
      async: false,
      success: function(response, status, xhr) {
        console.log("Status: " + status);
        console.log(response);
        result = response;
      },
      error: function (response, status, xhr) {
        console.log("Status: " + status);
      }
    });
    return result;
  };

  this.construct();
};
