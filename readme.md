create virtualenv with python -m venv env

Django pylint in settings json with this:

{
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--disable=C0111", // missing docstring
        "--load-plugins=pylint_django",
     ],
}

to use virtual env
"python.defaultInterpreterPath": "./env/scripts/python.exe"

note - when deploying remove media folder fgrom gitignore and delete all photos except defaults

still to do
- profile page - pad out, maybe add a bio option? exercises, operation experience fields?
- add full CRUD to albums and album photos