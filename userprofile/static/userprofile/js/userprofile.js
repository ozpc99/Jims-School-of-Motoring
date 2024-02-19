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

// Applies either 7deg or -7deg rotation to 'CANCELLED' text at random.
function applyRandomRotation() {
    var elements = document.querySelectorAll('.cancelled-text');
    elements.forEach(function (element) {
        var random = Math.random();
        if (random < 0.5) {
            element.style.transform = 'rotate(7deg)';
        } else {
            element.style.transform = 'rotate(-7deg)';
        }
    });
}
window.addEventListener('load', applyRandomRotation);