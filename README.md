# cardamom-workbench


## quick start

- Make sure you have [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed
- clone repo
- run docker compose
- then access in your browser localhost:5001

```
    git clone git@gitlab.insight-centre.org:uld/cardamom-workbench.git
    docker-compose up
```

## project structure


- dockerized postgres
![system design](docs/system_design.png)


### postgres
![postgres folders](docs/postgres_folders.png)

- postgres_data is where we persist the data from the application (if you want to reset the data just delete this folder)
- if you want to change the db schema just change create_tables.sql but you should reflect the changes on webserver/orm.py


### flask/ UI 
![flask_folders](docs/flask_folders.png)


- api.py 

manages the access to the database and uses orm.py (which converts query results to python classes)

- react_views/ is our react app to generate views 

to build run `npm run build` inside of the react_views folder it will generate a index.html inside of templates/ and all static in static/
to add a new route just follow the pattern as in react_views/src/index.js
