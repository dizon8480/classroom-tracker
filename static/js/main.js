function filterTable(inputId = "subjectFilter", tableId = "recordsTable") {
    const inputElement = document.getElementById(inputId);
    if (!inputElement) return;
    
    const filterValue = inputElement.value.toLowerCase();
    const tableRows = document.querySelectorAll(`#${tableId} tbody tr`);

    tableRows.forEach(row => {
        const rowText = row.innerText.toLowerCase();
        row.style.display = rowText.includes(filterValue) ? "" : "none";
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("subjectFilter");
    if (searchInput) {
        searchInput.addEventListener("keyup", () => filterTable());
    }
});