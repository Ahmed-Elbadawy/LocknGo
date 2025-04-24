function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/notes";
  });
}


// Search logic
document.getElementById("searchInput").addEventListener("keyup", function () {
  let filter = this.value.toLowerCase();
  let rows = document.querySelectorAll("#lockerTable tr");
  rows.forEach(row => {
      let text = row.textContent.toLowerCase();
      row.style.display = text.includes(filter) ? "" : "none";
  });
});

// Status + Payment logic
document.querySelectorAll(".status").forEach(select => {
  select.addEventListener("change", function () {
      let row = this.closest("tr");
      let paymentCheckbox = row.querySelector(".payment");
      let costCell = row.querySelector(".cost");
      let originalCost = row.getAttribute("data-cost");
      let lockerId = row.querySelector("td:first-child").textContent.replace('A-', ''); // Extract locker ID
      let newStatus = this.value;

      if (newStatus === "Outside" && !paymentCheckbox.checked) {
          alert("You must mark the payment as checked before setting the item outside.");
          this.value = "Inside";  // Reset
          return;
      }

      // Send the updated status to the backend via AJAX
      fetch('/update_locker_status', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              locker_id: lockerId,
              status: newStatus
          })
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              // If status is outside, reset cost to 0
              costCell.textContent = newStatus === "Outside" ? "0.00" : originalCost;
          } else {
              alert('Error updating locker status');
          }
      })
      .catch(error => {
          console.error('Error:', error);
      });
  });
});

