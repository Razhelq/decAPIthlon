# DecAPIthlon

DecAPIthlon is Django Rest Framework based application
which provides a few endpoints which allow to post/get/put/delete a movie 
or post/get a comment to/from postgres database and get top commented movies.

Available here - https://decapithlon.herokuapp.com/

- POST /movies:
    requires movie title in json format:
    {"title": "movie_title"}
    
- GET /movies:
    allows filtering and ordering
    e.g. movies/?ordering=id
    movies/?year=2014
    
- PUT /movies/(movie-id)/:
    allows updating any data related to given movie id
    e.g. movies/17/
    
- DELETE /movies/(movie-id)/:
    allows deleting a movie
    e.g. movies/17/

- POST /comments:
    requires movie id and comment body data in json format:
    {"movie_id": "movie_title", "body": "comment_body"}

- GET /comments:
    allows filtering by movie id:
    e.g. comments/?movie__id=1
    
- GET /top:
    requires time range in below format
    - top/?date_start=2020-04-17T00:00:00.000Z&date_end=2021-04-19T00:00:00.000Z
    
    (Top would be first thing to refactor. It seems to be overcomplicated.
    I think I would have to rebuild models to get some meaningful values 
    with for example annotate and Counter while filtering querysets.
    Lack of time makes me leave it this way.)
    
To run it locally you need to clone the repo
and install required dependencies on your virtual environment from requirements.txt file.
Next switch to "local" branch (which contains sqlite db settings) and run:
- python manage.py migrate
- python manage.py runserver

Basic tests can be run on local branch using 
- python manage.py test

    (I wanted to created mocking with factory_boy but for some reason it was not working properly.
    Because of lack of time I need to leave it this way.)