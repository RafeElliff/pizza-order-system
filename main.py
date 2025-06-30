import time
import pickle
from flask import Flask, render_template, request, redirect, url_for
from forms import new_order_form, fulfil_form
from order import Order, price_calc

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/order', methods=["GET", "POST"])
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
        new_order = Order(order_contents, total_price_of_order, 0, False, time.strftime("%X"), 0)
        with open("all_orders.pkl", "rb") as f:
            all_orders = pickle.load(f)
        new_order.number = len(all_orders) + 1
        all_orders.append(new_order)
        with open("all_orders.pkl", "wb") as f:
            pickle.dump(all_orders, f)
        with open("current_orders.pkl", "wb") as f:
            pickle.dump(all_orders, f)
        return redirect(url_for("order"))
    return render_template("order.html", form=form)


@app.route('/fulfil', methods=["GET", "POST"])
def fulfil():
    form = fulfil_form(request.form)
    with open("current_orders.pkl", "rb") as f:
        current_orders = pickle.load(f)
    current_order_numbers = []
    for item in current_orders:
        current_order_numbers.append(item.number)
    form.order_to_fulfil.choices = current_order_numbers
    if request.method == "POST":
        order_number_to_fulfil = int(request.form["order_to_fulfil"])
        for order in current_orders:
            if int(order.number) == order_number_to_fulfil:
                current_orders.remove(order)
            with open("current_orders.pkl", "wb") as f:
                pickle.dump(current_orders, f)
        return redirect(url_for("fulfil"))
    return render_template("fulfil.html", form=form)


@app.route("/wipe_history")
def wipe_history():
    with open("all_orders.pkl", "wb") as f:
        pickle.dump([], f)
    with open("current_orders.pkl", "wb") as f:
        pickle.dump([], f)
    return redirect(url_for("debug"))

@app.route("/debug")
def debug():
    return render_template("debug.html")


if __name__ == "__main__":
    app.run(debug=True)
