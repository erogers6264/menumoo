<html>
<head>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
    <script src="https://apis.google.com/js/client:platform.js?onload=start" async defer></script>
</head>

<body>
<script>

    function sendTokenToServer() {
        var access_token = FB.getAuthResponse()['accessToken'];
        console.log('Welcome! Fetching your access token... ');
        console.log(access_token);
        FB.api('/me', function(response) {
            console.log('Successful login for: ' + response.name);
            $.ajax({
                type: 'POST',
                url: '/fbconnect?state={{ state }}',
                processData: false,
                data: access_token,
                contentType: 'application/octet-stream; charset=utf-8',
                success: function(result) {
                    // Handle or verify the server response if necessary.
                    if (result) {
                        $('#result').html('Login Successful!<br>' + result + '<br>Redirecting...')
                        setTimeout(function() {
                            window.location.href = "/restaurants";
                        }, 4000);
                    }
                }
            });
        });
    }
    window.fbAsyncInit = function() {
        FB.init({
            appId      : '198517123849971',
            cookie     : true,  // enable cookies to allow the server to access
                                // the session
            xfbml      : true,  // parse social plugins on this page
            version    : 'v2.4'
        });
        console.log('fb initialized dude')
    };

    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
</script>
<button>
    <fb:login-button scope="public_profile,email" onlogin="sendTokenToServer();">
    <a href="javascript:sendTokenToServer();">Login with Facebook</a>
    </fb:login-button>
</button>


<div id="signinButton">
    <span class="g-signin"
        data-scope="openid email"
        data-clientid="1074516546873-bm6s3j47kv22s2rkpls8jntd1623hjo3.apps.googleusercontent.com"
        data-redirecturi="postmessage"
        data-accesstype="offline"
        data-cookiepolicy="single_host_origin"
        data-callback="signInCallback"
        data-approvalprompt="force">
    </span>
</div>
<div id="result"></div>

<script>
function signInCallback(authResult) {
    if (authResult['code']) {
        // Hide the sign-in button now that the user is authorized,
        $('#signinButton').attr('style', 'display: none');

        // Send the one-time-use code to the server, if the server responds,
        // write a 'login successful' message to the web page and then
        // redirect back to the main restaurants page
        $.ajax({
            type: 'POST',
            url: '/gconnect?state={{state}}',
            processData: false,
            contentType: 'application/octet-stream; charset=utf-8',
            data: authResult['code'],
            success: function (result) {
                if (result) {
                    $('#result').html('Login successful!</br>' + result + '</br>Redirecting...')
                    setTimeout(function() {
                        window.location.href = "/restaurants";
                    }, 4000);
                } else if (authResult['error']) {
                    console.log('There was an error: ' + authResult['error']);
                }
            }
        });
    }
}
</script>
</body>
</html>
