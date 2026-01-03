# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestSaleLineMarginPrice(TransactionCase):
    """
    Test suite for sale_line_margin_price module.
    Tests automatic price calculation based on product cost + margin %.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test data: product, customer, and sale order.
        This runs once for all test methods in this class.
        """
        super().setUpClass()

        # Create a product with a known cost
        cls.product_desk = cls.env['product.product'].create({
            'name': 'Test Desk',
            'type': 'consu',
            'standard_price': 100.0,  # Cost = 100
            'list_price': 150.0,
        })

        # Create a product with zero cost for edge case testing
        cls.product_zero_cost = cls.env['product.product'].create({
            'name': 'Test Zero Cost Product',
            'type': 'consu',
            'standard_price': 0.0,  # Cost = 0
            'list_price': 0.0,
        })

        # Create a test customer
        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Customer',
            'email': 'test@customer.com',
        })

        # Create a sale order in draft state
        cls.sale_order = cls.env['sale.order'].create({
            'partner_id': cls.partner.id,
            'state': 'draft',
        })

    def test_01_default_margin_on_new_line(self):
        """
        Test that a new sale order line gets the default margin (20%)
        and calculates price correctly.
        Expected: price_unit = 100 * (1 + 20/100) = 120.0
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
        })

        # Default margin should be 20%
        self.assertAlmostEqual(
            line.margin_percent,
            20.0,
            places=2,
            msg="Default margin should be 20%"
        )

        # Price should be: 100 * (1 + 20/100) = 120
        self.assertAlmostEqual(
            line.price_unit,
            120.0,
            places=2,
            msg="Price should be 120.0 with 20% margin on cost of 100"
        )

        # Cost price should be computed correctly
        self.assertAlmostEqual(
            line.cost_price,
            100.0,
            places=2,
            msg="Cost price should equal product standard_price"
        )

    def test_02_custom_margin_on_create(self):
        """
        Test creating a line with a custom margin (50%).
        Expected: price_unit = 100 * (1 + 50/100) = 150.0
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 50.0,
        })

        self.assertAlmostEqual(
            line.margin_percent,
            50.0,
            places=2,
            msg="Margin should be 50%"
        )

        self.assertAlmostEqual(
            line.price_unit,
            150.0,
            places=2,
            msg="Price should be 150.0 with 50% margin on cost of 100"
        )

    def test_03_margin_100_percent(self):
        """
        Test 100% margin calculation.
        Expected: price_unit = 100 * (1 + 100/100) = 200.0
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 100.0,
        })

        self.assertAlmostEqual(
            line.price_unit,
            200.0,
            places=2,
            msg="Price should be 200.0 with 100% margin on cost of 100"
        )

    def test_04_update_margin_in_draft(self):
        """
        Test that changing margin_percent in draft state updates price_unit.
        Start with 20% margin, change to 30%.
        Expected: 100 * 1.20 = 120, then 100 * 1.30 = 130
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        # Initial price
        self.assertAlmostEqual(line.price_unit, 120.0, places=2)

        # Update margin without providing price_unit
        line.write({'margin_percent': 30.0})

        # Price should be recalculated: 100 * (1 + 30/100) = 130
        self.assertAlmostEqual(
            line.price_unit,
            130.0,
            places=2,
            msg="Price should update to 130.0 with 30% margin"
        )

    def test_05_update_margin_in_sent_state(self):
        """
        Test that changing margin in 'sent' state also updates price.
        Sent is still a quotation state, so price should update.
        """
        # Create order in sent state
        order_sent = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'state': 'sent',
        })

        line = self.env['sale.order.line'].create({
            'order_id': order_sent.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        self.assertAlmostEqual(line.price_unit, 120.0, places=2)

        # Change margin in sent state
        line.write({'margin_percent': 40.0})

        # Price should update: 100 * 1.40 = 140
        self.assertAlmostEqual(
            line.price_unit,
            140.0,
            places=2,
            msg="Price should update in 'sent' state"
        )

    def test_06_no_update_after_confirmation(self):
        """
        Test that changing margin_percent after order confirmation
        does NOT update price_unit.
        This is critical - confirmed orders should not auto-recalculate prices.
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        # Confirm the order
        self.sale_order.action_confirm()
        self.assertEqual(self.sale_order.state, 'sale')

        # Record the price before margin change
        original_price = line.price_unit
        self.assertAlmostEqual(original_price, 120.0, places=2)

        # Try to change margin after confirmation
        line.write({'margin_percent': 50.0})

        # Price should NOT change
        self.assertAlmostEqual(
            line.price_unit,
            original_price,
            places=2,
            msg="Price should NOT update after order confirmation"
        )

        # But margin field itself should be updated
        self.assertAlmostEqual(line.margin_percent, 50.0, places=2)

    def test_07_explicit_price_not_overridden(self):
        """
        Test that if price_unit is explicitly provided in write(),
        it should NOT be overridden by margin calculation.
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        # Explicitly set price_unit and margin together
        line.write({
            'margin_percent': 50.0,
            'price_unit': 99.99,  # Explicit price
        })

        # Price should be the explicit value, not calculated
        self.assertAlmostEqual(
            line.price_unit,
            99.99,
            places=2,
            msg="Explicit price_unit should not be overridden"
        )

    def test_08_zero_cost_product(self):
        """
        Test edge case: product with zero cost.
        Should not crash and should calculate correctly.
        Expected: 0 * (1 + margin/100) = 0
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_zero_cost.id,
            'product_uom_qty': 1.0,
            'margin_percent': 50.0,
        })

        # Should not crash
        self.assertAlmostEqual(
            line.price_unit,
            0.0,
            places=2,
            msg="Zero cost product should result in zero price"
        )

        self.assertAlmostEqual(
            line.cost_price,
            0.0,
            places=2,
            msg="Cost price should be zero"
        )

    def test_09_change_product_updates_price(self):
        """
        Test that changing the product on a line updates the price
        based on the new product's cost and existing margin.
        """
        # Create a second product with different cost
        product_chair = self.env['product.product'].create({
            'name': 'Test Chair',
            'type': 'consu',
            'standard_price': 50.0,  # Cost = 50
            'list_price': 75.0,
        })

        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,  # Cost 100
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        # Initial: 100 * 1.20 = 120
        self.assertAlmostEqual(line.price_unit, 120.0, places=2)

        # Change product to chair (cost 50)
        line.write({'product_id': product_chair.id})

        # New price: 50 * 1.20 = 60
        self.assertAlmostEqual(
            line.price_unit,
            60.0,
            places=2,
            msg="Price should update when product changes"
        )

        # Cost price should also update
        self.assertAlmostEqual(line.cost_price, 50.0, places=2)

    def test_10_zero_margin(self):
        """
        Test with 0% margin - price should equal cost.
        Expected: 100 * (1 + 0/100) = 100
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 0.0,
        })

        self.assertAlmostEqual(
            line.price_unit,
            100.0,
            places=2,
            msg="With 0% margin, price should equal cost"
        )

    def test_11_negative_margin(self):
        """
        Test with negative margin (selling below cost).
        Expected: 100 * (1 + (-10)/100) = 90
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': -10.0,
        })

        self.assertAlmostEqual(
            line.price_unit,
            90.0,
            places=2,
            msg="Negative margin should reduce price below cost"
        )

    def test_12_multiple_lines_same_order(self):
        """
        Test that multiple lines in the same order each calculate
        their price independently based on their own margin.
        """
        line1 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        line2 = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 2.0,
            'margin_percent': 50.0,
        })

        # Line 1: 100 * 1.20 = 120
        self.assertAlmostEqual(line1.price_unit, 120.0, places=2)

        # Line 2: 100 * 1.50 = 150
        self.assertAlmostEqual(line2.price_unit, 150.0, places=2)

        # Lines should be independent
        line1.write({'margin_percent': 30.0})
        self.assertAlmostEqual(line1.price_unit, 130.0, places=2)

        # Line 2 should not be affected
        self.assertAlmostEqual(line2.price_unit, 150.0, places=2)

    def test_13_cost_price_computed_field(self):
        """
        Test that cost_price computed field correctly reflects
        the product's standard_price.
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
        })

        # Cost price should match product standard_price
        self.assertAlmostEqual(
            line.cost_price,
            self.product_desk.standard_price,
            places=2
        )

        # Update product cost
        self.product_desk.standard_price = 150.0

        # Recompute (simulate field dependency)
        line._compute_cost_price()

        # Cost price should update
        self.assertAlmostEqual(line.cost_price, 150.0, places=2)

    def test_14_write_margin_without_price_in_draft(self):
        """
        Test write() method specifically: changing margin_percent
        without price_unit in vals should trigger recalculation.
        """
        line = self.env['sale.order.line'].create({
            'order_id': self.sale_order.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        # Use write with only margin_percent
        result = line.write({'margin_percent': 25.0})

        self.assertTrue(result, "write() should succeed")

        # Price should be recalculated: 100 * 1.25 = 125
        self.assertAlmostEqual(
            line.price_unit,
            125.0,
            places=2,
            msg="write() with margin only should recalculate price"
        )

    def test_15_cancelled_order_no_update(self):
        """
        Test that cancelled orders don't auto-update prices.
        """
        # Create and cancel an order
        order_cancelled = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'state': 'draft',
        })

        line = self.env['sale.order.line'].create({
            'order_id': order_cancelled.id,
            'product_id': self.product_desk.id,
            'product_uom_qty': 1.0,
            'margin_percent': 20.0,
        })

        # Confirm then cancel
        order_cancelled.action_confirm()
        order_cancelled.action_cancel()

        self.assertEqual(order_cancelled.state, 'cancel')

        original_price = line.price_unit

        # Try to change margin
        line.write({'margin_percent': 50.0})

        # Price should NOT change in cancelled state
        self.assertAlmostEqual(
            line.price_unit,
            original_price,
            places=2,
            msg="Price should not update in cancelled orders"
        )
