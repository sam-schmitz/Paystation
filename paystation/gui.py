# gui.py


import tkinter as tk
import sys
sys.path.insert(0, '..')  # fix to allow imorts from paystation module
from io import StringIO

from paystation.domain import PayStation
from paystation.config import AlphaTownFactory, BetaTownFactory, GammaTownFactory, TripoliFactory

from paystation.guiview import PayStationGUIview

# Configuration of PayStations to appear in the GUI
FACTORIES = [AlphaTownFactory(), BetaTownFactory(),
             GammaTownFactory(), TripoliFactory()]


class MultiPayStationModel:
    """ Model for PayStationGUIApp"""

    def __init__(self):
        self._factories = []
        self.config_id = None
        self.paystation_labels = []

    def add_paystation(self, factory):
        self._factories.append(factory)
        self.paystation_labels.append(factory.config_id)

    def set_paystation(self, config_id):
        self.config_id = config_id
        self.ps = PayStation(self._factories[self.paystation_labels.index(config_id)])

    def add_payment(self, amount):
        self.ps.add_payment(amount)

    def read_display(self):
        return self.ps.read_display()

    def buy(self):
        return self.ps.buy()

    def cancel(self):
        self.ps.cancel()

class PayStationGUIApp:
    """ Presenter for the PayStation GUI """

    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view
        self.view.set_controller(self)
        self.state = dict(accept_select_paystation=True,
             accept_transaction=False,
             accept_coin=False,
             variant='Select Variant',
             display=''
             )
        self.view.set_state(self.state)
        self.view.set_labels(self.model.paystation_labels)

    def run(self):
        self.root.title("Paystation Simulator")
        self.root.deiconify()
        self.root.mainloop()

    def select_paystation(self, config_id):
        self.config_id = config_id
        self.model.set_paystation(config_id)
        self.state["accept_coin"] = True
        self.state["variant"] = config_id
        self.state["display"] = self.model.read_display()
        self.view.set_state(self.state)

    def coin(self, amount):
        self.model.add_payment(amount)
        self.state["accept_select_paystation"] = False
        self.state["accept_transaction"] = True
        self.state["display"] = self.model.read_display()
        self.view.set_state(self.state)

    def transaction(self, type):
        self.state["accept_select_paystation"] = True
        self.state["accept_transaction"] = False
        self.state["accept_coin"] = True
        if type == "cancel":
            self.model.cancel()
            self.state["display"] = self.model.read_display()
            self.view.set_state(self.state)
        elif type == "buy":
            receipt = self.model.buy()
            stream = StringIO()
            receipt.print(stream)
            self.state["display"] = self.model.read_display()
            self.view.show_receipt(stream.getvalue())
            self.view.set_state(self.state)


def main():
    root = tk.Tk()
    view = PayStationGUIview(root)
    model = MultiPayStationModel()
    for factory in FACTORIES:
        model.add_paystation(factory)
    PayStationGUIApp(root, model, view).run()


if __name__ == "__main__":
    main()
