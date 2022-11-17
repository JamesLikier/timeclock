const tc = {};
(function (tc) {
    const callbacks = {};
    function registerCallback(key,fn) {
        callbacks[key] = fn;
    }
    function apiCall(url, data = {}, callback) {
        fetch(url, data)
        .then(r => r.json())
        .then(r => callback(r));
    }
    document.addEventListener('submit', e => {
        const form = e.target;
        const fd = new FormData(form);
        apiCall(form.action, {body: fd}, callbacks[form.dataset.callback]);
    });

    // User Auth Functions
    registerCallback("login", r => {
        if (r.success) {

        } else {

        }
    });
    // End User Auth Functions
})(tc);