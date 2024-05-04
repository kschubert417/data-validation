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