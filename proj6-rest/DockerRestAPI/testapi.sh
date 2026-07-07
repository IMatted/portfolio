#!/bin/bash

API_URL="http://localhost:5001"

echo "=========================================="
echo "Starting RestAPI Endpoints Tests"
echo "=========================================="

echo -n "Testing GET /listAll (JSON)... "
RESPONSE=$(curl -s -w "%{http_code}" -o response.json "${API_URL}/listAll")
HTTP_STATUS="${RESPONSE:${#RESPONSE}-3}"

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "SUCCESS (200)"
else
    echo "FAILED with status $HTTP_STATUS"
fi

echo -n "Testing GET /listAll/csv (CSV)... "
RESPONSE=$(curl -s -w "%{http_code}" -o response.csv "${API_URL}/listAll/csv")
HTTP_STATUS="${RESPONSE:${#RESPONSE}-3}"

if [ "$HTTP_STATUS" -eq 200 ] && grep -q "brevets/controls/" response.csv; then
    echo "SUCCESS (200 & verified CSV header)"
else
    echo "FAILED"
fi

echo -n "Testing GET /listOpenOnly (JSON)... "
RESPONSE=$(curl -s -w "%{http_code}" -o response.json "${API_URL}/listOpenOnly")
HTTP_STATUS="${RESPONSE:${#RESPONSE}-3}"

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "SUCCESS (200)"
else
    echo "FAILED"
fi

echo -n "Testing GET /listCloseOnly/csv (CSV)... "
RESPONSE=$(curl -s -w "%{http_code}" -o response.csv "${API_URL}/listCloseOnly/csv")
HTTP_STATUS="${RESPONSE:${#RESPONSE}-3}"

if [ "$HTTP_STATUS" -eq 200 ] && grep -q "brevets/controls/close" response.csv; then
    echo "SUCCESS (200 & verified CSV header)"
else
    echo "FAILED"
fi

echo -n "Testing GET /listOpenOnly?top=3 (Filtering top k)... "
RESPONSE=$(curl -s -w "%{http_code}" -o response.json "${API_URL}/listOpenOnly?top=3")
HTTP_STATUS="${RESPONSE:${#RESPONSE}-3}"

if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "SUCCESS (200)"
else
    echo "FAILED"
fi

rm -f response.json response.csv

echo "=========================================="
echo "Testing complete."
echo "=========================================="