$(function() {

    chilliController.host = $('#controller_ip').val();
    var template_name = $('#template_name').val();
    var template_name = $('#').val();
    console.log(chilliController.host);
    console.log(template_name);



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

    $('#msform').validate({
           rules: {
                  username :  {
                        required: true,
                        minlength: 2
                        },
                  auth_user :  {
                        required: true,
                        minlength: 2
                        },
                  auth_pass :  {
                        required: true,
                        minlength: 2
                        },
                  password1 : {
                        required: true
                        },
                  password2 : {
                        equalTo: '#auth_pass'
                        },
                },
           messages:{
                  username :  {
                      required:'Por gentileza, preencha o campo.',
                      minlength: 'O nome de usuário deverá ter mais de dois caracteres.'
                      },
                  auth_user : {
                      required: 'Por gentileza, preencha o campo.',
                      minlength: 'O nome de usuário deverá ter mais de dois caracteres.',
                      },
                  auth_pass : {
                      required: 'Por gentileza, insira sua senha.'
                      },
                  password1 : {
                      required: 'Por gentileza, insira sua senha'
                      },
                  password2 : {
                      equalTo: 'As senhas devem coincidir'
                      },
           },
           submitHandler : function (form){
                $.ajax({
                        type: "POST",
                        url: '/portal/' + template_name + '/',
                        data: $('#msform').serialize(),
                        success: function(msg){
                           console.log(msg);
                           //alert(chilliController.clientState);
                           console.log('success');
                           login_coova();
                           console.log(chilliController.clientState);


                        },
                        error: function(msg){
                        console.log(msg);
                        console.log(msg.status);
                            if (msg.status == 404){
                                console.log('entrei 404');
                                $('#controller-form').append('<p> '+ msg.responseText + '<p/>');
                            }

                        },
                    });
           }

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