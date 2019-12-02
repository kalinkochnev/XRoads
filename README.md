# XRoads
A webapp for students to share their ideas using Django. Features include a unique user tag system similar to discord, custom user authentication, posting, searching and page navigation. Development of this project has been discontinued but many of the features like commenting and voting are completed in the backend but not in the front end. Lots of this code would be useful for anyone undertaking a forum system using Django.

### This would be the first page that an unauthenticated user would see if they went to the url
![landing page](https://user-images.githubusercontent.com/31194806/69973126-fa2a3c80-14f0-11ea-9d34-6168b0beffdf.png)

### The login and logout pages using custom user models
![login](https://user-images.githubusercontent.com/31194806/69973127-fa2a3c80-14f0-11ea-96d3-5693c18f7c1b.png)
![signup](https://user-images.githubusercontent.com/31194806/69973130-fac2d300-14f0-11ea-8812-897c4848ac10.png)

### There is also a user settings page (not fully functional)
![account settings](https://user-images.githubusercontent.com/31194806/69973123-fa2a3c80-14f0-11ea-987b-c7524a588ff0.png)

### You can create posts directly from the forum home, see example post in the image on how to do so
![forum home](https://user-images.githubusercontent.com/31194806/69973520-a10ed880-14f1-11ea-9d0d-bc657796766b.png)
![Post Example](https://user-images.githubusercontent.com/31194806/69974050-85580200-14f2-11ea-9377-1a3a913fdd9e.png)

### There is post body, title and class search functionality which can just be done by using the search bar (created using solr)
![Search Example](https://user-images.githubusercontent.com/31194806/69973129-fac2d300-14f0-11ea-82e7-e766488c5507.png)

---

### First time dev setup
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
