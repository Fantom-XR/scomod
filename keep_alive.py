from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.route('/')
def main():
    return "This is webserver for modmail bot hosted on repl.it.<br>Guide: https://sh.anonym-dev.tk/modmail-repl-guide"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

keep_alive()