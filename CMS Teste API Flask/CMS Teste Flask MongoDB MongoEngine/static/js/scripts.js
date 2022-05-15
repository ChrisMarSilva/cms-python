$("form[name=signup_form").submit(function(e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
  
    $.ajax({
      url: "/user/signup",
      type: "POST",
      data: data,
      dataType: "json",
      success: function(resp) {
        window.location.href = "/dashboard/";
      },
      error: function(resp) {
        $error.text(resp.responseJSON.error).removeClass("error--hidden");
      }
    });
  
    e.preventDefault();
  });
  
  $("form[name=login_form").submit(function(e) {
  
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();
  
    $.ajax({
      cache   : "false",
      async   : true,
      url: "/user/login",
      type: "post",
      dataType: "json",
      data: data,
      success: function(resp) {
        window.location.href = "/dashboard/";
      },
      error: function (request, status, error) { //  error: function(request) {
        if ((request.responseJSON != undefined) && (request.responseJSON != '')) {
          $error.text(request.responseJSON.error).removeClass("error--hidden");
        } else{
          $error.text(request.responseText).removeClass("error--hidden");
        }
      }
    });
  
    e.preventDefault();
  });
  
function adicionaZero(numero){
  if (numero <= 9) 
      return "0" + numero;
  else
      return numero; 
}

function adicionaZeros(numero){
  if (numero <= 9) 
  return "00" + numero;
  else if (numero <= 99) 
    return "0" + numero;
  else
    return numero; 
}

function get_logs() {
  
    var DivLogs = $("#logs");
    DivLogs.html( "" );
    
    $.ajax({
      cache   : "false",
      async   : true,
      url: "/user/logs",
      type: "get",
      dataType: "json",
      success: function(result) {
				content = '';
        const meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul","Ago","Set","Out","Nov","Dez"];
				$.each(result.logs, function (index, value) {
          let strDateISO = new Date(value.date)
          // let strDateFormatada = ((strDateISO.getDate() )) + "/" + ((strDateISO.getMonth() + 1)) + "/" + strDateISO.getFullYear();
          // let strDateFormatada = ((strDateISO.getDate() + "/" + meses[(strDateISO.getMonth())] +  "/" + strDateISO.getFullYear()));
          let strDateFormatada = 
            adicionaZero(strDateISO.getDate().toString()) + "/" + 
            adicionaZero(strDateISO.getMonth()+1).toString() + "/" + 
            strDateISO.getFullYear()+ " as " + 
            adicionaZero(strDateISO.getHours().toString()) + ":" + 
            adicionaZero(strDateISO.getMinutes().toString()) + ":" + 
            adicionaZero(strDateISO.getSeconds().toString()); // + "," + 
            // adicionaZeros(strDateISO.getMilliseconds().toString());
          content += '<span id="' + value.id +'">' + value.type.toString() +' \t\t ' + strDateFormatada +'</span> <br>';
				}); 
				//DivLogs.append( content );
        DivLogs.html( content );
      },
      error: function (request, status, error) { //  error: function(request) {
        console.log(request.responseText);
        if ((request.responseJSON != undefined) && (request.responseJSON != '')) {
          $error.text(request.responseJSON.error).removeClass("error--hidden");
        } else{
          $error.text(request.responseText).removeClass("error--hidden");
        }
      }
    });

 }