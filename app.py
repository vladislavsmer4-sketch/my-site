from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "my-secret-key"


products = [
    {"name": "Сигара", "price": 500},
    {"name": "Тютюн", "price": 300},
    {"name": "Запальничка", "price": 250},
    {"name": "Попільничка", "price": 400},
    {"name": "Сигарний футляр", "price": 800},
]


# ===== МОВА САЙТУ =====

@app.context_processor
def inject_language():
    language = session.get("language", "uk")
    return {"language": language}


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
    return render_template("catalog.html")


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