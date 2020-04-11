# Django-Vue-Template

## Environment variables

The project depends on three environment variables, ensure these are exported before beginning either Local Development or Server Deployment (It is recommended to create an `app-env` with these values saved for longer term use):

Create a file called `app-env` with the following contents, run `source app-env` before setting up make.
```bash
DJANGO_SECRET_KEY=secret_key
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=project_client_id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=project_client_secret
```

* `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` - Used for Google Accounts authentication
* `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` - Used for Google Accounts authentication
* `DJANGO_SECRET_KEY` - A secret for a particular Django build

## Local Development

### Before:

Install npm.
`brew install npm`

Run `make local`, which will run the following commands:
1. `make build`
2. `make up`
3. `make migrate`
4. `make npm-install`
5. `make frontend-dev`

If you want to log in to the django admin page (will be at `127.0.0.1:8000/admin`) create a superuser using `make create-superuser`.

### During:

- run `make build && make up` after making changes to the `Pipfile`/`Pipfile.lock`
- If you make changes to `app-env`/update the django settings/etc run `make restart-django`
- kill the webpack process then run `make npm-install` after updating `package.json`

### After:

Run `make down`

## Server deployment

The nginx config to be used in `/etc/nginx/sites-available` is available [here](deploy/nginx-static-sites-available.conf). Ensure that you rename this file to the sitename when actually deploying (kaye_tech.doman_name).

We use the Python library `Fabric` to allow for local users to deploy remotely to the PY3 server:
1. Install fabric globally via `sudo pip install fabric`
2. Export the environment variables mentioned in [Environment Variables](#kaye_tech)
3. Run `python3 deploy/deploy.py` (This will deploy the contents of `origin master`, not your local changes)

Bear in mind that you'll still need to setup the configuration files mentioned above for the backend portions of the application to actually function.
