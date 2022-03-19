# REST API for managing character sheets for tabletop RPGs
- Currently only supports the free ruleset of the DND 5e SRD.
- Using my [dnd-character](https://github.com/tassaron/dnd-character) Python library</li>
- This is my first Django project created for practice

## Installation
- Create and activate new Python virtual environment
- `pip install .`
- `python3 src/manage.py migrate` creates a SQLite db
- `python3 src/manage.py createsuperuser` creates an admin user

## Development
- Live-reloading dev server: `python3 src/manage.py runserver`
- Create migrations if you change models: `python3 src/manage.py makemigrations api_v1`

## Production
- Probably using uWSGI and Nginx just like my Flask projects?

## Upgrading
- Switch to the website user
- `git pull` new code
- Activate Python virtual environment
- `pip install .`
- `python3 src/manage.py migrate` (idempotent so you can always run it)
- Restart systemd unit