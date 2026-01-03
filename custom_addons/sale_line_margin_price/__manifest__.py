# -*- coding: utf-8 -*-
{
    'name': 'Sale Line Margin Pricing',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Calculate sale prices automatically from product cost plus configurable margin percentage',
    'description': """
Sale Line Margin Pricing
=========================

Automatically calculate selling prices on quotation lines based on product cost and margin percentage.

Key Features
------------
* Add configurable margin percentage field to each sale order line (default: 20%)
* Automatic price calculation: selling price = cost × (1 + margin%)
* Real-time price updates when product or margin changes (quotations only)
* Visual cost price display for better margin visibility
* Safe: prices locked after quotation confirmation
* Compatible with existing pricelist functionality

Perfect for businesses that need dynamic cost-plus pricing!
    """,
    'author': 'ThoughtLogik',
    'maintainer': 'ThoughtLogik',
    'website': 'https://thoughtlogik.com',
    'support': 'support@thoughtlogik.com',
    'depends': [
        'sale_management',
        'product',
    ],
    'data': [
        'views/sale_order_line_view.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/banner.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'price': 0.00,
    'currency': 'EUR',
}
