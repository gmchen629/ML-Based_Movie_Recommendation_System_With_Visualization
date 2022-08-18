# Machine_Learning-Based_Movie_Recommendation_System
Natural Language Processing based with HTML-JavaScript-Flask-SQlite3-Python

## 1. DESCRIPTION

This package mainly contains 3 directories (backend, d3tree and recommendation_algo) and other web application files (html, css and js).
- backend: use SQLite database with Flask web framework to implement CRUD operations
- d3tree: visualize the selection-recommendation process in an expandable tree fashion using D3.js
- recommendation_algo: attempt at implementing content based algorithm and try to build the model to come up with our final recommendation system in movie and music 
- index.html, styles.css, script.js: interactive interface with our recommendation system


## 2. INSTALLATION

We have already pre-trained the recommendation data, so you just need to install below packages in the "CODE" directory.(Make sure your Python version is over 3.7x where sqlite3 library is built in.)

- Enter "CODE" directory from root directory "team021final"
  $ cd CODE

- Use flask to manage our backend source
  $ pip install Flask

- Handle Cross Origin Resource Sharing
  $ pip install flask-cors


## 3. EXECUTION

- Create a HTTP server in "CODE" directory
  $ python -m http.server 5501 (python3)

- Go to backend directory in a new terminal and connect with server to manage data (default port: 5000)
--- New terminal in the "CODE" directory ---
  $ cd backend
  $ python app.py

- Open a web browser and go to http://localhost:5501/


## 4. LET'S TRY A SEARCH

- Enter your movie in the search bar -> choose your recommended favor (movie or music) -> click SEARCH button. 
(For example, you can fill in "Inception" in the search bar -> select "Movie" option below the bar -> click "Search" to get up to 10 movie recommendation from "Inception".)

- After seeing d3 tree, you can click on the node to explore more recommendation from that movie or you can start a new search in the search bar.
(The default recommend option for next tree level is movie but can be changed below the bar BEFORE next searching) 

- When exploring in the tree, if you change the recommendation option FIRST and click the tree node, the d3 tree would show you relative recommended expansion.
(Different color represents different kind of recommendation. Blue is movie and Orange is music.)

- Feel free to click on those checkboxes on our website, providing us with some suggestions to improve our recommendation system.
(You can see the new average feedback displayed in the terminal that is running your backend server.)



---- !! Important Notes !! ----

1. Revise your recommend option (movie / music) AFTER clicking a node is NOT available. # Future improvement

2. Recommendation from music is NOT available. # Future improvement

-------------------------------
