var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1); // Slice removes quotation marks
var clientSecret = $('#id_client_secret').text().slice(1, -1); // Slice removes quotation marks
var stripe = Stripe(stripePublicKey);

var elements = stripe.elements();
var style = {
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545',
        'border-color': '#dc3545',
        'outline': '0',
        'box-shadow': '0 0 0 .2rem rgba(0,123,255,.25)',
        'transition': 'border-color .15s ease-in-out, box-shadow .15s ease-in-out'
    },
    ':-webkit-autofill': {
        color: '#e8f0fe !important',
    },
};
var card = elements.create('card');
card.mount('#card-element', {style: style});

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon">
                <i class="fa-solid fa-triangle-exclamation"></i>
            </span>
            <span>${event.error.message}</span>
        `
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({'disabled': true});
    $('#submit-button').attr('disabled', true);
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: $.trim(form.billpayer_name.value),
                address:{
                    line1: $.trim(form.billpayer_house_no.value),
                    line2: $.trim(form.billpayer_street.value),
                    city: $.trim(form.billpayer_town.value),
                }
            }
        },
        shipping: {
            name: $.trim(form.full_name.value),
            address:{
                line1: $.trim(form.house_no.value),
                line2: $.trim(form.street.value),
                city: $.trim(form.town.value),
                postal_code: $.trim(form.post_code.value),
            },
        },
    }).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon">
                <i class="fa-solid fa-triangle-exclamation"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            card.update({'disabled': false});
            $('#submit-button').attr('disabled', false)
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                console.log('Payment Succeeded!')
                form.submit();
            }
        }
    });
});