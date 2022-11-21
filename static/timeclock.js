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
    const views = {};
    const actions = {};
    function registerCallback(key,fn) {
        callbacks[key] = fn;
    }
    function registerView(key,fn) {
        views[key] = fn;
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
        e.preventDefault();
        const form = e.target;
        const fd = new FormData(form);
        const obj = {};
        for (k of fd.keys()) {
            obj[k] = fd.get(k);
        }
        apiCall(form.action, {method: form.method, body: JSON.stringify(obj)}, callbacks[form.dataset.callback]);
    });
    document.addEventListener('click', e => {
        if (e.target.tagName.toUpperCase() == 'A') {
            const link = e.target;
            if (link.dataset.action) {
                actions[link.dataset.action](e);
            }
        }
    });

    // User Auth Functions
    registerView("#login", e => {
        apiCall("/api/login",{method:"GET"}, r => {
            content.innerHTML = r.text;
        });
    });
    registerCallback("login", r => {
        if (r.success) {
            document.location = "#main";
        } else {
            document.querySelector("#login-error-msg").textContent = r.text;
        }
    });
    registerAction("logout", e => {
        e.preventDefault();
        apiCall("/api/logout", {},r => {
            if (r.success) {
                document.location = "#main";
            }
        });
    });
    // End User Auth Functions

    // history support
    window.addEventListener('hashchange', e => {
        if(window.location.hash in views) {
            views[window.location.hash]();
        } else {
            views.main();
        }
    });
    // end history support

    // display punchclock page on first load
    function displayPunchClock() {
        fetch("/api/main").then(r => r.text()).then(t => content.innerHTML = t);
    }
    displayPunchClock();
    registerView("main", e => {
        displayPunchClock();
    });

    registerAction("reload", e => {
        apiCall("/api/reload",{method:"GET"},r => {
        });
    });
})(tc);