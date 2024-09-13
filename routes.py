from flask import Blueprint, render_template, request
from manager import manager


my_blueprint = Blueprint("my_blueprint", __name__)


@my_blueprint.route("/", methods=["GET", "POST"])
def main_view():
    if request.method == "GET":
        return render_template("magazyn.html", manager=manager.list_dict, saldo=manager.account)
    elif request.method == "POST":
        form_type = request.form.get("form_type")
        print(form_type)

        valid_data = None
        if form_type == "change_saldo":
            balance = request.form.get("kwota")
            valid_data = manager.change_saldo(float(balance))
        elif form_type == "sale":
            valid_data = manager.sell_product(request.form)
        else:
            valid_data = manager.buy_product(request.form)
        manager.save_app_context()
        if valid_data is not None and valid_data:
            return render_template("magazyn.html", manager=manager.list_dict, saldo=manager.account)
        else:
            return "Bład, nie znaleziono"


@my_blueprint.route("/history")
def show_all_history():
    data = manager.show_all_history()
    return render_template("historia.html", historia=data)


@my_blueprint.route("/history/<from_date>/<to_date>")
def show_history(from_date, to_date):
    try:
        from_date = int(from_date)
        to_date = int(to_date)
        if from_date < 0 or to_date > len(manager.book) or from_date > to_date:
            return f"Podany błedny zakres. Suma operacji to {len(manager.book)}"

        data = manager.show_history(int(from_date), int(to_date))
        return render_template("historia.html", historia=data)
    except ValueError:
        return "Bład"
