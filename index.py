from flask import Flask, render_template, request
# from flask_lt import run_with_lt
from a2web import Query
import os
import time

Q = Query()

app = Flask(__name__)
# run_with_lt(app)


last_time = {}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        result = None
        query = None
        model = None
        length = None

    if request.method == 'POST':
        client_ip = request.remote_addr
        current_time = int(time.time())
        time_difference = current_time - last_time.get(client_ip, 0)
        if time_difference < 5:
            return 'Form submission rate exceeded.'
        else:
            last_time[client_ip] = current_time
            data = request.form
            query = data.get("query")
            model = data.get("model")
            print(query, model)
            result = Q.search(query, model)
            length = len(result["result"])

    return render_template('search.html', result=result, query=query, model=model, length=length)


# @app.route('/test', methods=['GET'])
# def test():
#     return render_template('test.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("FLASK_RUN_PORT", "801")))
