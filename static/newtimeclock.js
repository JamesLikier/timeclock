const tc = {};
(function (tc) {
    tc.SUCCESS = "success";
    tc.FAIL = "fail";
    tc.sessionToken = null;
    function apiCall(url, data = {}, callback) {
        data.sessionToken = tc.sessionToken;
        fetch(url, data)
        .then(r => r.json())
        .then(r => callback(r));
    }
    tc.login = function (username, password) {
        apiCall(
            "/api/login",
            data = {
            method: "POST",
            body: JSON.stringify({username: username, password: password})
            }, r => {
                if (r.result == tc.SUCCESS) {
                    tc.sessionToken = r.data;
                } else {
                    tc.sessionToken = null;
                }
            });
    }
})(tc);