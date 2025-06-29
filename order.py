import time
def price_calc(contents):
    total_price = 0
    prices = {"margarita": 5, "pepperoni": 6}
    for product in contents:
        product_count = contents[product]
        product_price_per = prices[product]
        product_total_cost = product_price_per * product_count
        total_price = int(total_price) + int(product_total_cost)
    return total_price


class Order():
    def __init__ (self, contents, price, number, fulfilled, time_of_order, time_of_fulfilment):
        self.contents = contents
        self.price = price
        self.number = number
        self.fulfilled = fulfilled
        self.time_of_order = time_of_order
        self.time_of_fulfilment = time_of_fulfilment

    def fulfil(self):
        self.fulfilled = True
        self.time_of_fulfilment = time.strftime("%X")
