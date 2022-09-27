(function () {
    const responseHandlers = new Map()

    /* API Hooks */
    document.addEventListener("submit",e=>{
        if(e.target.action.includes("/api/")) {
            e.preventDefault();
            fd = new FormData(e.target);
            fetch(e.target.action, {
                "method": e.target.method,
                "body": fd
            }).then(r => {
                if (r.ok) {
                    r.json().then(o => {
                        responseHandlers.get(o["action"])(o);
                    });
                }
            });
        }
    });
    document.addEventListener("click",e=>{
        if ('href' in e.target && e.target.href.includes("/api/")) {
            e.preventDefault();
            fetch(e.target.href, {
                "method": e.target.dataset.method || "GET"
            }).then(r => {
                if (r.ok) {
                    r.json().then(o => {
                        responseHandlers.get(o["action"])(o);
                    });
                }
            });
        }
    });
    /* End API Hooks */

    /* Employee Functions */
    /* End Employee Functions */

    /* Login/Logout */
    responseHandlers.set("login",o => {
        if (o["result"] == "success") {
            document.location = "/";
        }
    });
    responseHandlers.set("logout",o => {
        if (o["result"] == "success") {
            document.location = "/";
        }
    });
    let loginFloat = undefined;
    function showLogin(p) {
        if (loginFloat == undefined){
            e = document.createElement("div");
            e.classList.add("login-float");
            fetch("/api/login", {
                "method": "GET"
            }).then(r => {
                if (r.ok) {
                    r.text().then(s => {
                        loginFloat = e;
                        e.innerHTML = s;
                        p.append(e);
                    });
                }
            });
        }
    }
    document.addEventListener("click",e=>{
        if (loginFloat != undefined && !loginFloat.contains(e.target)) {
            loginFloat.remove();
            loginFloat = undefined;
        }
        if (e.target.id == "login") {
            e.preventDefault();
            showLogin(e.target);
        }
    });
    /* End Login/Logout */

    /* Punch Clock */
    function updateClockTime() {
        let e = document.querySelector(".clock");
        let d = new Date()
        if (e) {
            e.textContent = d.toLocaleTimeString()
        }
    }
    updateClockTime()
    setInterval(updateClockTime,1000);

    document.addEventListener("click",e => {
        let numpadDisplay = document.querySelector(".numpad-display");
        let numpadValue = document.querySelector("#numpad-value");
        let value = e.target.textContent.trim();
        if(e.target.classList.contains("numpad-key")){
            if (numpadDisplay.classList.contains("private")) {
                numpadDisplay.textContent += "*";
                numpadValue.value += value;
            } else {
                numpadDisplay.textContent += value;
                numpadValue.value += value;
            }
        } else if (e.target.classList.contains("numpad-clear")){
            numpadDisplay.textContent = "";
            numpadValue.value = "";
        } else if (e.target.classList.contains("numpad-enter")){
        }
    });
    /* End Punch Clock */

    /* Collapse */
    function collapsed(e) {
        if (e.target.getAttribute("collapse") === "hide") {
            e.target.classList.add("d-none");
        } else {
            e.target.style.height = null;
        }
        e.target.classList.remove("collapsing");
        e.target.removeEventListener("transitionend", collapsed);
    }

    function collapseHide(e, transition = true) {
        effect = e.getAttribute("transition");
        if (transition) {
            window.requestAnimationFrame(timestamp => {
                e.style.height = `${e.scrollHeight}px`;
                window.requestAnimationFrame(timestamp => {
                    e.classList.add("hide");
                });
            });
        } else {
            e.style.height = `${e.scrollHeight}px`;
            e.classList.remove(effect);
            e.classList.add("d-none");
            e.classList.add("hide");
        }
        e.setAttribute("collapse", "hide");
    }

    function collapseShow(e, transition = true) {
        effect = e.getAttribute("transition");
        if (transition) {
            e.classList.add(effect);
            window.requestAnimationFrame(t => {
                e.classList.remove("d-none");
                window.requestAnimationFrame(t => {
                    e.classList.remove("hide");
                });
            });
        } else {
            e.classList.remove(effect);
            e.style.height = null;
            e.classList.remove("hide");
            e.classList.remove("d-none");
        }
        e.setAttribute("collapse", "show");
    }

    function toggleCollapse(e) {
        if (e.getAttribute("collapse") === "show") {
            collapseHide(e);
        } else {
            collapseShow(e);
        }
        e.addEventListener("transitionend", collapsed);
        e.classList.add("collapsing");
    }

    document.addEventListener("click", event => {
        let collapseTarget = event.target.getAttribute("collapse-target");
        if (collapseTarget != null) {
            toggleCollapse(document.querySelector(`#${collapseTarget}`));
        } else if (event.target.classList.contains("collapse-toggle")) {
            let parent = event.target.parentElement;
            let collapseElement = parent.querySelector(".collapse");
            toggleCollapse(collapseElement);
        }
    });
    let lastWidth = -1;
    let collapseWidth = 800;
    function initializeCollapseState() {
        let e = document.querySelector(".collapse");
        //window first created
        if (lastWidth === -1) {
            if (window.innerWidth <= collapseWidth) {
                collapseHide(e, false);
            }
            //window was resized from large to small
        } else if (window.innerWidth <= collapseWidth && lastWidth > collapseWidth) {
            collapseHide(e, false);
            //window was resized from small to large
        } else if (window.innerWidth > collapseWidth && lastWidth <= collapseWidth) {
            collapseShow(e, false);
        }
        lastWidth = window.innerWidth;
    }
    initializeCollapseState();
    window.addEventListener("resize", event => {
        initializeCollapseState();
    });
    /* End Collapse */
})();