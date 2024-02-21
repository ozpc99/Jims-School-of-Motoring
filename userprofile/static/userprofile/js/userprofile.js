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
 * Applies rotation (-7deg to 7deg) to 'CANCELLED' stamp at random.
 * Applies opacity level (0.5 to 1) at random.
 */
function CancelledStampRandom() {
    var stamp = document.querySelectorAll('.cancelled-text');
    stamp.forEach(function (element) {
        // Random Rotation
        var rotation = Math.random() * (7 - (-7)) - 7;
        element.style.transform = 'rotate(' + rotation + 'deg)';
        // Random Opacity
        var opacity = Math.random() * (1 - 0.5) + 0.5;
        element.style.opacity = opacity;
    });
}
window.addEventListener('load', CancelledStampRandom);