# XRoads
A webapp for students to share their ideas using Django. Features include a unique user tag system similar to discord, custom user authentication, posting, searching and page navigation. Development of this project has been discontinued but many of the features like commenting and voting are completed in the backend but not in the front end. Lots of this code would be useful for anyone undertaking a forum system using Django.

---

### First time setup
1. Create virtual environment and install pip packages in requirements.txt
2. When in the main directory (~/XRoads) run the following scripts:
```terminal
/bin/bash scripts/postgres/install.sh      (installs postgres with databases and users required)
/bin/bash scripts/solr/setup/install.sh    (installs solr with correct setup)
```

### Management commands
There are several scripts to help reduce the amount of time doing configuration and more time coding! 
They're all located within the scripts folder. Heres a general overview of them:
##### Postgres
-  **_reset-db.sh_** In the event a terrible mistake has been made, this will reset the local database entirely. This will remove all users other than djangouser
- **_create-superuser.sh_** This can be used to add an additional user with rights given to the local database
##### Solr
- **_management/rebuild-index.sh_** Is useful for when you want to update the schema or rebuild the search indexes
- **_management/_** _start.sh, stop.sh, restart.sh_ These apply to the solr server. It is pretty self explanatory
