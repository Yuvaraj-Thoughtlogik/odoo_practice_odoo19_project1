# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_percent = fields.Float(
        string='Margin %',
        default=20.0,  # Default 20%
        help='Margin percentage applied to product cost to calculate selling price'
    )

    cost_price = fields.Float(
        string='Cost Price',
        compute='_compute_cost_price',
        store=True,
        readonly=True,
        help='Product standard cost price (for visibility)'
    )

    @api.depends('product_id')
    def _compute_cost_price(self):
        """Compute the cost price from product standard_price"""
        for line in self:
            if line.product_id:
                line.cost_price = line.product_id.standard_price
            else:
                line.cost_price = 0.0

    @api.onchange('margin_percent')
    def _onchange_margin_percent(self):
        """
        Auto-update price_unit when margin changes.
        Only applies in draft/sent states.
        Formula: price_unit = product.standard_price * (1 + margin_percent/100)

        Note: margin_percent is stored as a number (100 for 100%, 20 for 20%)
        """
        if self.order_id and self.order_id.state not in ('draft', 'sent'):
            return

        if self.product_id:
            cost = self.product_id.standard_price or 0.0

            # margin_percent is stored as number: 100 for 100%, 50 for 50%, 20 for 20%
            margin_multiplier = 1.0 + (self.margin_percent / 100.0)
            new_price = cost * margin_multiplier

            self.price_unit = new_price

    @api.onchange('product_id')
    def _onchange_product_id_margin(self):
        """
        Auto-update price_unit when product changes.
        This runs AFTER the standard product_id onchange.
        """
        # Call parent onchange first
        res = super(SaleOrderLine, self)._onchange_product_id()

        if self.order_id and self.order_id.state not in ('draft', 'sent'):
            return res

        # Then override price with margin-based calculation
        if self.product_id:
            cost = self.product_id.standard_price or 0.0
            margin_multiplier = 1.0 + (self.margin_percent / 100.0)
            self.price_unit = cost * margin_multiplier

        return res

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to recompute price_unit from margin on new lines
        if price_unit not explicitly provided.
        Only applies in draft/sent states.
        Note: margin_percent is stored as number (20.0 for 20%, 100.0 for 100%)
        """
        for vals in vals_list:
            # Check if we should auto-compute price
            if self._should_auto_compute_price(vals):
                product = self.env['product.product'].browse(vals.get('product_id'))
                margin_percent = vals.get('margin_percent', 20.0)  # Default 20%

                if product and product.standard_price:
                    margin_multiplier = 1.0 + (margin_percent / 100.0)
                    vals['price_unit'] = product.standard_price * margin_multiplier

        return super(SaleOrderLine, self).create(vals_list)

    def write(self, vals):
        """
        Override write to recompute price_unit when margin or product changes
        if price_unit not explicitly provided in vals.
        Only applies in draft/sent states.
        Note: margin_percent is stored as number (20.0 for 20%, 100.0 for 100%)
        """
        # If price_unit is being explicitly set by user, don't auto-compute
        if 'price_unit' in vals:
            return super(SaleOrderLine, self).write(vals)

        # Check if margin or product is changing
        if 'margin_percent' in vals or 'product_id' in vals:
            for line in self:
                # Only auto-update in quotation states
                if line.order_id and line.order_id.state not in ('draft', 'sent'):
                    continue

                # Determine the product and margin to use
                product = line.product_id
                if 'product_id' in vals:
                    product = self.env['product.product'].browse(vals['product_id'])

                margin_percent = vals.get('margin_percent', line.margin_percent)

                # Compute new price (divide by 100 to convert percentage to decimal)
                cost = product.standard_price if product else 0.0
                margin_multiplier = 1.0 + (margin_percent / 100.0)
                computed_price = cost * margin_multiplier

                # Update price_unit in vals for this specific line
                line_vals = vals.copy()
                line_vals['price_unit'] = computed_price
                super(SaleOrderLine, line).write(line_vals)

            # If we updated prices individually, return True
            if any(line.order_id and line.order_id.state in ('draft', 'sent') for line in self):
                return True

        return super(SaleOrderLine, self).write(vals)

    def _should_auto_compute_price(self, vals):
        """
        Helper to determine if we should auto-compute price_unit.
        Returns True if:
        - price_unit is not explicitly provided in vals
        - product_id is provided
        - order state is draft or sent (check via order_id if provided)
        """
        if 'price_unit' in vals:
            return False

        if not vals.get('product_id'):
            return False

        # Check order state if order_id provided
        if vals.get('order_id'):
            order = self.env['sale.order'].browse(vals['order_id'])
            if order.state not in ('draft', 'sent'):
                return False

        return True
