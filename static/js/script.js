console.log("I am here")
// Get all select elements with the class "select-control"
var selects = document.querySelectorAll('.select-control');
selects.forEach(function(select) {
    select.addEventListener('change', function() {
        // This assumes the textbox container is immediately after the select element in the DOM
        var textboxContainer = this.nextElementSibling;
        if (this.value === 'option3') {
            textboxContainer.style.display = 'inline-block'; // Show the text box
        } else {
            textboxContainer.style.display = 'none'; // Hide the text box
        }
    });
});