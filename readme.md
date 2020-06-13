create virtualenv with python -m venv env

Django pylint in settings json with this:

{
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--disable=C0111", // missing docstring
        "--load-plugins=pylint_django",
     ],
}