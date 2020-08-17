#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# Make sure to be in the root of the django directory before running!

source $1/bin/activate
pip install -r requirements.txt
pytest --cov=XroadsAPI/ XroadsAPI/tests/ --count=1
pytest --cov-append --cov=XroadsAuth/ XroadsAuth/tests/ --count=1
coverage html --omit="*/test*"