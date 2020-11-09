Greevil web application
==================================================

This is a Django web application that can be deployed using docker and docker-compose.


#### Built using
[![made-with-python](https://img.shields.io/static/v1?label=&message=python&style=for-the-badge&logo=python&logoColor=white&color=3776ab)](https://www.python.org/)
[![made-with-django](https://img.shields.io/static/v1?label=&message=Django&color=green&style=for-the-badge&logo=django)](https://djangoproject.com)
[![made-with-docker](https://img.shields.io/static/v1?label=&message=Docker&style=for-the-badge&logo=docker&color=2496ed&logoColor=white)](https://www.docker.com/)

Getting Started
---------------

1. Install docker and docker-compose.
        
2. Enable and/or start docker service:

        $ sudo systemctl start docker.service
        $ sudo systemctl enable docker.service

3. Use docker-compose, or run ```run_docker.sh```:

        $ chmod +x ./run_docker.sh
        $ ./run_docker.sh

4. Open http://localhost/ in a web browser to view the application.

5. Setup [greevil-app](https://github.com/Acquil/greevil-app) too for using the application.
   APP_SERVER needs to be set with the value of greevil-app's ip address:
        
        $ export APP_SERVER=<greevil-app-ip>
        
6. To use other ports, change the ports used in ```docker-compse.yaml``` and ```nginx/project.conf``` 

## Running without docker

1. Go to ```src/```:
        
        $ cd ./src
    
2. Create virtualenv for python3 and install dependencies in ```requirements.txt```:
    
        $ python3 venv -m venv
        $ source venv/bin/activate
        $ pip install -r requirements.txt

3. (Optional) Enable Django's debug mode for development:

        $ export DJANGO_DEBUG=True

4. Start the Django development server:

        $ python manage.py runserver


## Other info

To run your tests locally, go to the root directory of the sample code and run
the `python manage.py test` command.
