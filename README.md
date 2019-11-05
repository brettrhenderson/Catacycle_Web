# Catacycle
A web-based interface to generate visualizations of the rates of various steps in a catalytic cycle, which can be customized by the user. Population of a web form using known data will generate a graphic for annotation by the user to represent their chemistry.

## Run it Locally
0. Create a python virtual environment with a python 3.7 interpreter. It may well work on earlier python versions but this is untested. 
1. In the main Catacycle directory, and within the virtual environment, run `pip install -r requirements.txt`
2. `python flask_app2.py`
3. Visit [localhost:5000](localhost:5000) in your web browser.

## The Code
The main python components lie within the **app** subdirectory.  

- *drawing_helpers.py* contains the implementation of drawing individual arrows using matplotlib functions. 
- *oboros.py* strings together the drawing functions to create a cycle using the input from the web form.  
- *form.py* and *routes.py* contain the backend of the website using the flask framework.
