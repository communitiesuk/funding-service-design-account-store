# funding-service-design-account-store
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://funding-service-design-account-store-dev.london.cloudapps.digital/#/default/core.account.post_account_by_email)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

Repo for the funding service design account store.

Built with Flask + Connexion.

Takes a email address and creates/returns a corresponding payload of account json.

## Prerequisites
- python ^= 3.10

# Getting started

## Installation

Clone the repository

### Create a Virtual environment

    python3 -m venv .venv

### Enter the virtual environment

...either macOS using bash:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt

### Install pre-commit hooks
    pre-commit install

### Updating dependencies
requirements-dev.txt and requirements.txt are updated using [pip-tools pip-compile](https://github.com/jazzband/pip-tools)
To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run (in the following order):

    pip-compile requirements.in

    pip-compile requirements-dev.in

### Setting the environment config

A number of Flask environment config setups exist, including default, development, dev, test, production and unit_test configurations.

Depending on where you are running this you may need to set particular environment variables that are declared in these config files in [config/envs](config/envs) eg. host names etc. More generally though you can switch between these environment configs using the `FLASK_ENV` environment variable. This has been set in the `.flaskenv` to `FLASK_ENV=development` so you shouldn't need to set that if running locally, but you will need to set that elsewhere to ensure it uses the correct config file for the environment you want it to run in.

### Creating the database
This application requires a postgres database.

If running on a local development machine, first ensure you have PostgreSQL server running with a superuser 'postgres'.

You can then either manually create a database called `fsd_account_store_dev` or use the provided invoke script which can be run from the root directory with

    invoke bootstrap_dev_db

Once you have created the database you need to set the `DATABASE_URL` environment variable so the application knows where to find it.

This url has been set in the `.flaskenv` file in the root as

    DATABASE_URL==postgresql://postgres:postgres@127.0.0.1:5432/fsd_account_store_dev

...so if you are running locally on a development machine and you have used the `invoke bootstrap_dev_db` script above to create the database, it should just connect automatically.

If running elsewhere you will need to set the DATABASE_URL env var to the correct url eg. with `export DATABASE_URL=<your-database-url>`

NOTE: during testing with pytest a separate database is created for unit tests to run against. This is then deleted after the tests have run.

Once you have the database running and have the flask application configured to connect to it, you then need to run the database migrations to create the required tables etc. Simply run:

    flask db upgrade

## How to use
Enter the virtual environment as described above, then:

    flask run

# Docker
You can run this api using a docker container. To build a image run the following command:

    docker build -t fsd_account_store .

### Build with Paketo

[Pack](https://buildpacks.io/docs/tools/pack/cli/pack_build/)

[Paketo buildpacks](https://paketo.io/)

```pack build <name your image> --builder paketobuildpacks/builder:base```

Example:

```
[~/work/repos/funding-service-design-account-store] pack build paketo-demofsd-app --builder paketobuildpacks/builder:base
***
Successfully built image paketo-demofsd-app
```

You can then use that image with docker to run a container

```
docker run -d -p 8080:8080 --env PORT=8080 --env FLASK_ENV=dev [envs] paketo-demofsd-app
```

`envs` needs to include values for each of:
SENTRY_DSN
GITHUB_SHA
DATABASE_URL

```
docker ps -a
CONTAINER ID   IMAGE                       COMMAND                  CREATED          STATUS                    PORTS                    NAMES
42633142c619   paketo-demofsd-app          "/cnb/process/web"       8 seconds ago    Up 7 seconds              0.0.0.0:8080->8080/tcp   peaceful_knuth
```

# Pipelines

Place brief descriptions of Pipelines here

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities.  Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.

# Testing

## Unit & Accessibility Testing

1. Ensure you have a local postgres instance setup and running with a user `postgres` created.
2. Ensure that you have set a DATABASE_URL environment variable.
3. Activate your virtual env: `source .venv/bin/activate`
4. Install `requirements-dev.txt`
5. Run pytest

NB : pytest will create a database with a unique name to use just for unit tests. Changes to this db from tests does not persist.

## Transactional tests
These rely on the module `pytest-flask-sqlalchemy` which has good docs on its github page: https://github.com/jeancochrane/pytest-flask-sqlalchemy

The main parts of this framework are invoked in `conftest.py` with the following fixture definitions:
- `enable_transactional_tests` - This makes all tests use transactions, so we don't need to turn it on for each test individually
- `_db` - this makes the framework use our `db` variable from `db.db`, overriding anywhere it is used during the tests.

To make the tests work with a test postgres db in the github pipelines, we pass the following 2 inputs to the shared workflow:

      postgres_unit_testing: true
      db_name: fsd_account_store_test

## Extras

This repo comes with a .pre-commit-config.yaml, if you wish to use this do
the following while in your virtual enviroment:

    pip install pre-commit black

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.
