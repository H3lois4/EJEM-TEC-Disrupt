document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('btn-toggle-sidebar');  
    const sidebar = document.querySelector('.navbar-lateral');
    if (toggleButton && sidebar) {
        toggleButton.addEventListener('click', function (event) {
            event.preventDefault();
            sidebar.classList.toggle('expanded');
        });
    }
});