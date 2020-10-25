# ngapi

NGAPI is Django Rest Framework based application
which provides a few endpoints which allow to post/get a movie or comment to the database and get top commented movies.

Available here - https://ngaping.herokuapp.com/

- POST /movies:
    requires movie title in json format:
    {"title": "movie_title"}
    
- GET /movies:
    allows filtering and ordering
    e.g. movies/?ordering=id
    movies/?year=2014

- POST /comments:
    requires movie id and comment body data in json format:
    {"movie_id": "movie_title", "body": "comment_body"}

- GET /comments:
    allows searching by movie id:
    e.g. comments/?search=1
    
- GET /top:
    requires time range in below format
    top/?date_start=2020-04-17T00:00:00.000Z&date_end=2021-04-19T00:00:00.000Z

To run it locally you need to clone the repo and install required dependencies on your virtual environment from requirements.txt file.
Next switch to "local" branch (which contains sqlite db settings) and run:
- python manage.py migrate
- python manage.py runserver

Basic tests can be run on local branch using 
- python manage.py test