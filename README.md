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
    
## How to use
Enter the virtual environment as described above, then:

    flask run

# Docker
You can run this api using a docker container. To build a image run the following command:

    docker build -t fsd_account_store .

# Pipelines

Place brief descriptions of Pipelines here

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities.  Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.

# Testing

Unit & Accessibility Testing
To run all tests including aXe accessibility tests (using Chrome driver for Selenium) in a development environment run:

'
pytest
'

## Extras

This repo comes with a .pre-commit-config.yaml, if you wish to use this do
the following while in your virtual enviroment:

    pip install pre-commit black

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.


## Role Management

As well as the [Api](openapi/api.yml) endpoints available on this store for 
managing account roles, a cli command is also provided to enable role updates
to be made without requiring a browser.

Just add an escaped stringified JSON object to the environment variable ASSESSMENT_PROCESS_ROLES
with a set of email/role key-value pairs that you want set.

For example:

    export ASSESMENT_PROCESS_ROLES='{\"a@example.com\":\"ASSESSOR\",\"b@example.com\":\"LEAD_ASSESSOR\"}'

Then via the terminal or SSH run:

    flask update-account-roles

This will update the role for the required users. NOTE - the account for the email must already exist in the DB

Acceptable role names are:

    ADMIN
    LEAD_ASSESSOR
    ASSESSOR
    COMMENTER
    APPLICANT

