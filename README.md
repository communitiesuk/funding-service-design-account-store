# funding-service-design-account-store
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Code style : black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)

This repository is designed to handle the generating and providing of JSON payloads for accounts.

[Developer setup guide](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-setup.md)


This service depends on:
- A postgres database
- No other microservices

# IDE Setup
[Python IDE Setup](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-ide-setup.md)

# Data
### Setting the environment config

A number of Flask environment config setups exist, including default, development, dev, test, production and unit_test configurations.

Depending on where you are running this you may need to set particular environment variables that are declared in these config files in [config/envs](config/envs) eg. host names etc. More generally though you can switch between these environment configs using the `FLASK_ENV` environment variable. This has been set in the `.flaskenv` to `FLASK_ENV=development` so you shouldn't need to set that if running locally, but you will need to set that elsewhere to ensure it uses the correct config file for the environment you want it to run in.

### Creating the database
This application requires a postgres database.

General instructions for local db development are available here: [Local database development](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-db-development.md)

When creating the database you either manually create a database called `fsd_account_store_dev` or use the provided invoke script which can be run from the root directory with

    invoke bootstrap_dev_db

Once you have created the database you need to set the `DATABASE_URL` environment variable so the application knows where to find it.

This url can be set in the `.flaskenv` file in the root as

    # pragma: allowlist nextline secret
    DATABASE_URL==postgresql://postgres:postgres@127.0.0.1:5432/fsd_account_store_dev

...so if you are running locally on a development machine and you have used the `invoke bootstrap_dev_db` script above to create the database, it should just connect automatically.

If running elsewhere you will need to set the DATABASE_URL env var to the correct url eg. with `export DATABASE_URL=<your-database-url>`

NOTE: during testing with pytest a separate database is created for unit tests to run against. This is then deleted after the tests have run.

Once you have the database running and have the flask application configured to connect to it, you then need to run the database migrations to create the required tables etc.
This is outlined in the Local database development README above.

## How to use
Enter the virtual environment as described above, then:

    flask run

# Docker
You can run this api using a docker container. To build a image run the following command:

    docker build -t fsd_account_store .

## Paketo
Paketo is used to build the docker image which gets deployed to our test and production environments. Details available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-paketo.md)

`envs` needs to include values for each of:
SENTRY_DSN
GITHUB_SHA
DATABASE_URL

# Testing
[Testing in Python repos](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-testing.md)


## Unit & Accessibility Testing

1. Ensure you have a local postgres instance setup and running with a user `postgres` created.
2. Ensure that you have set a DATABASE_URL environment variable.
3. Activate your virtual env: `source .venv/bin/activate`
4. Install `requirements-dev.txt`
5. Run pytest

NB : pytest will create a database with a unique name to use just for unit tests. Changes to this db from tests does not persist.

## Transactional tests

Test data is created on a per-test basis to prevent test pollution. To create test data for a test, request the `seed_test_data` fixture in your test. That fixture then provides access to the inserted records and will clean up after itself at the end of the test session.

More details on the fixtures in utils: https://github.com/communitiesuk/funding-service-design-utils/blob/dcc64b0b253a1056ce99e8fe7ea8530406355c96/README.md#fixtures


# Builds and Deploys
Details on how our pipelines work and the release process is available [here](https://dluhcdigital.atlassian.net/wiki/spaces/FS/pages/73695505/How+do+we+deploy+our+code+to+prod)

## Copilot
Copilot is used for infrastructure deployment. Instructions are available [here](https://github.com/communitiesuk/funding-service-design-workflows/blob/main/readmes/python-repos-copilot.md), with the following values for the account store:
- service-name: fsd-account-store
- image-name: ghcr.io/communitiesuk/funding-service-design-account-store:latest
