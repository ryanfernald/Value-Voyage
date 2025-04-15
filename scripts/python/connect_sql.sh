#!/bin/bash

# MySQL connection details
HOST="127.0.0.1"
PORT="3307"
USER="value_voyage_backend"
PASS="very_cheap_prices_420"

# Connect to MySQL
mysql -h "$HOST" -P "$PORT" -u "$USER" -p"$PASS"