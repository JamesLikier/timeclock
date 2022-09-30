(function () {
    const content = document.querySelector("#content");
    const responseHandlers = new Map()

    /* API Hooks */
    document.addEventListener("submit",e=>{
        let form = null
        for(f of document.querySelectorAll("form")){
            if(f.contains(e.submitter)){
                form = f;
                break;
            }
        }
        if(form.action.includes("/api/")) {
            e.preventDefault();
            fd = new FormData(form);
            fetch(form.action, {
                "method": form.method,
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
    responseHandlers.set("employee/new",o => {
        content.innerHTML = o["body"];
    });
    /* End Employee Functions */

    /* Punch Functions */
    responseHandlers.set("punch/new",o=> {
        displayModal("Punch Result", o["result"], null, 3);
    });
    /* End Punch Functions */

    /* Login/Logout */
    let loginFloat = null;
    responseHandlers.set("comp/login",o => {
        c = document.querySelector("#login");
        e = document.createElement("div");
        e.classList.add("login-float");
        e.innerHTML = o["body"];
        c.append(e);
        loginFloat = e;
    });
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
    document.addEventListener("click",e=>{
        if (loginFloat != null && !loginFloat.contains(e.target)) {
            loginFloat.remove();
            loginFloat = null;
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
    /* End Punch Clock */

    /* Num Pad */
    document.addEventListener("click",e => {
        let numpad = null;
        for (n of document.querySelectorAll("#numpad")) {
            if (n.contains(e.target)) {
                numpad = n;
                break;
            }
        }
        if (numpad == null) return;

        let numpadDisplay = numpad.querySelector("#numpad-display");
        let numpadValue = numpad.querySelector("#numpad-value");
        if(e.target.classList.contains("numpad-key")){
            let value = e.target.textContent.trim();
            if(numpadValue.value == null) {
                numpadValue.value == "";
            }
            numpadValue.value += value;
            if (numpadDisplay.classList.contains("private")) {
                numpadDisplay.textContent += "*";
            } else {
                numpadDisplay.textContent += value;
            }
        } else if (e.target.classList.contains("numpad-clear")){
            numpadDisplay.textContent = "";
            numpadValue.value = "";
        } else if (e.target.classList.contains("numpad-enter")){
            const forms = document.querySelectorAll("form");
            let form = null
            for (f of forms) {
                if (f.contains(e.target)) {
                    form = f;
                }
            }
            if (form != null) {
                document.dispatchEvent(new SubmitEvent('submit',{'submitter': e.target}));
                numpadDisplay.textContent = "";
                numpadValue.value = "";
            }
        }
    });
    /* End Num Pad */

    /* Modal */
    function displayModal(title="",body="", target=null, time=0) {
        let modal_bg = document.createElement("div");
        modal_bg.classList.add("modal-bg");
        let modal = document.createElement("div");
        modal.classList.add("modal");
        let modal_title = document.createElement("div");
        modal_title.classList.add("modal-title");
        modal_title.textContent = title;
        let modal_body = document.createElement("div");
        modal_body.classList.add("modal-body");
        modal_body.textContent = body;
        let modal_footer = document.createElement("div");
        modal_footer.classList.add("modal-footer");
        let close_button = document.createElement("button");
        close_button.textContent = "Close";
        close_button.addEventListener("click", e => modal_bg.remove());
        modal_footer.append(close_button);
        modal.append(modal_title);
        modal.append(modal_body);
        modal.append(modal_footer);
        modal_bg.append(modal);
        if (target == null) {
            document.querySelector("body").append(modal_bg);
        } else {
            target.append(modal_bg);
        }
        if (time > 0) {
            setTimeout(() => {
                modal_bg.remove();
            },time*1000);
        }
    } 
    /* End Modal */

    /* Collapse */
    function collapsed(e) {
        if (e.target.getAttribute("collapse") === "hide") {
            e.target.classList.add("d-none");
        } else {
            //e.target.style.height = null;
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