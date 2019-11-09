#!/bin/bash

#Shuts off the solr server
/bin/bash ./scripts/solr/management/stop.sh

#Deletes the folder
rm -rf solr

#Reinstalls it
/bin/bash ./scripts/solr/setup/install.sh