// Create a Stripe client.
var stripe = Stripe('pk_test_BrSBsahua38JoP9xfxQIIuME00QJ01M5ar');

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});

// Submit the form with the token ID.
function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}

document.addEventListener('DOMContentLoaded', () => {


    function notifyUser(message="") {

      alertElem = document.querySelector("#alert-message");
      
      if (message == "") {
          alertElem.innerHTML = "";
          return;
      }

      alertElem.innerHTML = '<div class="alert alert-info d-flex justify-content-center" role="alert">' + message + '</div>'; 
    }

    function submitForm(formData) {

        let url = "/orders/processForm/";

        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify(formData)
        })

        .then((response) => {
            return response.json();
        })

        .then((data) => {
            if (data.status == true) 
            {
              document.querySelector("#address-form").className = "d-none";
              document.querySelector("#payment-form").className = "";
              document.querySelector("#formDiv").className = "mx-auto p-4 bg-light w-50 h-50"
              notifyUser("Fields have been successfully updated.")
            }
            else 
            {
              notifyUser("Sorry fields are not valid.")
            }
        })
    }


    document.querySelector("#addressForm").onclick = function() {

        notifyUser("");
        let serFormArray = $('#address-form').serializeArray();

        let formData = {};

        for (d of serFormArray) {

            if (d['value'] != "") {
              formData[d['name']] = d['value'];
            }
            else {
              notifyUser("Fields cannot be empty.");
              return;
            }
        }

        submitForm(formData);

    }

});