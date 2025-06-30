from wtforms import Form, IntegerField, SubmitField, SelectField


class new_order_form(Form):
    margarita = IntegerField("Margarita")
    pepperoni = IntegerField("Pepperoni")
    submit = SubmitField("Submit")

class fulfil_form(Form):
    order_to_fulfil = SelectField("Which order to fulfil", choices=[])
    order_to_collect = SelectField("Which order to collect", choices=[])
    submit = SubmitField("Submit")