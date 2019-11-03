# XRoads
A forum for students to share ideas

# Solr Install
1. Download and unzip the files in a dir
```shell
curl -LO https://archive.apache.org/dist/lucene/solr/6.6.0/solr-6.6.0.tgz
mkdir solr
tar -C solr -xf solr-6.6.0.tgz --strip-components=1
cd solr
./bin/solr start                                           # start solr
./bin/solr create -c xroads_search -n basic_config         # create core named 'xroads_search'
```
2. Generate static schema
```shell
./manage.py build_solr_schema --configure-directory=/solr/server/solr/xroads_search/conf --reload-core=1
```



# Haystack install
1. pip install django-haystack
2. Ad to installed apps
```python
INSTALLED_APPS = [
    # Added.
    'haystack',
    # Then your usual apps...
    'forum',
]
```

3. Add haystack settings
```python
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr/xroads_search',
        'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/mysite',
    },
}
```

#Starting solr
```
cd solr/
./bin/solr start
```
