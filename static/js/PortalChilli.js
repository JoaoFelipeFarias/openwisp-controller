$(function() {

    authenticate_client_on_load = $("#login_coova_input").val();
    console.log(authenticate_client_on_load);

    chilliController.host = $('#controller_ip').val();
    //var template_name = $('#template_name').val();
    //var template_name = $('#').val();
    console.log(chilliController.host);
    console.log(template_name);
    var current_url = $("#current_url").text();
    current_url = current_url.split("/")[2];
    console.log(current_url);

    // coova elcoma page modifications
    if (authenticate_client_on_load == 'True')
    {
        console.log('authenticating client')
        username = $('#username').val();
        password = $('#password').val();
        console.log('username:' + username + 'password:' + password)
        chilliController.refresh()
        chilliController.logon(username,password);

//        document.getElementById("client_state").innerHTML = "value is " + chilliController.clientState;
//        //$('#client_state').val('value is ' + chilliController.clientState);
//        $('#client_state').show();

    } else if (authenticate_client_on_load == 'False'){
        console.log('do not authenticate client on load');
        url_params = $('#urlparams').val();
        host = window.location.hostname;
        port = window.location.port;
        console.log('http://' + host + ':' + port + '/portal/login/' + url_params);
        window.location.replace('http://' + host + ':' + port + '/portal/login/' + url_params);

    }


    //getting the csrf token for ajax POST requests
    var csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    $("#msform").submit(function(event) {
    event.preventDefault();
    console.log('calling form')


    $.ajax({
                        type: "POST",
                        //url: '/portal/' + template_name + '/',
                        url: '/portal/' + current_url + '/',
                        data: $('#msform').serialize(),
                        success: function(msg){
                           console.log(msg);
                           //alert(chilliController.clientState);
                           console.log('success login on server');
                           login_coova();
//                           register_connection();
                           console.log(chilliController.clientState);

                        },
                        error: function(msg){
                        console.log(msg);
                        console.log(msg.status);
                            if (msg.status == 404){
                                console.log('entrei 404');
                                $('#controller-form').append('<p> '+ msg.responseText + '<p/>');
                            }
                         }
    });
});

    console.log(chilliController.host)

    function login_coova() {
        console.log('realizando login');
        var username =  $('#auth_user').val();
        var password =  $('#auth_pass').val();
        var obj = chilliController.logon(username,password);

    }


    chilliController.onUpdate = updateUI;

    function updateUI(){
          console.log('update status');
          console.log(chilliController.clientState)
          if(chilliController.clientState == 1){ //if client logged on successfully, go to redirect_url{
            redirect_url = $('#redirect_url').val();
            window.location.replace(redirect_url);
          }
    }

    function handleErrors ( code ) {
            console.log( 'The last contact with the Controller failed. Error code =' + code );
    }

    function logout_coova(){
        chilliController.logoff();
    }
});


