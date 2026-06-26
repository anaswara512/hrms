console.log("HRMS Loaded Successfully");

document.addEventListener("DOMContentLoaded", function () {

    const search = document.getElementById("searchEmployee");

    if (search) {

        search.addEventListener("keyup", function () {

            const filter = this.value.toLowerCase();

            const rows = document.querySelectorAll("#employeeTable tbody tr");

            rows.forEach(function (row) {

                const text = row.innerText.toLowerCase();

                row.style.display = text.includes(filter) ? "" : "none";

            });

        });

    }

});

document.addEventListener("DOMContentLoaded", function () {

    const search = document.getElementById("searchEmployee");

    if (search) {

        search.addEventListener("keyup", function () {

            let value = this.value.toLowerCase();

            let rows = document.querySelectorAll("#employeeTable tbody tr");

            rows.forEach(function(row){

                row.style.display =
                    row.innerText.toLowerCase().includes(value)
                    ? ""
                    : "none";

            });

        });

    }

});

function checkIn(employeeId) {
    const csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrftoken = csrfEl ? csrfEl.value : '';
    
    fetch("/attendance/checkin/" + employeeId + "/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
        } else {
            alert("Error: " + (data.message || "Failed to check in"));
        }
        location.reload();
    })
    .catch(err => {
        console.error(err);
        alert("Failed to send request.");
    });
}

function checkOut(attendanceId) {
    const csrfEl = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrftoken = csrfEl ? csrfEl.value : '';
    
    fetch("/attendance/checkout/" + attendanceId + "/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert(data.message);
        } else {
            alert("Error: " + (data.message || "Failed to check out"));
        }
        location.reload();
    })
    .catch(err => {
        console.error(err);
        alert("Failed to send request.");
    });
}