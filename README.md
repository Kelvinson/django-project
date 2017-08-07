# djanogo-project

This is the code for my undergraduate thesis project-visualization for data mining on ecommerce data, I am planning to rewrite the code for the project. The project is based on Django, NVD3( a django wrapper for the famous D3.js library) and other libraries.

To install
----------
To install django framework, it is recommended to use python virtual environemtn. Assuem you have python3 installed. In command line execute:
```sh
$ python3 -m venv myvenv
```
Start your virtual environment by running:
```
$ source myvenv/bin/activate
```
Remember to replace myvenv with your chosen virtualenv name!

NOTE: sometimes source might not be available. In those cases try doing this instead:

```
$ . myvenv/bin/activate
```
You will know that you have virtualenv started when you see that the prompt in your console is prefixed with (myvenv).

When working within a virtual environment, python will automatically refer to the correct version so you can use python instead of python3.

Installing Django

Now that you have your virtualenv started, you can install Django.

Before we do that, we should make sure we have the latest version of pip, the software that we use to install Django:

command-line
(myvenv) ~$ pip install --upgrade pip
Then run pip install django~=1.10.0 (note that we use a tilde followed by an equal sign: ~=) to install Django.

```
$ pip install django~=1.10.0
```
Based on what problem your application will handle, you will have to install other dependencies, for me I have to install scipy, pandas, statmodels and so on.

Use the database.
----------
The sqlite database file in this repo contains the data information I used in my project, it is all about ecommerce data. You can update the database in the console and migrate to your app.

