from file_handler import FileHandler


class Manager:
    def __init__(self, history_file, data_file):
        self.actions = {}
        self.file_handler = FileHandler(data_file=data_file, history_file=history_file)
        self.data = self.file_handler.load_data_from_data_file()
        self.book = self.file_handler.load_history_from_history_file()
        self.list_dict = self.data.get("magazyn")
        self.account = self.data.get("saldo")

    def change_saldo(self, balance):
        if balance > self.account:
            return False
        manager.account += balance
        manager.book.append(f"Zmiana na koncie o kwote {balance} ")
        return True

    def show_history(self, od, do):
        return self.book[od:do]

    def show_all_history(self):
        return self.book

    def save_app_context(self):
        self.file_handler.save_data_to_data_file({
            "magazyn": self.list_dict,
            "saldo": self.account
        })
        self.file_handler.save_history_to_history_file(self.book)

    def sell_product(self, data):
        product_name = data.get("product")
        found_product = False
        for product in self.list_dict:
            if product.get("przedmiot") == product_name:
                found_product = True
                quantity = int(data.get("quantity"))
                price = int(product.get("cena"))
                if product.get("ilosc") >= quantity:
                    product["ilosc"] -= quantity
                    self.account += price * quantity
                    manager.book.append(f"Sprzedaz {product_name} w ilosci {quantity} ")
                    return True
                else:
                    return False
        if not found_product:
            return False

    def buy_product(self, data):
        product_name = data.get("buy_product")
        quantity = int(data.get("buy_quantity"))
        price = int(data.get("buy_price"))
        if price < 0 or quantity < 0:
            return False
        found = False
        for product in self.list_dict:
            if product["przedmiot"] == product_name:
                product["ilosc"] += quantity
                found = True
                break
        if not found:
            self.list_dict.append({
                "przedmiot": product_name,
                "cena": price,
                "ilosc": quantity
            })
        if self.account >= quantity * price:
            self.account -= quantity * price
            manager.book.append(f"Zakup {product_name} w ilosci {quantity}")
            return True
        return False


manager = Manager(history_file="dziennik.json", data_file="dane.json")
