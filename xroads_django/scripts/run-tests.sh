#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# Make sure to be in the root of the django directory before running!

source $1/bin/activate
pip install -r requirements.txt
pytest --cov=XroadsAPI/ XroadsAPI/tests/
pytest --cov-append --cov=XroadsAuth/ XroadsAuth/tests/
coverage html --omit="*/test*"