# flask_mvc_github_boilerplate
## a sample project for working with files in your Github repo using Flask webapp / api
### 10000 ft. overview:
![alt text][diagram]

[diagram]: https://github.com/datahappy1/flask_mvc_github_boilerplate/blob/master/flaskr/docs/diagram.png "diagram"

### purpose of this boilerplate Flask project is to demonstrate:
1) how Flask can be used with the MVC design pattern using api endpoints and using blueprints modular import
2) how Flask can deal with Github integration using the Github api v3 (used as the model "persistence" layer
in the MVC design pattern)
3) api endpoint requests pytest testing
4) ability of such a web application to gracefully fail on Github integration exceptions

### how to setup your environment:
1) git clone this repo
2) setup a virtual environment for this project
3) create a Github personal access token: login to Github and go to settings - developer settings - Personal access tokens - Generate a new token
4) generate a random flask secret app key
5) setup your environment variables like:

```
github_token = <your github token value>
flask_secret_key = <your generated flask secret key> 
```
6) setup your github repository name, files playground folder and other settings in flaskr/lib/settings.py
7) your startup configuration should look like this:

![alt text][setup]

[setup]: https://github.com/datahappy1/flask_mvc_github_boilerplate/blob/master/flaskr/docs/setup.png "setup"


*disclaimer: this boilerplate app comes as is, in a production ready application, you
should use the OAuth protocol for Github login, this project will
get you started: https://github-flask.readthedocs.io/en/latest/