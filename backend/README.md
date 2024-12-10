# Project for Web App Design course (backend)

This is a web-service using python, django, and DRF. Dependencies managed with pip-tools.


## Installing on a local machine

This project requires `python >= 3.10`. It may work with an erlier versions, but it's undetermined.

Python virtual environment should be installed and activated.

```bash
# Unix
python -m venv .venv
source .venv/bin/activate

# Windows
py -m venv .venv
source .venv/Scripts/activate
```


### Automatic installation

```bash
make welcome

cd src
python manage.py runserver
```


### Manual installation

```bash
pip install pip-tools  # Install dependency manager

pip-sync requirements.txt  # Install dependencies

cd src
python manage.py runserver  # Run server
```


## Usage

The database is already prefilled with test data. (`python manage.py loaddata dump.json`)

To view documentation and all endpoints, visit http://localhost:8000/docs/

The admin panel is located at http://localhost:8000/admin/ <br>
(username: `admin`, password: `admin`)

By default, you have two users - `admin` and `user`. Both have passwords matching their usernames. However, you can create your own user by following [this link](http://localhost:8000/admin/users/user/add/).

For testing with Postman, select "Basic Auth" in the authorization tab and provide your desired credentials.

## License

[MIT](https://choosealicense.com/licenses/mit/)
