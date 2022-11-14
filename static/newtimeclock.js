const tc = {};
(function (tc) {
    tc.SUCCESS = "success";
    tc.FAIL = "fail";
    tc.accessToken = null;
    function apiCall(url, data = {}, callback) {
        data.accessToken = tc.accessToken;
        fetch(url, data)
        .then(r => r.json())
        .then(r => callback(r));
    }

    // Display Layer Stack
    
    // End Display Layer Stack

    // User Auth Functions
    tc.login = function (username, password) {
        apiCall(
            "/api/login",
            data = {
                method: "POST",
                body: JSON.stringify({ username: username, password: password })
            },
            r => {
                if (r.result == tc.SUCCESS) {
                } else {
                }
            }
        );
    }
    tc.logout = function () {
        apiCall(
            "/api/logout",
            data = {
                method: "POST"
            }
        );
    }
    // End User Auth Functions

    // Views

    // End Views
})(tc);