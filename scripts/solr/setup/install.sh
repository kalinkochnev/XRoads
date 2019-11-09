#!/bin/bash
# Make sure to run     chmod a+x install.sh     before running and you are in the XRoads dir


#Creates a directory if it does not exist
echo Initalizing directory...
DIRECTORY="solr"
if [ ! -d "$DIRECTORY" ]; then
  mkdir $DIRECTORY
  fi

#Downloads solr, unzips and deletes the tar file
echo Downloading and unzipping...
curl -LO https://archive.apache.org/dist/lucene/solr/6.6.0/solr-6.6.0.tgz
tar -C solr -xf solr-6.6.0.tgz --strip-components=1 > /dev/null
rm -rf solr-6.6.0.tgz


#Starts solr and sets up xroadsc_search
echo Configuring xroads_search...
cd solr/
./bin/solr start
./bin/solr create -c xroads_search -n basic_config

#Builds the schema and index
cd ../
/bin/bash ./scripts/solr/management/rebuild-index.sh
