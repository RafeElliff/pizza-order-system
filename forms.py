from wtforms import Form, IntegerField, SubmitField, SelectField


class new_order_form(Form):
    margarita = IntegerField("Margarita")
    pepperoni = IntegerField("Pepperoni")
    submit = SubmitField("Submit")

class fulfil_form(Form):
    order_to_fulfil = SelectField("Which order to fulfil")
    submit = SubmitField("Submit")