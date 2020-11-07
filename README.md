Greevil web application
==================================================

This is a Django web application that can be deployed by AWS CodeDeploy and AWS CloudFormation to an Amazon EC2 server.

What's Here
-----------

Template structure:

* README.md - this file
* appspec.yml - this file is used by AWS CodeDeploy when deploying the web
  application to EC2
* buildspec.yml - this file is used by AWS CodeBuild to build and test
  your application
* requirements/ - this directory contains requirements files that describe
  the Python dependencies required for your Django application in different
  environments
* requirements.txt - this file is used to install production Python dependencies
* ec2django/ - this directory contains your Django project files. Note that this
  directory contains a Django config file (settings.py) that includes a pre-defined
  SECRET_KEY. Before running in a production environment, you should replace this
  application key with one you generate
  (see https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/#secret-key for details)
* helloworld/ - this directory contains your Django application files
* manage.py - this Python script is used to start your Django web application
* scripts/ - this directory contains scripts used by AWS CodeDeploy when
  installing and deploying your application on the Amazon EC2 instance
* supervisord.conf - this configuration file is used by Supervisor to control
  your web application on the Amazon EC2 instance
* template.yml - this file contains the description of AWS resources used by AWS
  CloudFormation to deploy your infrastructure
* template-configuration.json - this file contains the project ARN with placeholders used for tagging resources with the project ID

Getting Started
---------------

1. Create a Python virtual environment:

        $ python3 -m venv ./venv

2. Activate the virtual environment:

        $ source ./venv/bin/activate

3. Install development Python dependencies:

        $ pip install -r requirements/dev.txt

4. (Optional) Enable Django's debug mode for development:

        $ export DJANGO_DEBUG=True

5. Start the Django development server:

        $ python manage.py runserver

6. Open http://127.0.0.1:8000/ in a web browser to view the application.


7. Setup [greevil-app](https://github.com/sreedeepack/greevil-app) too for using the application.

## Other info

To run your tests locally, go to the root directory of the sample code and run
the `python manage.py test` command, which AWS CodeBuild also runs through
the `buildspec.yml` file.
