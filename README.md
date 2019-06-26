# flask_github_integrator
## purpose of this boilerplate Flask project is to demonstrate:
1) how Flask can be used with the MVC design pattern using api endpoints and the blueprints modular import
2) how Flask can deal with Github integration using the Github api v3 (used as the model "persistance" layer
in the mvc pattern)
3) WIP: how Flask can deal with Celery workers ( used for background long-running asynchronous tasks )
4) how Flack can be used with the logging decorators

## how to setup your environment:
1) git clone this repo
2) setup a virtual environment for this project
3) create a Github personal access token: login to Github and go to settings - developer settings - Personal access tokens - Generate a new token
4) generate a random flask secret app key
5) setup your environment variables like:

```
github_token = <your github token value>
flask_secret_key = <your generated flask secret key> 
```

*disclaimer: this boilerplate app comes as is, in a production ready application, you
should use the OAuth protocol for Github login, this project will
get you started: https://github-flask.readthedocs.io/en/latest/