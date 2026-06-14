function applyFilters() {
    const loader = document.getElementById("timesheetLoader");

    if (loader) {
        loader.classList.add("show");
    }

    const project = document.getElementById("filter-project").value;

    const params = new URLSearchParams();

    if (project) {
        params.set("project_id", project);
    }

    const queryString = params.toString();

    window.location.href = queryString
        ? "/timesheets?" + queryString
        : "/timesheets";
}