#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running and you are in the XRoads dir

#Builds the new schema (make sure you migrated before)
echo Configuring xroads_search core folder...
./manage.py build_solr_schema --configure-directory=$(pwd)/solr/server/solr/xroads_search/conf --reload-core=1
echo Updated schema

#Rebuilds the index (make sure you migrated before)
echo Rebuilding the index
./manage.py rebuild_index
echo Restarting the Solr server
/bin/bash ./scripts/solr/management/restart.sh
echo completed