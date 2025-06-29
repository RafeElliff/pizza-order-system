import time
import pickle
from flask import Flask, render_template, request, redirect, url_for
from forms import new_order_form, fulfil_form
from order import Order, price_calc
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/order', methods = ["GET", "POST"])
def order():
    form = new_order_form(request.form)
    order_contents = {}
    margarita = 0
    pepperoni = 0
    if request.method == "POST":
        if request.form["margarita"]:
            margarita = int(request.form["margarita"])
        if request.form["pepperoni"]:
            pepperoni = int(request.form["pepperoni"])
        order_contents["margarita"] = margarita
        order_contents["pepperoni"] = pepperoni
        total_price_of_order = price_calc(order_contents)
        new_order = Order(order_contents, total_price_of_order, 2, False, time.strftime("%X"), 0)
        with open("all_orders.pkl", "rb") as f:
            all_orders = pickle.load(f)
        all_orders.append(new_order)
        with open("all_orders.pkl", "wb") as f:
            pickle.dump(all_orders, f)
    return render_template("order.html", form=form)


@app.route('/fulfil', methods = ["GET", "POST"])
def fulfil():
    form = fulfil_form(request.form)
    return render_template("fulfil.html", form = form)


if __name__ == "__main__":
    app.run(debug=True)