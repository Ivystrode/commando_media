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
- add location information to user profile
- use things learned in pixel tracker to gather information