from flask import Flask
import jsonify


app = Flask(__name__)


@app.route("/api/gw")
def return_string():
    return {"result": 13371}


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

    
