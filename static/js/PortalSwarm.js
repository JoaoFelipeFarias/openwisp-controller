//<form id='controller-form' method='post' action='http://172.22.254.254:8002?zone=captive_analysis'>
//</form>

<script type="text/javascript">
	function verify_login(){
	    $.ajax({
				type: "POST",
				url: '/portal/login/',
				data: $('#login-signup-form').serialize(),
				success: function (msg){
	                console.log('user_access_success');
					$('#controller-form').append('<input type="hidden" id="form-username" name="auth_user" value="" />');
					var user = $('#id_auth_user').val();
					var password = $('#id_auth_pass').val();
					$('#form-username').val(user).val();
					$('#controller-form').append('<input type="hidden" id="form-password" name="auth_pass" value="" />');
					$('#form-password').val(password);
					$('#controller-form').append('<input id="button_submit" type="submit" name="accept" value="Continue" style="display:none; "/>' );
					$('#button_submit').trigger('click');
					console.log('after submit');

				},
				error: function(msg){
					console.log('error sending user access');
				},
			});
}
</script>