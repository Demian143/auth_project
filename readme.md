<h1>Welcome to auth project</h1>

It's a simple project to create and update information about a user.
Until this moment, you are able to do the following:
    <ul>
    Create a new user with username, email and password.
    Login and change the password, username  and email.
    </ul>

<h2>How to run the project</h2>

You can simply run the server by ./manage.py runserver. After running the command, go to http://127.0.0.1:8000/authentication/signin/ create your first user, so you'll be able to update the user's information.

<h2>How to test</h2>

You're able to test the functionality by hand or by running ./manage.py test authentication.tests.test_views .