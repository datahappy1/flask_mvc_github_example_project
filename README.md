# flask_mvc_github_example_project

![](https://github.com/datahappy1/flask_mvc_github_example_project/blob/master/docs/rating.svg)

Example project demonstrating the CRUD paradigm on top of the branches and files in a Github repository, built with Flask.
This project implements the same CRUD pattern using a Rest API and using a web application.

- [Project Overview](#project-overview)
- [Key features](#key-features)
- [Screenshots from the web application](#screenshots-from-the-web-application)
- [How to install and setup locally](#how-to-install-and-setup-locally)

## Project Overview:
![alt text][diagram]

[diagram]: https://github.com/datahappy1/flask_mvc_github_example_project/blob/master/docs/diagram.png "diagram"

## Key features:
1) how to deliver the same features in both API endpoints and static html forms in one Flask project
2) how Flask can be used with the MVC design pattern with the controller imported as Flask blueprints
3) how Flask can deal with Github integration using the Github API v3 (used as the model "persistence" layer
in the MVC design pattern)
4) API endpoint pytest testing with importing the app factory
5) ability of such a web application to gracefully fail on Github integration exceptions
6) how easy it is to integrate a Flask web application with Bootstrap used for styling

## Screenshots from the web application:
![alt text][mainscreen]

[mainscreen]: https://github.com/datahappy1/flask_mvc_github_example_project/blob/master/docs/main_screen.png "main screen"

![alt text][branchesmanager]

[branchesmanager]: https://github.com/datahappy1/flask_mvc_github_example_project/blob/master/docs/branches_manager.png "branchesmanager"

![alt text][filesmanager]

[filesmanager]: https://github.com/datahappy1/flask_mvc_github_example_project/blob/master/docs/files_manager.png "filesmanager"



## How to install and setup locally:
1) `git clone` this repo
2) setup a virtual environment for this project
3) create a Github personal access token: login to Github and go to settings --> developer settings --> Personal access tokens --> Generate a new token
4) generate a random flask secret app key
5) setup your environment variables like:

```
github_token = <your github token value>
flask_secret_key = <your generated flask secret key> 
```
6) setup your github repository name, the "files playground" folder and other settings in `flaskr/project_variables/settings.py`
7) your startup configuration should look something like this:

![alt text][setup]

[setup]: https://github.com/datahappy1/flask_mvc_github_example_project/blob/master/docs/setup.png "setup"


> disclaimer: this example project codebase comes as is, in a production ready application, besides other things, 
you should use the OAuth protocol for the Github login, this library can
get you started: https://github-flask.readthedocs.io/en/latest/
