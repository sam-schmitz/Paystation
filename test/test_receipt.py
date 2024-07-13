# test_receipt.py

import unittest
from io import StringIO

from paystation.domain import Receipt


class TestReceipt(unittest.TestCase):

    def setUp(self):
        self.stdrec = Receipt(30)

    def validate_common_portions(self, lines):
        self.assertEqual("-"*50, lines[0])
        self.assertEqual("-"*7, lines[1][:7])
        self.assertEqual("-"*7, lines[1][-7:])
        self.assertEqual(50, len(lines[1]))
        self.assertIn("P A R K I N G   R E C E I P T", lines[1])
        self.assertIn("Value 030 minutes.", lines[2])
        self.assertIn("Car parked at", lines[3])
        parked_at_str = lines[3][28:33]
        int(parked_at_str[:2])
        self.assertEqual(":", parked_at_str[2])
        int(parked_at_str[3:5])
        self.assertEqual("-"*50, lines[4])

    def test_receipt_stores_value(self):
        self.assertEqual(30, self.stdrec.value)

    def test_prints_correct_standard_receipt(self):
        stream = StringIO()
        self.stdrec.print(stream)
        lines = stream.getvalue().split("\n")
        self.assertEqual(6, len(lines))
        self.validate_common_portions(lines)
        self.assertEqual("", lines[5])

    def test_prints_receipt_with_barcode(self):
        bcrec = Receipt(30, barcode=True)
        stream = StringIO()
        bcrec.print(stream)
        lines = stream.getvalue().split("\n")
        self.assertEqual(7, len(lines))
        self.validate_common_portions(lines)
        self.assertIn("|", lines[5])
        self.assertIn(" ", lines[5])
        self.assertEqual("", lines[6])
