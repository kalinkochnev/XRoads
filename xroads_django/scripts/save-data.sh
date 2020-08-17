#!/bin/bash
# Make sure to run     chmod a+x start-with-data.sh     before running
# To execute  ./start-with-data.sh
# This saves all the database into a file (not including images) to be imported later

python3 manage.py dumpdata --natural-foreign > fixtures/test_data_foreign.json
python3 manage.py dumpdata --natural-primary > fixtures/test_data_primary.json