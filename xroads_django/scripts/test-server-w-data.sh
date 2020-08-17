#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# To execute  ./install.sh
./scripts/run-tests.sh
python3 manage.py testserver fixtures/test_data_foreign.json
