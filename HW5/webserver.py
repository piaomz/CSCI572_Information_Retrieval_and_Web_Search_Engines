
from flask import Flask
from flask import render_template
from flask import send_file

# creates a Flask application
app = Flask(__name__)


@app.route("/data.json")
def hello():
    message = "Hello, World"
    return send_file("mydata.json")


# run the application
if __name__ == "__main__":
    app.run(debug=True, port=8000)
