

# COSI217 Assignment 3
**Annika Sparrell**

## Docker Run Instructions
From the top level directory (`assignment3`), start the application by running `docker compose up --build -d`.

### Flask Site
Simply navigate to http://127.0.0.1:5000/ in the browser to view the site. Either use the default input or type your own text to be processed,
select whether you would like to see the formatted results or what is stored in the database, and hit submit. You can return to the form at any time by clicking "Back to form".


### Streamlit
After the containers are running with the compose, run `docker stop assignment3=streamlit-1`. Then, run `docker run -d -p 8501:8501 assignment3-streamlit` and the site should load on http://localhost:8501 . 

[//]: # (Simply navigate to ____ in the browser to view the site. On this page, you can select "entities" or "dependencies" from the sidebar, and then you can change between the table and graph views by selecting the corresponding tab.)


### FastAPI
Run either `docker exec -it assignment3-fastapi-1 curl http://127.0.0.1:8000/dep?pretty=true -H "Content-Type: application/json" -d@input.json` for dependency parsing or
`docker exec -it assignment3-fastapi-1 curl http://127.0.0.1:8000/ner?pretty=true -H "Content-Type: application/json" -d@input.json` for named entity recognition. The section `?pretty=true` is optional but recommended.

### Spindown
Finally, run `docker compose down --rmi all` to close the docker build.