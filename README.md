# Recipe App

<h2>Overview</h2>
<p>
This project focuses on creating a web application using the Django framework. Django has the advantage of being neatly moduralized and developer friendly, while also being powerful enough to run some of the world’s most popular websites. In this project, working with Python-based Django, a full-stack web application using the Django development server will be developed. The application will be deployed using Heroku, with a Postgres database at the backend, HTML, and CSS-based rendered pages at the frontend and Python-based Django as the web application framework. The main focus of this project will be the backend with a light touch of styling on the frontend. The final web application will be dynamic and multi-user, letting users sign up and create their own content. It’ll also have statistical dashboards, implementing new data analytics and data visualization skills.
</p>

<br>

<h2>Features</h2>
<ul>
  <li>User Authentication, for secure user login system.</li>
  <li>Recipe Management, users can create recipes and upload images.</li>
  <li>Difficulty Calculation, the application calculates the difficulty of recipes based on cooking time and number of ingredients.</li>
  <li>Chart Visualization, charts show data visualization based on search criteria.</li>
  <li>Navbar, each page, once logged in, has a navbar with navigation to About, Recipes, Search, Add Recipe, and Logout.</li>
</ul>

<br>

<h2>Usage</h2>
<ul>
  <li>Home: The homepage displays a welcome message and login button. Clicking "Login" will direct users to the login form on a separate page.</li>
  <li>Recipes: The Recipes page displays a list of all available recipes within the application. Clicking on a recipe name or image will navigate to its Details page.</li>
  <li>Details: The Details page shows detailed information about a recipe, including ingredients, cooking time, difficulty, and its image.</li>
  <li>About: The About page shows developer contact information, including portfolio website link, LinkedIn, GitHub, and email address.</li>
  <li>Search: The Search page allows users to search for any and all recipes available within the database and provides chart visualizations related to recipes data.</li>
  <li>Add Recipe: A form for adding recipes, including fields for the name, ingredients, cooking time, and image. Difficulty is automatically calculated.</li>
</ul>

<br>

<h2>Installation</h2>
<ol>
  <li>Clone the repository: git clone https://github.com/juliocgtrz/recipe_app</li>
  <li>Create and activate virtual environment: python -m venv venv</li>
  <li>Install dependencies: pip install -r requirements.txt</li>
  <li>Apply database migrations: python manage.py migrate</li>
  <li>Run development server: python manage.py runserver</li>
</ol>
