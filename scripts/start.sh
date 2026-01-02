#!/bin/bash
set -e

ODOO_HOME="/Users/yuvaraj/Documents/Odoo/odoo19"
CONF="/Users/yuvaraj/Documents/Odoo/projects/project1/config/odoo.conf"
LOG="/Users/yuvaraj/Documents/Odoo/projects/project1/odoo.log"

cd "$ODOO_HOME"
source venv/bin/activate

# Start Odoo in background
./odoo-bin -c "$CONF" --dev=all &

ODOO_PID=$!
echo "Odoo started with PID $ODOO_PID"
echo "Tailing logs: $LOG"
echo "Press CTRL+C to stop tailing (Odoo will keep running)"

# Wait briefly to ensure log file is created
sleep 2

# Tail logs
tail -f "$LOG"