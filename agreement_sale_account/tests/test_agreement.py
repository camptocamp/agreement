# Copyright 2024 Camptocamp SA (https://www.camptocamp.com).
# @author: Italo Lopes <italo.lopes@camptocamp.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestAgreement(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_customer = cls.env["res.partner"].create(
            {"name": "Agreement Customer"}
        )
        cls.test_agreement_to_propagate = cls.env["agreement"].create(
            {
                "name": "Test Agreement To Propagate",
                "code": "SALE",
                "partner_id": cls.test_customer.id,
                "domain": "sale",
            }
        )
        cls.product = cls.env["product.product"].create({"name": "Test product"})
        cls.test_sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.test_customer.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100,
                        },
                    ),
                ],
            }
        )

    def test_01_agreement_propagate(self):
        self.test_sale_order.agreement_id = self.test_agreement_to_propagate
        self.test_sale_order.action_confirm()
        invoice = self.test_sale_order._create_invoices()

        self.assertEqual(invoice.agreement_id, self.test_sale_order.agreement_id)
        self.assertEqual(invoice.agreement_id, self.test_agreement_to_propagate)
