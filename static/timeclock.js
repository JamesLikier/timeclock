document.addEventListener("click", (event) => {
    if (event.target.classList.contains("collapse-toggle")) {
        parent = event.target.parentElement;
        collapse = parent.querySelector(".collapse");
        parent.classList.toggle("flex-row");
        collapse.classList.toggle("d-flex");
    }
});