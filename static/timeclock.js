(function () {
    const content = document.querySelector("#content");
    const responseHandlers = new Map();
    const clickHandlers = new Map();

    /* API Hooks */
    function apiCall(path, options, handler = null) {
        fetch(path, options).then(r => {
            if (r.ok) {
                r.json().then(o => {
                    if (handler) {
                        handler(o);
                    } else {
                        responseHandlers.get(o["action"])(o);
                    }
                });
            }
        });
    }
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
            data = {};
            for(pairs of fd.entries()){
                data[pairs[0]] = pairs[1];
            }
            apiCall(form.action, {
                "method": form.method,
                "body": JSON.stringify(data)
            })
        }
    });
    document.addEventListener("click",e=>{
        if ('href' in e.target && e.target.getAttribute("href").includes("#")) {
            const href = e.target.getAttribute("href");
            e.preventDefault();
            if (clickHandlers.has(href)) {
                clickHandlers.get(href)(e);
            }
        } else if ('href' in e.target && e.target.href.includes("/api/")) {
            e.preventDefault();
            apiCall(e.target.href, {
                "method": e.target.dataset.method || "GET"
            })
        }
    });
    /* End API Hooks */

    /* Float Functions */
    const floatHandlers = new Map();
    function setFloat(f, closeHandler = null) {
        if (floatHandlers.get(f)) {
            //do nothing, already showing the float
        } else {
            let handler = function (e) {
                if (f.parentElement && !f.parentElement.contains(e.target)) {
                    f.classList.add('d-none');
                    document.removeEventListener("click", handler);
                    floatHandlers.delete(f);
                    closeHandler && closeHandler(f);
                }
            }
            f.classList.remove("d-none");
            floatHandlers.set(f, handler);
            document.addEventListener("click", handler);
        }
    }
    /* End Float Functions */

    /* Menu Functions */
    clickHandlers.set("#dropdown-toggle", e => {
        const m = e.target.parentElement.querySelector("#menu");
        setFloat(m);
    });
    /* End Menu Functions */

    /* Punch Functions */
    responseHandlers.set("punch/new",o=> {
        if (o["result"] == "success") {
            const f = document.querySelector("#newPunch");
            f.reset();
            displaySuccessModal("Punch Result","Success",3);
        } else {
            displayErrorModal("Punch Result","Problem Creating Punch",3);
        }
    });
    responseHandlers.set("punch/delete",o=>{
    });
    function refreshPunchList() {
        apiCall('/api/punch/list', {
            'method': 'POST',
            'body': JSON.stringify({
                "employeeid": 1,
                "startDate": document.querySelector('#punchlistStartdate').value,
                "endDate": document.querySelector("#punchlistEnddate").value
            })
        }, o => {
            if (o["result"] == "success") {
                content.innerHTML = o["body"];
            }
        });
    }
    document.addEventListener('change',e=>{
        if (e.target.id == "punchlistStartdate" || e.target.id == "punchlistEnddate"){
            refreshPunchList();
        }
    });
    let curCell = null;
    let curCellFloat = null;
    clickHandlers.set("#punchlist/modify/cancel",e=>{
        resetCurCell();
    });
    clickHandlers.set("#punchlist/modify/delete",e=>{
        apiCall("/api/punch/delete",{
            'method': 'POST',
            'body': JSON.stringify({'pid': curCell.getAttribute('data-pid')})
        }, o => {
            if (o["result"] == "success") {
                refreshPunchList();
            }
        });
    });
    clickHandlers.set("#punchlist/modify/save",e=>{
        apiCall("/api/punch/new",{
            'method': 'POST',
            'body': JSON.stringify({
                'employeeid': curCell.getAttribute('data-eid'),
                'date': curCell.getAttribute('data-date'),
                'time': curCell.querySelector('input').value
            })
        }, o => {
            if (o["result"] == "success") {
                refreshPunchList();
            }
        });
    });
    function styleModifyFloat(f) {
        f.classList.add('modify-float');
        return f;
    }
    function createSaveFloat() {
        const cellFloat = document.createElement('div');
        cellFloat.classList.add('floating');
        const saveBtn = document.createElement('a');
        saveBtn.textContent = 'Save';
        saveBtn.href = "#punchlist/modify/save";
        const cancelBtn = document.createElement('a');
        cancelBtn.textContent = 'Cancel';
        cancelBtn.href = "#punchlist/modify/cancel";
        cellFloat.appendChild(saveBtn);
        cellFloat.appendChild(cancelBtn);
        return styleModifyFloat(cellFloat);
    }
    function createDeleteFloat() {
        const cellFloat = document.createElement('div');
        cellFloat.classList.add('floating');
        const deleteBtn = document.createElement('a');
        deleteBtn.textContent = 'Delete';
        deleteBtn.href = "#punchlist/modify/delete";
        const cancelBtn = document.createElement('a');
        cancelBtn.textContent = 'Cancel';
        cancelBtn.href = "#punchlist/modify/cancel";
        cellFloat.appendChild(deleteBtn);
        cellFloat.appendChild(cancelBtn);
        return styleModifyFloat(cellFloat);
    }
    function setCurCell(cell) {
        curCell = cell;
        curCell.classList.add('highlight-yellow');
        if (curCell.getAttribute('data-pid') == 'new') {
            const timeInput = document.createElement('input');
            timeInput.type = "text";
            timeInput.name = "time";
            curCell.appendChild(timeInput);
            curCellFloat = createSaveFloat();
        } else {
            curCellFloat = createDeleteFloat();
        }
        curCell.appendChild(curCellFloat);
        setFloat(curCellFloat, f => {
            f.remove();
        });
    }
    function resetCurCell() {
        if (curCell) {
            curCell.classList.remove('highlight-yellow');
            let input = curCell.querySelector('input');
            input && input.remove();
            curCell = null;
            curCellFloat && curCellFloat.remove();
        }
    }
    document.addEventListener('click',e=>{
        if (e.target == curCell) {
            //do nothing
        } else {
            if (e.target.classList.contains('punch-list-time')) {
                if (curCell) {
                    resetCurCell();
                }
                setCurCell(e.target);
            } else if (curCell && !curCell.contains(e.target)) {
                resetCurCell();
            }
        }
    });
    /* End Punch Functions */

    /* Reload Handler */
    clickHandlers.set("#reload", e=> {
        apiCall("/api/reload",{"method": "GET"});
    });
    responseHandlers.set("reload",o=> {
        const title = "Hot Reload";
        body = o["result"];
        if (o["result"] == "success") {
            displaySuccessModal(title,body,3);
        } else {
            displayErrorModal(title,body,3);
        }
    });
    /* End Reload Handler */

    /* Employee Functions */
    responseHandlers.set("employee/new",o => {
        content.innerHTML = o["body"];
    });
    /* End Employee Functions */

    /* Login/Logout */
    clickHandlers.set("#login", e=> {
        const d = e.target.parentElement.querySelector("#login");
        setFloat(d);
    });
    clickHandlers.set("#logout", e=> {
        apiCall("/api/logout",{"method": "GET"});
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
    /* End Login/Logout */

    /* Punch Clock */
    let numpadDisplay = document.querySelector("#numpad-display");
    let numpadValue = document.querySelector("#numpad-value");
    if(numpadDisplay != null) {
        numpadDisplay.textContent = "Enter ID";
        numpadValue.value == "";
    }
    responseHandlers.set("punchclock",o => {
        const title = "PunchClock Result";
        let func = (o["result"] == "success") ? displaySuccessModal : displayErrorModal;
        func(title,o["body"],3);
    });
    const punchClock = {}
    punchClock.state = "employeeid";
    document.addEventListener('numpad-enter', e => {
        if (punchClock.state == "employeeid"){
            numpadDisplay.textContent = "Enter PIN";
            numpadDisplay.classList.add("private");
            punchClock.employeeid = e.detail;
            punchClock.state = "pin";
        } else if (punchClock.state == "pin"){
            numpadDisplay.textContent = "Enter ID";
            numpadDisplay.classList.remove("private");
            punchClock.pin = e.detail;
            punchClock.state = "employeeid";
            for(f of document.querySelectorAll("form")){
                if (f.contains(e.target)){
                    f.querySelector("#pc-employeeid").value = punchClock.employeeid;
                    f.querySelector("#pc-pin").value = punchClock.pin;
                    f.dispatchEvent(new SubmitEvent("submit",{ "bubbles": true, "cancelable": true, submitter: e.target}))
                    break;
                }
            }
        }
    });
    function updateClockTime() {
        let e = document.querySelector(".clock");
        let d = new Date()
        if (e) {
            e.textContent = d.toLocaleTimeString();
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
            if(numpadValue.value == "") {
                numpadDisplay.textContent = "";
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
            numpadDisplay.textContent = "";
            numpad.dispatchEvent(new CustomEvent('numpad-enter', {"bubbles": true, "detail": numpadValue.value}));
            numpadValue.value = "";
        }
    });

    /* Modal */
    function displayErrorModal(title="",body="",time=0,target=null) {
        displayModal(title,body,time,target,"error");
    }
    function displaySuccessModal(title="",body="",time=0,target=null) {
        displayModal(title,body,time,target,"success");
    }
    function displayWarningModal(title="",body="",time=0,target=null) {
        displayModal(title,body,time,target,"warning");
    }
    function displayModal(title="",body="",time=0,target=null,mode="normal") {
        let modal_bg = document.createElement("div");
        modal_bg.classList.add("modal-bg");
        let modal = document.createElement("div");
        modal.classList.add("modal");
        let modal_title = document.createElement("div");
        modal_title.classList.add("modal-title");
        modal_title.classList.add(mode);
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