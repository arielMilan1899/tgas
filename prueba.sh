#!/usr/bin/env bash
curl "http://0.0.0.0:8001/repostajes/add" \
  -H "Authorization: Token AFvz0CbJFTrIR1lmc66laHrj"\
  -H "Content-Type: application/json" \
  -d '{
  "alias": "dev.revolico.com"
}'