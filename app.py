from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "my-secret-key"


# ===== ТОВАРИ =====

products = [
    {"id": 1, "name": "Premium Cigar", "price": 850},
    {"id": 2, "name": "Havana Reserve", "price": 1200},
    {"id": 3, "name": "Royal Collection", "price": 1500},
    {"id": 4, "name": "Black Label", "price": 1050},
]


# ===== МОВА САЙТУ =====

@app.context_processor
def inject_language():

    language = session.get("language", "uk")

    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return {
        "language": language,
        "cart_count": cart_count
    }


@app.route("/set-language/<language>")
def set_language(language):

    if language in ["uk", "en"]:
        session["language"] = language

    return redirect(request.referrer or "/")


# ===== ГОЛОВНА =====

@app.route("/")
def home():
    return render_template("index.html")


# ===== КАТЕГОРІЇ =====

@app.route("/categories")
def categories():
    return render_template("categories.html")


# ===== КАТАЛОГ =====

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", products=products)


# ===== ДОДАТИ В КОШИК =====

@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session["cart"] = cart
    session.modified = True

    return redirect(request.referrer or "/catalog")


# ===== ЗБІЛЬШИТИ КІЛЬКІСТЬ =====

@app.route("/increase-cart/<int:product_id>", methods=["POST"])
def increase_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    session["cart"] = cart
    session.modified = True

    return redirect("/cart")


# ===== ЗМЕНШИТИ КІЛЬКІСТЬ =====

@app.route("/decrease-cart/<int:product_id>", methods=["POST"])
def decrease_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect("/cart")


# ===== КОШИК =====

@app.route("/cart")
def cart():

    cart = session.get("cart", {})

    cart_products = []
    total = 0

    for product in products:

        product_id = str(product["id"])

        if product_id in cart:

            quantity = cart[product_id]

            item_total = product["price"] * quantity

            cart_products.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "total": item_total
            })

            total += item_total

    return render_template(
        "cart.html",
        cart_products=cart_products,
        total=total
    )


# ===== ВИДАЛИТИ З КОШИКА =====

@app.route("/remove-from-cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect("/cart")


# ===== ОЧИСТИТИ КОШИК =====

@app.route("/clear-cart", methods=["POST"])
def clear_cart():

    session["cart"] = {}
    session.modified = True

    return redirect("/cart")


# ===== ОФОРМЛЕННЯ ЗАМОВЛЕННЯ =====

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    cart = session.get("cart", {})

    if not cart:
        return redirect("/cart")

    cart_products = []
    total = 0

    for product in products:

        product_id = str(product["id"])

        if product_id in cart:

            quantity = cart[product_id]

            item_total = product["price"] * quantity

            cart_products.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": quantity,
                "total": item_total
            })

            total += item_total


    if request.method == "POST":

        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        city = request.form.get("city", "").strip()
        address = request.form.get("address", "").strip()
        comment = request.form.get("comment", "").strip()

        # Поки що просто зберігаємо дані замовлення в session.
        session["order"] = {
            "name": name,
            "phone": phone,
            "email": email,
            "city": city,
            "address": address,
            "comment": comment,
            "cart_products": cart_products,
            "total": total
        }

        return redirect("/order-success")


    return render_template(
        "checkout.html",
        cart_products=cart_products,
        total=total
    )


# ===== ЗАМОВЛЕННЯ УСПІШНО ОФОРМЛЕНО =====

@app.route("/order-success")
def order_success():

    order = session.get("order")

    if not order:
        return redirect("/catalog")

    return render_template(
        "order-success.html",
        order=order
    )


# ===== ПРО НАС =====

@app.route("/about")
def about():
    return render_template("about.html")


# ===== КОНТАКТИ =====

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")


# ===== ВХІД =====

@app.route("/login")
def login():
    return render_template("login.html")


# ===== РЕЄСТРАЦІЯ =====

@app.route("/register")
def register():
    return render_template("register.html")


# ===== ПОШУК =====

@app.route("/search")
def search():

    query = request.args.get("q", "").strip()

    results = [
        product
        for product in products
        if query.lower() in product["name"].lower()
    ]

    return render_template(
        "search.html",
        query=query,
        results=results
    )


# ===== ЗАПУСК =====

if __name__ == "__main__":
    app.run(debug=True)
