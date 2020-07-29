#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running
# Make sure to be in the root of the django directory before running!

source $1/bin/activate
pytest --cov=XroadsAPI/
coverage html --omit="*/test*"