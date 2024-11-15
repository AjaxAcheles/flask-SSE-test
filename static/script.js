document.addEventListener('DOMContentLoaded', (event) => {
    const eventSource = new EventSource('/stream');
    const tableBody = document.querySelector('#data-table tbody');

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${data.date_time}</td>
            <td>${data.v_code}</td>
            <td>${data.raw}</td>
            <td>${data.cadet}</td>
        `;
        tableBody.insertBefore(newRow, tableBody.firstChild);
    };
});