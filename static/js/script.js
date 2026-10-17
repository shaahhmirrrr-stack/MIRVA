
// =========================
// MIRVA SHOPPING CART
// =========================

let cart =
    JSON.parse(localStorage.getItem("mirvaCart")) || [];


// =========================
// SAVE CART
// =========================

function saveCart() {

    localStorage.setItem(
        "mirvaCart",
        JSON.stringify(cart)
    );

}


// =========================
// ADD PRODUCT
// =========================

function addToCart(productName, price) {

    // Check if product already exists

    const existingProduct = cart.find(function(product) {

        return product.name === productName;

    });


    if (existingProduct) {

        existingProduct.quantity += 1;

    } else {

        cart.push({

            name: productName,
            price: price,
            quantity: 1

        });

    }


    saveCart();

    alert(productName + " added to cart!");

    displayCart();

}


// =========================
// DISPLAY CART
// =========================

function displayCart() {

    const cartItems =
        document.getElementById("cart-items");

    const cartTotal =
        document.getElementById("cart-total");


    // Only run on shop page

    if (!cartItems || !cartTotal) {

        return;

    }


    cartItems.innerHTML = "";


    // EMPTY CART

    if (cart.length === 0) {

        cartItems.innerHTML =
            "<p>Your cart is empty.</p>";

        cartTotal.innerHTML =
            "Total: Rs. 0";

        return;

    }


    let total = 0;


    // DISPLAY PRODUCTS

    cart.forEach(function(product, index) {

        // Make sure old cart products
        // have a quantity

        if (!product.quantity) {

            product.quantity = 1;

        }


        const productTotal =
            product.price * product.quantity;


        total =
            total + productTotal;


        const item =
            document.createElement("div");


        item.className = "cart-item";


        item.innerHTML = `

            <div>

                <span>
                    ${product.name}
                </span>

                <p>
                    Rs. ${product.price.toLocaleString()}
                    each
                </p>

            </div>


            <div>

                <button
                    onclick="decreaseQuantity(${index})">
                    −
                </button>


                <span style="margin: 0 15px;">
                    ${product.quantity}
                </span>


                <button
                    onclick="increaseQuantity(${index})">
                    +
                </button>

            </div>


            <div>

                <strong>
                    Rs. ${productTotal.toLocaleString()}
                </strong>

            </div>


            <button
                onclick="removeFromCart(${index})">
                REMOVE
            </button>

        `;


        cartItems.appendChild(item);

    });


    // TOTAL

    cartTotal.innerHTML =
        "Total: Rs. " +
        total.toLocaleString();


    saveCart();

}


// =========================
// INCREASE QUANTITY
// =========================

function increaseQuantity(index) {

    cart[index].quantity += 1;

    saveCart();

    displayCart();

}


// =========================
// DECREASE QUANTITY
// =========================

function decreaseQuantity(index) {

    if (cart[index].quantity > 1) {

        cart[index].quantity -= 1;

    } else {

        cart.splice(index, 1);

    }


    saveCart();

    displayCart();

}


// =========================
// REMOVE PRODUCT
// =========================

function removeFromCart(index) {

    cart.splice(index, 1);

    saveCart();

    displayCart();

}


// =========================
// CLEAR CART
// =========================

function clearCart() {

    cart = [];

    saveCart();

    displayCart();

}


// =========================
// LOAD CART
// =========================

displayCart();
