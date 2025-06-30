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
        if margarita == 0 and pepperoni == 0:
            return redirect(url_for("order"))
        order_contents["margarita"] = margarita
        order_contents["pepperoni"] = pepperoni
        total_price_of_order = price_calc(order_contents)
        new_order = Order(order_contents, total_price_of_order, -1, False, False, time.strftime("%X"), 0, time.time())
        with open("all_orders.pkl", "rb") as f:
            all_orders = pickle.load(f)
        new_order.number = len(all_orders) + 1
        all_orders.append(new_order)
        with open("all_orders.pkl", "wb") as f:
            pickle.dump(all_orders, f)
        # with open("current_orders.pkl", "rb") as f:
        #     current_orders = pickle.load(f)
        # current_orders.append(new_order)
        # with open("current_orders.pkl", "wb") as f:
        #     pickle.dump(current_orders, f)
        return redirect(url_for("order"))
    return render_template("order.html", form=form)


@app.route('/fulfil', methods=["GET", "POST"])
def fulfil():
    form = fulfil_form(request.form)
    with open("all_orders.pkl", "rb") as f:
        all_orders = pickle.load(f)
    current_orders = []
    for order in all_orders:
        if order.fulfilled is False or order.collected is False:
            current_orders.append(order)
    options_to_fulfil = ['']
    options_to_collect = ['']
    for order in current_orders:
        if order.fulfilled is False:
            options_to_fulfil.append(order.number)
        elif order.fulfilled is True and order.collected is False:
            options_to_collect.append(order.number)
    form.order_to_fulfil.choices = options_to_fulfil
    form.order_to_fulfil.default = ''
    form.order_to_collect.choices = options_to_collect
    form.order_to_collect.default = ''
    if request.method == "POST":
        if request.form.get("order_to_fulfil"):
            order_number_to_fulfil = int(request.form["order_to_fulfil"])
            for order in current_orders:
                if order.number == order_number_to_fulfil:
                    order.fulfil()
        elif request.form.get("order_to_collect"):
            order_number_to_collect = int(request.form["order_to_collect"])
            for order in current_orders:
                if order.number == order_number_to_collect:
                    order.collected = True
        with open("all_orders.pkl", "wb") as f:
            pickle.dump(all_orders, f)
        return redirect(url_for("fulfil"))

    return render_template("fulfil.html", form=form)

@app.route("/view_orders")
def view_orders():
    completed_orders = []
    uncompleted_orders = []
    with open("all_orders.pkl", "rb") as f:
        all_orders = pickle.load(f)
    for order in all_orders:
        if order.fulfilled is True and order.collected is False:
            completed_orders.append(order.number)
            completed_orders.sort()
        elif order.collected is False:
            uncompleted_orders.append(order.number)
            uncompleted_orders.sort()
    return render_template("view_orders.html", completed_orders = completed_orders, uncompleted_orders = uncompleted_orders)

@app.route("/wipe_history")
def wipe_history():
    with open("all_orders.pkl", "wb") as f:
        pickle.dump([], f)
    return redirect(url_for("debug"))


@app.route("/see_all_data")
def see_all_data():
    with open("all_orders.pkl", "rb") as f:
        all_orders = pickle.load(f)
    return render_template("see_all_data.html", all_orders=all_orders)

@app.route("/debug")
def debug():
    return render_template("debug.html")


if __name__ == "__main__":
    app.run(debug=True)
