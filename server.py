#Веб-сервер на фреймворке Bottle на Heroku. Ошибки отражаются в панеле Sentry. 

import os

import sentry_sdk
from bottle import Bottle
from sentry_sdk.integrations.bottle import BottleIntegration


sentry_sdk.init(
    dsn="https://af7bbba5324d4890a937ca2d6a4bc359@o513510.ingest.sentry.io/5616605",
    integrations=[BottleIntegration()]
)

app = Bottle()


def generate_message():
    return "Тест: /success  or /fail"


def success_message():
    return "Все ОК"


def fail_message():
    return "Что-то не так ..."


@app.route("/success")
def success():
    html_success = """
    <!doctype html>
    <html lang="en">
      <head>
        <title>Heroku-server Bottle</title>
      </head>
      <body>
        <div class="container">
          <h1>This is success</h1>
          <p>{}</p>        
        </div>
      </body>
    </html>
    """.format(
        success_message()
    )
    return html_success


@app.route("/")
def index():
    html = """
<!doctype html>
<html lang="en">
  <head>
    <title>Heroku-server Bottle</title>
  </head>
  <body>
    <div class="container">
      <h1>Протестируй</h1>
      <p>{}</p>
    </div>
  </body>
</html>
""".format(
        generate_message()
    )
    return html


@app.route('/fail')
def fail():
    raise RuntimeError("There is an error")



if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3, )
else:
    app.run(host='127.0.0.1', port=8080, debug=True)