document.querySelectorAll('.module-checkbox').forEach(function (moduleCheckbox) {
  moduleCheckbox.addEventListener('change', function () {
    let module = this.dataset.module;
    document.querySelectorAll('.table-checkbox').forEach(function (tableCheckbox) {
      if (tableCheckbox.dataset.module === module) {
        tableCheckbox.checked = moduleCheckbox.checked;
        let table = tableCheckbox.dataset.table;
        document.querySelectorAll('.column-checkbox').forEach(function (columnCheckbox) {
          if (columnCheckbox.dataset.table === table) {
            columnCheckbox.checked = tableCheckbox.checked;
          }
        });
      }
    });
  });
});

document.querySelectorAll('.table-checkbox').forEach(function (tableCheckbox) {
  tableCheckbox.addEventListener('change', function () {
    let table = this.dataset.table;
    document.querySelectorAll('.column-checkbox').forEach(function (columnCheckbox) {
      if (columnCheckbox.dataset.table === table) {
        columnCheckbox.checked = tableCheckbox.checked;
      }
    });
  });
});


// Script to update URL to map files to tables
function updateLink(selectElement) {
  const table = selectElement.value;
  const link = selectElement
    .closest("tr")
    .querySelector(".settings-link");
  const url = new URL(link.href);

  // Remove existing 'table' query parameter if present
  url.searchParams.delete("table");
  // Add new 'table' parameter
  url.searchParams.append("table", table);
  link.href = url.toString();
  console.log(link.href);
}

// Function to update metadata in application
// used to make sure fields are properly stored
document.getElementById('myForm').addEventListener('save', function (event) {
  event.preventDefault();

  var formData = new FormData(event.target);
  var data = {};

  formData.forEach(function (value, key) {
    data[key] = value;
  });

  fetch('/save?file={{ file_name }}', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
