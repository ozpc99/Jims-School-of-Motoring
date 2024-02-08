document.addEventListener('DOMContentLoaded', function () {

    // Welcome Messages:
    let welcomeMessage;

    if (firstName === "None") {
        welcomeMessage = 'Welcome, ' + userName;
        displayWelcomeMessage(welcomeMessage);
    } else {
        welcomeMessage = 'Welcome back, ' + firstName;
        displayWelcomeMessage(welcomeMessage);
    }

    function displayWelcomeMessage(message) {
        document.getElementById('profileTitle').innerText = message;

        // Transitions...
        var headerContainer = document.getElementById('profileHeaderContainer');
        setTimeout(function () {
            headerContainer.classList.add('active');
        }, 1000);

        var profileBody = document.getElementById('profileBody');
        setTimeout(function () {
            profileBody.classList.add('active');
        }, 2000);
    }
});