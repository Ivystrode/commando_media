create virtualenv with python -m venv env

Django pylint in settings json with this:

{
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--disable=C0111", // missing docstring
        "--load-plugins=pylint_django",
     ],
}

note - when deploying remove media folder fgrom gitignore and delete all photos except defaults

still to do
- profile page - pad out, maybe add a bio option? exercises, operation experience fields?
- add full CRUD to albums and album photos
- users - if user changes username, breaks all links in posts they made. change to use id to reference post user's name?