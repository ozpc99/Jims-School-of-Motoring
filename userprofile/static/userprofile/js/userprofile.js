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


/**
 * Applies rotation (-7deg to 7deg) to stamps at random.
 */
function stampRandom() {
    var stamps = document.querySelectorAll('.cancelled-text, .previous-text');
    stamps.forEach(function (element) {
        // Random Rotation
        var rotation = Math.random() * (7 - (-7)) - 7;
        element.style.transform = 'rotate(' + rotation + 'deg)';
    });
}
window.addEventListener('load', stampRandom);