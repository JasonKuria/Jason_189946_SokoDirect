// static/js/cart.js
var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(e){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('Processing Product ID:', productId, '|| Action:', action)

        if (user === 'AnonymousUser' || user === '' || user === 'None'){
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action){
    console.log('Sending update to server...')

    var url = '/orders/update_item/' 

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken 
        }, 
        body: JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) => {
        if (!response.ok) {
            console.error('Server rejected the request with status:', response.status);
        }
        return response.json();
    })
    .then((data) => {
        console.log('Server reports success:', data);
        location.reload();
    })
    .catch((error) => {
        console.error('Network or parsing error encountered:', error);
    });
}

function addCookieItem(productId, action){
    if (action == 'add'){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove' || action == 'delete_item'){
        // Defensive check: only remove if the item exists in the cookie cart
        if (cart[productId] != undefined) {
            if (action == 'delete_item' || cart[productId]['quantity'] <= 1){
                console.log('Removing element from cookie key references.')
                delete cart[productId];
            } else {
                cart[productId]['quantity'] -= 1
            }
        }
    }
    
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}