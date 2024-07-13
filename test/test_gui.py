# test_gui.py

import unittest
from unittest.mock import Mock
import tkinter as tk

from paystation.gui import (MultiPayStationModel,
                            PayStationGUIApp
                            )
from paystation.guiview import PayStationGUIview


class FakeFactory1:
    config_id = "Fake1"

    class FakeReceipt:
        def print(self, stream):
            print("Fake Receipt 1", file=stream)

    def create_rate_strategy(self):
        def frs1(amt):
            return amt
        return frs1

    def create_receipt(self, amt):
        return self.FakeReceipt()


class FakeFactory2:
    config_id = "Fake2"

    class FakeReceipt:
        def print(self, stream):
            print("Fake Receipt 2", file=stream)

    def create_rate_strategy(self):
        def frs2(amt):
            return 2 * amt
        return frs2

    def create_receipt(self, amt):
        return self.FakeReceipt()


class TestMultiPayStationModel(unittest.TestCase):

    def setUp(self):
        self.model = MultiPayStationModel()
        self.model.add_paystation(FakeFactory1())
        self.model.add_paystation(FakeFactory2())

    def test_initially_no_paystation(self):
        self.assertIsNone(self.model.config_id)

    def test_paystion_labels(self):
        self.assertEqual(self.model.paystation_labels,
                         ["Fake1", "Fake2"])

    def test_configures_to_paystation(self):
        self.model.set_paystation("Fake1")
        self.assertEqual(self.model.config_id, "Fake1")
        self.model.set_paystation("Fake2")
        self.assertEqual(self.model.config_id, "Fake2")

    def test_delegates_add_payment(self):
        self.model.set_paystation("Fake1")
        self.model.add_payment(25)
        self.assertEqual(25, self.model.read_display())
        self.model.set_paystation("Fake2")
        self.model.add_payment(25)
        self.assertEqual(50, self.model.read_display())

    def test_switch_gets_new_paystation(self):
        self.model.set_paystation("Fake1")
        self.model.add_payment(25)
        self.model.set_paystation("Fake2")
        self.model.set_paystation("Fake1")
        self.assertEqual(0, self.model.read_display())

    def test_delegates_buy(self):
        self.model.set_paystation("Fake1")
        self.model.add_payment(25)
        rec = self.model.buy()
        self.assertIsInstance(rec, FakeFactory1.FakeReceipt)
        self.model.set_paystation("Fake2")
        self.model.add_payment(25)
        rec = self.model.buy()
        self.assertIsInstance(rec, FakeFactory2.FakeReceipt)

    def test_delegates_cancel(self):
        self.model.set_paystation("Fake1")
        self.model.add_payment(25)
        self.model.cancel()
        self.assertEqual(0, self.model.read_display())


class Test_PayStationGUIApp(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.view = Mock()
        self.model = MultiPayStationModel()
        self.model.add_paystation(FakeFactory1())
        self.model.add_paystation(FakeFactory2())
        self.app = PayStationGUIApp(root, self.model, self.view)

    def test_sets_up_view_correctly(self):
        self.view.set_controller.assert_called_once_with(self.app)
        self.view.set_state.assert_called_once_with(
            dict(accept_select_paystation=True,
                 accept_transaction=False,
                 accept_coin=False,
                 variant='Select Variant',
                 display=''
                 )
            )
        self.view.set_labels.assert_called_once_with(["Fake1", "Fake2"])

    def test_handles_variant_selection(self):
        self.app.select_paystation("Fake2")
        self.assertEqual(self.model.config_id, "Fake2")
        self.view.set_state.assert_called_with(
            dict(accept_select_paystation=True,
                 accept_transaction=False,
                 accept_coin=True,
                 variant='Fake2',
                 display=self.model.read_display()
                 )
            )

    def test_handles_nickel(self):
        self.app.select_paystation("Fake2")
        self.app.coin(5)
        self.assertEqual(10, self.model.read_display())
        self.view.set_state.assert_called_with(
            dict(accept_select_paystation=False,
                 accept_transaction=True,
                 accept_coin=True,
                 variant='Fake2',
                 display=self.model.read_display()
                 )
            )

    def test_handles_dime(self):
        self.app.select_paystation("Fake2")
        self.app.coin(10)
        self.assertEqual(20, self.model.read_display())
        self.view.set_state.assert_called_with(
            dict(accept_select_paystation=False,
                 accept_transaction=True,
                 accept_coin=True,
                 variant='Fake2',
                 display=self.model.read_display()
                 )
            )

    def test_handles_quarter(self):
        self.app.select_paystation("Fake2")
        self.app.coin(25)
        self.assertEqual(50, self.model.read_display())
        self.view.set_state.assert_called_with(
            dict(accept_select_paystation=False,
                 accept_transaction=True,
                 accept_coin=True,
                 variant='Fake2',
                 display=self.model.read_display()
                 )
            )

    def test_handles_cancel(self):
        self.app.select_paystation("Fake2")
        self.app.coin(25)
        self.app.transaction("cancel")
        self.assertEqual(0, self.model.read_display())
        self.view.set_state.assert_called_with(
            dict(accept_select_paystation=True,
                 accept_transaction=False,
                 accept_coin=True,
                 variant='Fake2',
                 display=self.model.read_display()
                 )
            )

    def test_handles_buy(self):
        self.app.select_paystation("Fake2")
        self.app.coin(25)
        self.app.transaction("buy")
        self.view.show_receipt.assert_called_once_with("Fake Receipt 2\n")
        self.assertEqual(0, self.model.read_display())
        self.view.set_state.assert_called_with(
            dict(accept_select_paystation=True,
                 accept_transaction=False,
                 accept_coin=True,
                 variant='Fake2',
                 display=self.model.read_display()
                 )
             )



class Test_GUIView(unittest.TestCase):

    def setUp(self):
        root = tk.Tk()
        self.view = PayStationGUIview(root)

    def test_set_state(self):
        self.view.set_state(
            dict(accept_select_paystation=True,
                 accept_transaction=True,
                 accept_coin=True,
                 variant='Alphatown',
                 display=0
                 )
            )
        self.assertEqual(str(self.view.variant_selector["state"]), "normal")

        self.assertEqual(str(self.view.b_buy["state"]), "normal")
        self.assertEqual(str(self.view.b_cancel["state"]), "normal")

        self.assertEqual(str(self.view.b_5_c["state"]), "normal")
        self.assertEqual(str(self.view.b_10_c["state"]), "normal")
        self.assertEqual(str(self.view.b_25_c["state"]), "normal")

        self.assertEqual(self.view.variant_selector["text"], "Alphatown")
        self.assertEqual(self.view.display["text"], '0')

        self.view.set_state(
            dict(accept_select_paystation=False,
                 accept_transaction=False,
                 accept_coin=False,
                 variant='Betatown',
                 display=1
                 )
            )

        self.assertEqual(str(self.view.variant_selector["state"]), "disabled")

        self.assertEqual(str(self.view.b_buy["state"]), "disabled")
        self.assertEqual(str(self.view.b_cancel["state"]), "disabled")

        self.assertEqual(str(self.view.b_5_c["state"]), "disabled")
        self.assertEqual(str(self.view.b_10_c["state"]), "disabled")
        self.assertEqual(str(self.view.b_25_c["state"]), "disabled")

        self.assertEqual(self.view.variant_selector["text"], "Betatown")
        self.assertEqual(self.view.display["text"], '1')

    def test_coin_buttons(self):
        controller = Mock()
        self.view.set_controller(controller)
        self.view.b_5_c.invoke()
        controller.coin.assert_called_once_with(5)
        self.view.b_10_c.invoke()
        controller.coin.assert_called_with(10)
        self.view.b_25_c.invoke()
        controller.coin.assert_called_with(25)

    def test_transaction_buttons(self):
        controller = Mock()
        self.view.set_controller(controller)
        self.view.b_buy.invoke()
        controller.transaction.called_once_with("buy")
        self.view.b_cancel.invoke()
        controller.transaction.called_with("cancel")

    def test_set_labels(self):
        self.view.set_labels(["town1", "town2"])
        self.assertEqual(self.view.variant_menu.entrycget(0, "label"), "town1")
        self.assertEqual(self.view.variant_menu.entrycget(1, "label"), "town2")

    def test_variant_selection(self):
        controller = Mock()
        self.view.set_controller(controller)
        self.view.set_labels(["town1", "town2"])
        self.view.variant_menu.invoke(0)
        controller.select_paystation.assert_called_once_with("town1")
        self.view.variant_menu.invoke(1)
        controller.select_paystation.assert_called_with("town2")
