function flatten(o) {
    s = o.toString() + '<br>';
    for (k in o) {
        s += `${k}=${o[k]}<br>`;
    }
    return s;
}
const tc = {};
(function (tc) {
    const content = document.querySelector("#content");
    const callbacks = {};
    const actions = {};
    function registerCallback(key,fn) {
        callbacks[key] = fn;
    }
    function registerAction(key,fn) {
        actions[key] = fn;
    }
    function apiCall(url, data = {}, callback) {
        fetch(url, data)
        .then(r => r.json())
        .then(r => callback(r));
    }
    document.addEventListener('submit', e => {
        const form = e.target;
        const fd = new FormData(form);
        apiCall(form.action, {method: form.method, body: fd}, callbacks[form.dataset.callback]);
    });
    document.addEventListener('click', e => {
        const link = e.target;
        if ('hash' in link && link.baseURI.startsWith(link.origin)) {
            if (link.hash in actions) {
                actions[link.hash](e);
            }
        }
    });

    // User Auth Functions
    registerAction("#login", function(e) {
        apiCall("/api/login",{method:"GET"}, r => {
            content.innerHTML = r.text;
        });
    });
    registerCallback("login", r => {
        if (r.success) {

        } else {

        }
    });
    // End User Auth Functions

    // history support
    window.addEventListener('hashchange', e => {
        if(window.location.hash in actions) {
            actions[window.location.hash]();
        } else {
            displayPunchClock();
        }
    });
    // end history support

    // display punchclock page on first load
    function displayPunchClock() {
        fetch("/api/main").then(r => r.text()).then(t => content.innerHTML = t);
    }
    displayPunchClock();
})(tc);