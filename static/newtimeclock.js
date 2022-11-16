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

    // Display Layer Stack
    // End Display Layer Stack

    // User Auth Functions
    // End User Auth Functions

    // Views
    // End Views
})(tc);