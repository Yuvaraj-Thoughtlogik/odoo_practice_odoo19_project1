# Sale Line Margin Price - Test Suite

## Overview

This directory contains automated tests for the `sale_line_margin_price` module.

## Test Coverage

The test suite covers:

1. **Default Behavior**: Default 20% margin and automatic price calculation
2. **Custom Margins**: Creating lines with custom margin percentages (50%, 100%, etc.)
3. **Price Updates in Draft/Sent**: Verifying price recalculation when margin changes in quotation states
4. **Confirmation Lock**: Ensuring prices DON'T update after order confirmation
5. **Explicit Price Override**: Testing that explicitly set prices are not overridden
6. **Edge Cases**:
   - Zero cost products
   - Zero margin
   - Negative margins
   - Cancelled orders
7. **Product Changes**: Price updates when changing products on a line
8. **Multiple Lines**: Independent margin calculations for multiple lines
9. **Computed Fields**: Proper cost_price field computation

## Running Tests

### Run all tests for this module:

```bash
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin \
  -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf \
  -d YOUR_DATABASE_NAME \
  --test-enable \
  --test-tags sale_line_margin_price \
  --stop-after-init
```

### Run tests with more verbose output:

```bash
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin \
  -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf \
  -d YOUR_DATABASE_NAME \
  --test-enable \
  --test-tags sale_line_margin_price \
  --log-level=test \
  --stop-after-init
```

### Run only this specific test class:

```bash
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin \
  -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf \
  -d YOUR_DATABASE_NAME \
  --test-enable \
  --test-tags /sale_line_margin_price:TestSaleLineMarginPrice \
  --stop-after-init
```

### Run a specific test method:

```bash
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin \
  -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf \
  -d YOUR_DATABASE_NAME \
  --test-enable \
  --test-tags /sale_line_margin_price:TestSaleLineMarginPrice.test_01_default_margin_on_new_line \
  --stop-after-init
```

## Test Database

**IMPORTANT**: Always use a TEST database, not your production database!

### Create a test database:

```bash
# Create a new test database
createdb odoo_test_sale_margin

# Initialize it with Odoo
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin \
  -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf \
  -d odoo_test_sale_margin \
  -i sale_line_margin_price \
  --stop-after-init

# Run tests on it
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin \
  -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf \
  -d odoo_test_sale_margin \
  --test-enable \
  --test-tags sale_line_margin_price \
  --stop-after-init
```

## Test Execution Notes

- Tests are tagged with `@tagged('post_install', '-at_install')` so they run after module installation
- Tests use `TransactionCase` which provides transaction rollback for isolation
- All tests use `assertAlmostEqual` for float comparisons to avoid precision issues
- Tests are numbered (test_01, test_02, etc.) for clear execution order

## Expected Output

When all tests pass, you should see:

```
...............
----------------------------------------------------------------------
Ran 15 tests in X.XXXs

OK
```

## Troubleshooting

If tests fail:

1. Check that the module is properly installed: `Apps → sale_line_margin_price`
2. Verify the database has the required dependencies: `sale`, `product`
3. Check Odoo logs for detailed error messages
4. Ensure you're using a clean test database

## Adding New Tests

To add new test cases:

1. Add a new method to `TestSaleLineMarginPrice` class
2. Name it `test_XX_description` (where XX is the next number)
3. Use `self.assertAlmostEqual()` for float comparisons
4. Add clear docstrings explaining what the test validates
