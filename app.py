
from flask import Flask, render_template, render_template_string, abort

app = Flask(__name__)

PRODUCTS = {
    "tshirt": {
        "name": "MIRVA Classic T-Shirt",
        "price": 2499,
        "image": "tshirt.png",
        "description": "Clean lines. Effortless comfort."
    },
    "hoodie": {
        "name": "MIRVA Premium Hoodie",
        "price": 4999,
        "image": "hoodie.png",
        "description": "Relaxed comfort. Refined style."
    },
    "jacket": {
        "name": "MIRVA Denim Jacket",
        "price": 6999,
        "image": "jacket.png",
        "description": "A timeless layer with attitude."
    },
    "coat": {
        "name": "MIRVA Signature Coat",
        "price": 9999,
        "image": "coat.png",
        "description": "A polished finishing layer for cooler days."
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/product/<product_id>")
def product(product_id):
    item = PRODUCTS.get(product_id)

    if item is None:
        abort(404)

    page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>{{ item.name }} | MIRVA</title>

        <style>
            * { box-sizing: border-box; }

            body {
                margin: 0;
                background: #f7f4ee;
                color: #171715;
                font-family: Arial, sans-serif;
            }

            header {
                padding: 22px 7%;
                border-bottom: 1px solid #e5e0d7;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .logo {
                font: bold 30px Georgia, serif;
                letter-spacing: 5px;
                text-decoration: none;
                color: #171715;
            }

            header a:last-child {
                color: #171715;
                text-decoration: none;
                font-size: 12px;
            }

            main {
                max-width: 1000px;
                margin: 50px auto;
                padding: 0 22px;
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 45px;
                align-items: center;
            }

            img {
                width: 100%;
                display: block;
                object-fit: contain;
                background: #e9e3d9;
                min-height: 300px;
                max-height: 550px;
            }

            .eyebrow {
                font-size: 11px;
                letter-spacing: 3px;
                color: #77746d;
            }

            h1 {
                font: normal 42px Georgia, serif;
            }

            .description {
                color: #77746d;
                line-height: 1.8;
            }

            .price {
                font-size: 20px;
                font-weight: bold;
                margin: 25px 0;
            }

            button {
                width: 100%;
                padding: 16px;
                background: #171715;
                color: white;
                border: 0;
                cursor: pointer;
            }

            button:hover {
                background: #8b7048;
            }

            .back {
                display: inline-block;
                margin-top: 22px;
                color: #171715;
            }

            #message {
                line-height: 1.7;
                font-size: 13px;
            }

            @media (max-width: 650px) {
                main {
                    grid-template-columns: 1fr;
                    margin-top: 25px;
                }

                h1 { font-size: 34px; }
            }
        </style>
    </head>

    <body>
        <header>
            <a class="logo" href="/">MIRVA</a>
            <a href="/cart">VIEW BAG 🛍</a>
        </header>

        <main>
            <div>
                <img
                    src="{{ url_for(
                        'static',
                        filename='images/' + item.image
                    ) }}"
                    alt="{{ item.name }}"
                >
            </div>

            <div>
                <p class="eyebrow">MIRVA COLLECTION</p>

                <h1>{{ item.name }}</h1>

                <p class="description">{{ item.description }}</p>

                <p class="price">
                    Rs. {{ "{:,}".format(item.price) }}
                </p>

                <button type="button" onclick="addToBag()">
                    ADD TO BAG +
                </button>

                <a class="back" href="/shop">← Continue shopping</a>

                <p id="message" aria-live="polite"></p>
            </div>
        </main>

        <script>
            const product = {
                id: {{ product_id | tojson }},
                name: {{ item.name | tojson }},
                price: {{ item.price | tojson }},
                image: {{ item.image | tojson }}
            };

            function addToBag() {
                const key = "mirvaBag";
                let bag = [];

                try {
                    const saved = JSON.parse(
                        localStorage.getItem(key) || "[]"
                    );

                    if (Array.isArray(saved)) {
                        bag = saved;
                    }
                } catch (error) {
                    bag = [];
                }

                // Convert older saved product IDs to cart items.
                bag = bag.map(entry => {
                    if (typeof entry === "string") {
                        const oldProducts = {
                            tshirt: {
                                id: "tshirt",
                                name: "MIRVA Classic T-Shirt",
                                price: 2499,
                                image: "tshirt.png"
                            },
                            hoodie: {
                                id: "hoodie",
                                name: "MIRVA Premium Hoodie",
                                price: 4999,
                                image: "hoodie.png"
                            },
                            jacket: {
                                id: "jacket",
                                name: "MIRVA Denim Jacket",
                                price: 6999,
                                image: "jacket.png"
                            },
                            coat: {
                                id: "coat",
                                name: "MIRVA Signature Coat",
                                price: 9999,
                                image: "coat.png"
                            }
                        };

                        const oldItem = oldProducts[entry];

                        if (oldItem) {
                            return {
                                ...oldItem,
                                quantity: 1
                            };
                        }

                        return null;
                    }

                    return entry;
                }).filter(Boolean);

                const existing = bag.find(entry =>
                    entry.id === product.id
                );

                if (existing) {
                    existing.quantity += 1;
                } else {
                    bag.push({
                        ...product,
                        quantity: 1
                    });
                }

                localStorage.setItem(key, JSON.stringify(bag));

                document.getElementById("message").innerHTML =
                    "Added to your bag! " +
                    '<a href="/cart">View your bag →</a>';
            }
        </script>
    </body>
    </html>
    """

    return render_template_string(
        page,
        item=item,
        product_id=product_id
    )


@app.route("/cart")
def cart():
    page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">

        <title>Your Bag | MIRVA</title>

        <style>
            * { box-sizing: border-box; }

            body {
                margin: 0;
                background: #f7f4ee;
                color: #171715;
                font-family: Arial, sans-serif;
            }

            header {
                padding: 22px 7%;
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 1px solid #e5e0d7;
            }

            header a {
                color: #171715;
                text-decoration: none;
            }

            .logo {
                font: bold 30px Georgia, serif;
                letter-spacing: 5px;
            }

            main {
                max-width: 950px;
                margin: 50px auto;
                padding: 0 22px;
            }

            h1 {
                font: normal 40px Georgia, serif;
                margin-bottom: 10px;
            }

            .subtitle {
                color: #77746d;
                margin-bottom: 35px;
            }

            .item {
                display: grid;
                grid-template-columns: 110px 1fr auto;
                gap: 22px;
                align-items: center;
                padding: 22px 0;
                border-bottom: 1px solid #ded8ce;
            }

            .item img {
                width: 110px;
                height: 125px;
                object-fit: cover;
                background: #e9e3d9;
            }

            .item h3 {
                margin: 0 0 10px;
                font-size: 16px;
            }

            .item p {
                color: #77746d;
                font-size: 13px;
                line-height: 1.7;
                margin: 5px 0;
            }

            .remove {
                margin-top: 8px;
                border: none;
                background: transparent;
                padding: 0;
                color: #8a3e32;
                cursor: pointer;
                text-decoration: underline;
            }

            .summary {
                max-width: 360px;
                margin: 35px 0 0 auto;
            }

            .total {
                display: flex;
                justify-content: space-between;
                font-size: 18px;
                font-weight: bold;
                padding: 20px 0;
                border-bottom: 1px solid #ded8ce;
            }

            .button {
                display: block;
                width: 100%;
                margin-top: 20px;
                padding: 16px;
                text-align: center;
                background: #171715;
                color: white;
                text-decoration: none;
                border: none;
                cursor: pointer;
            }

            .secondary {
                background: transparent;
                color: #171715;
                border: 1px solid #cfc7bb;
            }

            .empty {
                padding: 35px 0;
                color: #77746d;
                line-height: 1.8;
            }

            footer {
                margin-top: 60px;
                padding: 28px;
                text-align: center;
                border-top: 1px solid #e5e0d7;
                color: #77746d;
                font-size: 11px;
                letter-spacing: 2px;
            }

            @media (max-width: 550px) {
                .item {
                    grid-template-columns: 80px 1fr;
                    gap: 14px;
                }

                .item img {
                    width: 80px;
                    height: 100px;
                }

                .item-price {
                    grid-column: 2;
                }

                h1 { font-size: 33px; }
            }
        </style>
    </head>

    <body>
        <header>
            <a class="logo" href="/">MIRVA</a>
            <a href="/shop">← CONTINUE SHOPPING</a>
        </header>

        <main>
            <h1>Your Shopping Bag</h1>

            <p class="subtitle">
                Your selected MIRVA pieces, all in one place.
            </p>

            <div id="items"></div>

            <div id="summary" class="summary" hidden>
                <div class="total">
                    <span>Subtotal</span>
                    <span id="total">Rs. 0</span>
                </div>

                <p style="color:#77746d;font-size:12px;line-height:1.7;">
                    Delivery charges, if applicable, are not included.
                </p>

                <a class="button" href="/checkout">PROCEED TO CHECKOUT</a>

                <button class="button secondary" onclick="clearBag()">
                    CLEAR BAG
                </button>
            </div>
        </main>

        <footer>
            MIRVA — WHERE STYLE SPEAKS.
        </footer>

        <script>
            const products = {{ products | tojson }};

            function getBag() {
                try {
                    const bag = JSON.parse(
                        localStorage.getItem("mirvaBag") || "[]"
                    );

                    if (!Array.isArray(bag)) return [];

                    return bag.map(entry => {
                        // Support older saved product IDs.
                        if (typeof entry === "string") {
                            const oldItem = products[entry];

                            if (!oldItem) return null;

                            return {
                                id: entry,
                                ...oldItem,
                                quantity: 1
                            };
                        }

                        return entry;
                    }).filter(entry =>
                        entry &&
                        products[entry.id] &&
                        Number.isInteger(entry.quantity) &&
                        entry.quantity > 0
                    );
                } catch (error) {
                    return [];
                }
            }

            function saveBag(bag) {
                localStorage.setItem("mirvaBag", JSON.stringify(bag));
            }

            function renderBag() {
                const bag = getBag();
                const items = document.getElementById("items");
                const summary = document.getElementById("summary");

                items.innerHTML = "";

                if (bag.length === 0) {
                    items.innerHTML =
                        '<div class="empty">' +
                        '<p>Your bag is currently empty.</p>' +
                        '<a href="/shop">Explore the MIRVA collection →</a>' +
                        '</div>';

                    summary.hidden = true;
                    return;
                }

                let subtotal = 0;

                bag.forEach(item => {
                    const details = products[item.id];
                    const price = details.price;
                    subtotal += price * item.quantity;

                    const row = document.createElement("div");
                    row.className = "item";

                    const image = document.createElement("img");
                    image.src = "/static/images/" + details.image;
                    image.alt = details.name;

                    const info = document.createElement("div");

                    const name = document.createElement("h3");
                    name.textContent = details.name;

                    const quantity = document.createElement("p");
                    quantity.textContent = "Quantity: " + item.quantity;

                    const remove = document.createElement("button");
                    remove.className = "remove";
                    remove.textContent = "Remove";
                    remove.onclick = () => removeItem(item.id);

                    info.append(name, quantity, remove);

                    const priceLabel = document.createElement("div");
                    priceLabel.className = "item-price";
                    priceLabel.textContent =
                        "Rs. " + (price * item.quantity).toLocaleString("en-PK");

                    row.append(image, info, priceLabel);
                    items.appendChild(row);
                });

                document.getElementById("total").textContent =
                    "Rs. " + subtotal.toLocaleString("en-PK");

                summary.hidden = false;
            }

            function removeItem(id) {
                const bag = getBag().filter(item => item.id !== id);
                saveBag(bag);
                renderBag();
            }

            function clearBag() {
                if (confirm("Are you sure you want to clear your bag?")) {
                    localStorage.removeItem("mirvaBag");
                    renderBag();
                }
            }

            renderBag();
        </script>
    </body>
    </html>
    """

    return render_template_string(page, products=PRODUCTS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


if __name__ == "__main__":
    app.run(debug=True)
