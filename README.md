# Quotes

### Quotes is a Slack application to save and request inspirational quotes

### Tech stack:

- Python 3.8
- Tornado Web Server
- Celery
- MongoDB
- Docker

### Available commands:

- **/savequote {quote}**  Save a new quote in a mongo database and associate it to user who triggered the command

- **/quote**              Choose randomly a quote from database and write it in the current channel

### Prerequisites:

- A Slack account and an application created to have the SLACK_BOT_TOKEN needed to connecting to Slack API

- Docker and docker-compose installed

- Python version 3.8

- You must have access to a Slack channel to install the app. If not create your own

- Ngrok installed to help us to expose our local web server


### Usage


1. Clone the repository
   
  `git clone git@github.com:rubbenpad/botapp.git`

2. Navigate into new folder create

  `cd botapp`

3. Run docker-compose

  `docker-compose up --build -d`

4. Run in another terminal the next command to expose our local web sever

  `ngrok http 8000`

5. To run the commands in Slack channel you need to register the URL given for ngrok in Slack commands settings

### Contribute

If you want to contribute to this project feel free to open a PR

### License

- MIT

## Author:

Rubén Padilla - [@rubbenpad2](https://twitter.com/rubbenpad2)

Get in touch if have troubles with your project