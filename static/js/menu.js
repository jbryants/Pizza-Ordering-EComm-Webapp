document.addEventListener('DOMContentLoaded', () => {

    // price change based on quantity change, just for the UI
    document.querySelectorAll("[id^=quantity]").forEach( function(select) {

        select.onchange = function() {
            let idVal = select.dataset.id;
            let priceElem = document.getElementById(idVal);
            let ogPrice = priceElem.dataset.ogprice;

            let extrasSelected = getExtras(idVal).size;

            priceChange = ogPrice * select.value;

            if (extrasSelected >= 1)
            {
                priceChange = Number(priceChange) + ((0.50 * extrasSelected) * select.value);
            }

            // rounding up the number to upto 2 decimal places and
            // changing the innerHTML to display the new price
            priceElem.innerHTML = "$" + (Math.round(priceChange * 100) / 100).toFixed(2);
            priceElem.setAttribute("value", priceChange);
        }

    });


    // hashmap to prevent repeated change of same select option for extras.
    var extrasMap = new Map();


    // price change based on extras added, just for the UI
    document.querySelectorAll("[id^=extras]").forEach( function(select) {

        select.onchange = function() {
            let idVal = select.dataset.id
            let priceElem = document.getElementById(idVal);

            let quantElem = document.querySelector("#quantity" + idVal);

            // new entry in map
            if (!extrasMap.has(select))
            {
                extrasMap.set(select, false);
            }

            // if select changed to an extra item
            if ((select.value != "") && (extrasMap.get(select) == false))
            {
                priceChange = Number(priceElem.getAttribute("value")) + (0.50 * quantElem.value);
                extrasMap.set(select, true);
            }
            // if select changed back to nothing
            else if (select.value == "")
            {
                priceChange = Number(priceElem.getAttribute("value")) - (0.50 * quantElem.value);
                extrasMap.set(select, false);
            }

            // rounding up the number to upto 2 decimal places and
            // changing the innerHTML to display the new price
            priceElem.innerHTML = "$" + (Math.round(priceChange * 100) / 100).toFixed(2);
            priceElem.setAttribute("value", priceChange);
        }

    });


});