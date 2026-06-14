
    function applyFilters() {
        const project = document.getElementById("filter-project").value;
        const month = document.getElementById("filter-month").value;

        const params = new URLSearchParams();

        if (project) {
            params.set("project_id", project);
        }

        if (month) {
            params.set("month", month);
        }

        const queryString = params.toString();

        window.location.href = queryString
            ? "/timesheets?" + queryString
            : "/timesheets";
    }