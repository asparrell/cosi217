

# COSI217 Assignment 1
Annika Sparrell
## Run Instructions
### Requirements
Python version 3.10

Packages:
* `spacy`
* `fastapi`
* `uvicorn`
* `flask`
* `typing_extensions=4.8.0`
* `streamlit`
* `pandas`
* `altair`
* `graphviz`, `python-graphviz`

### FastAPI Application
In order to start the FastAPI server, run `uvicorn app_fastapi:app --reload` in the terminal. The server should activate. 
In a new terminal window, run `curl http://127.0.0.1:8000`. This should print out instructions regarding the usage of the application.
You can also run it with `?pretty=true` appended to the address to print it out with more spacing. 

To run the named entity recognition or the dependency parsing, run:

`curl http://127.0.0.1:8000/ner?pretty=true -H "Content-Type: application/json" -d@input.json` for NER or

`curl http://127.0.0.1:8000/dep?pretty=true -H "Content-Type: application/json" -d@input.json` for dependency parsing. The pretty parameter is optional for both.

### Flask Site
Run the main module in `app_flask.py` from your IDE. You should see a script that states that the flask server is now running on http://127.0.0.1:5000 . 
Navigate to this port on your browser, and you should be able to access the site.* Either use the default input or type your own text to be processed,
select whether you would like to see NER or the dependencies, and hit submit. You can return to the form at any time by clicking "Back to form".

*There is a strange issue where sometimes it will say "Access to localhost was denied. You don't have authorization to view this page". It is unclear what causes this; try force reloading if it occurs.

### Streamlit Application
Run `streamlit run app_streamlit.py` from the project directory in your terminal. It should automatically load the page http://localhost:8501 . 
On this page, you can select "entities" or "dependencies" from the sidebar, and then you can change between the table and graph views by selecting the corresponding tab.

