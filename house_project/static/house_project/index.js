document.addEventListener('DOMContentLoaded', () => {
    
    document.getElementById("login-form").addEventListener("submit", function(event) {
        // Get the username and password values
        var username = document.getElementById("Username").value;
        var password = document.getElementById("Password").value;
    
        // Validate the username and password
        if (username === "" || password === "") {
            alert("Please enter a valid username and password.");
            event.preventDefault();
        }
    });

})


