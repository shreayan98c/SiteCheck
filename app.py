import json
import pickle
from app_utils import save_page_dashboard
from flask import Flask, render_template, request

from main import main

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        input_url = request.form.get('input_url')
        depth = int(request.form.get('depth'))
        selected_option = int(list(request.form.values())[-1])

        api_response = main(input_url, depth, set(), [])

        # add the indexes to each entry of the api_response with key as 'index'
        for i in range(len(api_response)):
            api_response[i]['index'] = i

        landing_page = api_response[0]
        hierarchy_pprint = json.dumps(landing_page['hierarchy'], indent=4)

        for pg in api_response:
            save_page_dashboard(pg)

        return render_template('dashboard.html', input_url=input_url, depth=depth,
                               hierarchy_pprint=hierarchy_pprint, selected_option=selected_option,
                               landing_page=landing_page, responses=api_response)


if __name__ == '__main__':
    app.run(debug=True)
