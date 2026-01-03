# Sale Line Margin Price - Installation Guide

## Module Overview
Automatically calculates sale order line prices based on product cost + margin %.

## Installation Steps

### 1. Verify Addon Path
The addon is already in the correct location:
```
/Users/yuvaraj/Documents/Odoo/projects/project1/custom_addons/sale_line_margin_price
```

Your `odoo.conf` already includes this path ✓

### 2. Restart Odoo Server

**Option A: If running Odoo manually**
```bash
# Stop the current Odoo process (Ctrl+C)
# Then restart with:
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf
```

**Option B: If using a service/script**
```bash
# Restart your Odoo service
```

### 3. Update Apps List in Odoo UI

1. Open Odoo in browser: http://localhost:8169
2. **Enable Developer Mode**:
   - Click on Settings (⚙️) in the top menu
   - Scroll down and click "Activate the developer mode"
   - OR append `?debug=1` to your URL

3. **Update Apps List**:
   - Go to **Apps** menu
   - Click the **three dots menu** (⋮) in the search bar
   - Click **"Update Apps List"**
   - In the popup, click **"Update"**

4. **Search for the Module**:
   - Remove any filters (click the 🗑️ next to "Apps" filter)
   - Search for: `sale_line_margin_price` or `Sale Line Margin Price`
   - You should see the module appear

5. **Install**:
   - Click **"Install"** button

### 4. Verify Installation

After installation:
1. Go to **Sales → Orders → Quotations**
2. Create a new quotation
3. Add a product to an order line
4. You should see the new fields:
   - **Margin %** (default 20%)
   - **Cost Price** (hidden by default, click optional columns to show)
5. Change the margin % and watch the price update automatically!

## Troubleshooting

### Module doesn't appear after updating apps list
- Ensure developer mode is enabled
- Remove the "Apps" filter (only shows main apps, not all modules)
- Search by technical name: `sale_line_margin_price`

### Price doesn't update
- Only works in Draft/Sent states (not on confirmed orders)
- Requires product to have a cost price (standard_price)

### Module shows as "installed" but fields don't appear
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
- Upgrade the module: Apps → Search → three dots → Upgrade

## Quick Start Command

If you have CLI access to Odoo:
```bash
# Install directly via command line
/Users/yuvaraj/Documents/Odoo/odoo19/odoo-bin -c /Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf -d YOUR_DATABASE_NAME -i sale_line_margin_price --stop-after-init
```

Replace `YOUR_DATABASE_NAME` with your actual database name.
