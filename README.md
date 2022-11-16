# Cella API

This is an API supporting the frontend of [Cella App](https://cella.vercel.app/) which was for a hackathon organized by [Ingressive](https://ingressive.org/)

## Hackathon Image Preview
[Hackathon Image](hackathong_image.jpeg)

## Setting up the BackenProject

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Run the Server

Run both migration commands:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

## API Documentation
The API interacts with the trivia database, and helps users to retrieve questions or categories, create new questions, and go through a quiz-like gameplay scenario.

### Getting started
- Base URL: The API is currently only accessible via your localhost server and can be accessed locally via http://127.0.0.1:8000/ or localhost:8000
- Authentication: No authentication or API keys are required to access the API at this time.

### Error Handling
The app uses conventional HTTP response codes for successes and failures of API requests. As a reminder: Codes `2xx` indicate success, `4xx` indicate failures (such as a bad request or a request for non-existent data), and `5xx` indicate server errors (which means something went wrong with your local server).

Errors are parsed back to the user as JSON-encoded messages in the format below:

    {
            "success": False,
            "error": 404,
            "message": "resource not found"
    }

You can expect the following error codes when using the API:
+ `400 - Bad Request: The request wasn't accepted, often because of a missing parameter`
+ `404 - Not Found: The requested resource doesn't exist on the server`
+ `422 - Unprocessable: An error in your request is preventing the server from processing it`

### Endpoints

-    Documentation for this endpoints can be found [here](https://documenter.getpostman.com/view/20677030/2s8YekQaJL)

