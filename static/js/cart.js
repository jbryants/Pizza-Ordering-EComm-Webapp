document.addEventListener('DOMContentLoaded', () => {


    function getExtras(productId) {

        let extrasElems = document.querySelectorAll("#extras" + productId);

        let extras = new Set();

        for (e of extrasElems) {

            if (extras.has(e.value))
            {
                e.focus();
                return "Extras can't repeat, please recheck your extras choices.";
            }

            if (!e.value == "") {
                // add to if selected.
                extras.add(e.value);
            }

        }

        return extras;
    }


    function updateCartInfo(items, price) 
    {
        let innerContent = `${items} items, $${price}`;

        // if span elem exist
        let cartItems = document.querySelector("#cart-items");

        if (cartItems) 
        {
            cartItems.innerHTML =  innerContent;
        }
        else 
        {
            // else if span elem does not exist
            let cart = document.querySelector("#cartUI");

            let span = document.createElement("span");
            
            span.setAttribute("id", "cart-items");
            span.setAttribute("class", "badge badge-pill badge-light text-success");
            span.innerHTML = innerContent;

            cart.appendChild(span);
        }
    }

    function addOrderItem(productId, action, toppings, extras, quantity) {

        let url = "/cart/add/";

        toppings = Array.from(toppings).join(' ');
        extras = Array.from(extras).join(' ');

        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'productId': productId,
                                 'action': action,
                                 'toppings': toppings,
                                 'extras': extras,
                                 'quantity': quantity})
        })

        .then((response) => {
            return response.json();
        })

        .then((data) => {
            if (data.added == true) {
                updateCartInfo(data.totalItems, data.totalPrice);
            }
        })
    }


    function extractToppings(toppingsArg) {

        let toppings = new Set();

        for (t of toppingsArg) {
                        
            if (t.value == "") {
                t.focus();
                return "Please select topping for Pizza.";
            }
            
            if (toppings.has(t.value))
            {
                t.focus();
                return "Toppings can't repeat, please recheck your toppings choices.";
            }

            toppings.add(t.value);
        }

        return toppings;
    }


    function getToppings(productId) {

        let oneToppings = document.querySelectorAll("#oneToppings" + productId);
        let twoToppings = document.querySelectorAll("#twoToppings" + productId);
        let threeToppings = document.querySelectorAll("#threeToppings" + productId);

        if (oneToppings.length == 1) 
        {
            return extractToppings(oneToppings);
        } 
        else if (twoToppings.length >= 1) 
        {
            return extractToppings(twoToppings);
        } 
        else if (threeToppings.length >= 1) 
        {
            return extractToppings(threeToppings);
        }
        else
        {
            // return empty set
            return new Set();
        }

    }


    function notifyUser(message="") {

        alertElem = document.querySelector("#alert-message");
        
        if (message == "") {
            alertElem.innerHTML = "";
            return;
        }

        alertElem.innerHTML = '<div class="alert alert-info d-flex justify-content-center" role="alert">' + message + '</div>'; 
    }


    function getQuantity(productId)
    {
        let quantElem = document.querySelector("#quantity" + productId);
        return quantElem.value;
    }

    document.querySelectorAll("#addToCart").forEach( function(button) {
        
        button.onclick = function() {
            
            // clearing out messages if any.
            notifyUser();

            if (isUserAuth == "False") {
                // is user is not authenticated then notify user to login first
                notifyUser(message="You need to login first in order to add items to the cart.")
                return;
            }

            let productId = this.dataset.product;
            let action = this.dataset.action;

            // get toppings present
            toppings = getToppings(productId);

            if (typeof(toppings) == "string") {
                // validation failed so notify user.
                notifyUser(toppings);
                return;
            }

            // get extras present
            extras = getExtras(productId);

            if (typeof(extras) == "string") {
                // validation failed so notify user.
                notifyUser(extras);
                return;
            }
            
            quantity = getQuantity(productId);

            if (isUserAuth == "True") {
                // as user it auth we can update cart
                addOrderItem(productId, action,
                                toppings, extras, quantity);
            }

        }
    })


    function updateOrderItem(itemId, quantity=0) {
        let url = "/cart/update/";

        fetch(url, {
            method: "POST",
            headers: {
                'Content-Type':'application/json',
                'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'itemId': itemId, 'quantity': quantity})
        })

        .then((response) => {
            return response.json();
        })

        .then((data) => {
            if (data.updated == true) {
                if (quantity == 0) {
                    
                    // delete if quantity 0
                    let row = document.querySelector("#row" + itemId);
                    row.remove();

                }
                else {
                    notifyUser('Quantity has been successfully updated.');

                    let priceElem = document.querySelector("#price" + itemId);
                    priceElem.innerHTML = "$" + data.price;
                }

                let totalPrice = document.querySelector("#totalPrice");
                totalPrice.innerHTML = "$" + data.totalPrice;

                updateCartInfo(data.totalItems, data.totalPrice);
            }
        })
    }


    document.querySelectorAll("#update").forEach( function(button) {

        button.onclick = function() {
            
            // clearing out messages if any.
            notifyUser();

            let itemId = button.dataset.id;
            let quantity = document.querySelector("#itemQuantity" + itemId).value;

            updateOrderItem(itemId, quantity);

        }
    })


    document.querySelectorAll("#delete").forEach( function(button) {

        button.onclick = function() {
            
            // clearing out messages if any.
            notifyUser();

            let itemId = button.dataset.id;

            updateOrderItem(itemId);

        }
    })

    document.querySelector("#checkoutBtn").onclick = (btn) => {

        if (document.querySelector("#cart-items").innerHTML[0] == "0") {
            btn.preventDefault();
            notifyUser("Cart cannot be empty, please add some items to the cart before checkout.");
        }

    }
});