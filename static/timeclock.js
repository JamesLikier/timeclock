function collapsed(e) {
    if (e.getAttribute("collapse") === "hide") {
        e.target.classList.add("d-none");
    } else {
        e.target.style.height = null;
    }
    e.target.classList.remove("collapsing");
    e.target.removeEventListener("transitionend", collapsed);
}

function collapseHide(e) {
    window.requestAnimationFrame(timestamp => {
        e.style.height = `${e.scrollHeight}px`;
        window.requestAnimationFrame(timestamp => {
            e.classList.toggle("hide");
        });
    });
    e.setAttribute("collapse", "hide");
}

function collapseShow(e) {
    window.requestAnimationFrame(t => {
        e.classList.remove("d-none");
        window.requestAnimationFrame(t => {
            e.classList.remove("hide");
        });
    });
    e.setAttribute("collapse", "show");
}

function toggleCollapse(e) {
    if (e.getAttribute("collapse") === "hide") {
        collapseShow(e);
    } else {
        collapseHide(e);
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