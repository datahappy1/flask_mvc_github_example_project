from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='flask_mvc_github_example_project',
    version='1.0',
    description='Flask, MVC, Github integration in one template project',
    license="MIT",
    long_description=long_description,
    author='datahappy1',
    url="http://datahappy.wordpress.com/",
    packages=['flask_mvc_github_example_project'],  # same as name
    install_requires=['flask==1.1.2', 'werkzeug==1.0.1', 'PyGithub==1.51', 'requests==2.24.0', 'pytest'],
    # external packages as dependencies
)
