// script to take data from admin page and import flags into database
// can definitely be improved
document.addEventListener('DOMContentLoaded', (event) => {
  document.querySelector('.submit').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the default action of the link

    let result = {
      info: { 'customer': customer, 'swvendor': swvendor },
      modules: {},
      tables: {},
      columns: {}
    };

    // Process module checkboxes
    document.querySelectorAll('.module-checkbox').forEach((checkbox) => {
      let moduleName = checkbox.getAttribute('data-module');
      result.modules[moduleName] = checkbox.checked ? 1 : 0;
    });

    // Process table checkboxes
    document.querySelectorAll('.table-checkbox').forEach((checkbox) => {
      let moduleName = checkbox.getAttribute('data-module');
      let tableName = checkbox.getAttribute('data-table');
      if (!(moduleName in result.tables)) {
        result.tables[moduleName] = {};
      }
      result.tables[moduleName][tableName] = checkbox.checked ? 1 : 0;
    });

    // Process column checkboxes
    document.querySelectorAll('.column-checkbox').forEach((checkbox) => {
      let tableName = checkbox.getAttribute('data-table');
      let columnName = checkbox.closest('tr').querySelector('td:nth-child(2)').textContent;
      if (!(tableName in result.columns)) {
        result.columns[tableName] = {};
      }
      result.columns[tableName][columnName] = checkbox.checked ? 1 : 0;
    });

    console.log(result);
    // alert('Configuration updated successfully!');
    // If you want to send this data to the server, you can use the fetch API here
    fetch('/updatecustconfig', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(result)
    }).then(response => {
      if (response.ok) {
        alert('Configuration updated successfully!');
      } else {
        alert('Failed to update configuration.');
      }
    }).catch(error => {
      console.error('Error:', error);
      alert('An error occurred while updating configuration.');
    });
  });
});







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








