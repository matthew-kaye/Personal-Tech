# Personal Tech Website

## Secrets

The project depends on several secrets, stored in AWS Secret Manager. Ensure your AWS environment credentials are set up in order to access.

## Local Development

### Before:

Install npm.
On Mac: `brew install npm` - check using appropriate version
On Windows: https://nodejs.org/en/

To set up locally, run the following:

1. `make local`
2. `make migrate`
3. `make npm-install` (using node v10.9)
4. `make frontend-dev`

If you want to log in to the django admin page (will be at `127.0.0.1:8000/admin`) create a superuser using `make superuser`.

### During:

- Run `pipenv install` after making changes to the `Pipfile`/`Pipfile.lock`
- Kill the webpack process then run `make npm-install` after updating `package.json`

## Deployment

The website is hosted on AWS Elastic Beanstalk, with an RDS database.

To deploy an update, run:

1. `make npm-build` and `make collect-static` (for a frontend update).
2. `make deploy`
