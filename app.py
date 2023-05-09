import json
import pickle
from app_utils import save_landing_page_dashboard
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        input_url = request.form.get('input_url')
        depth = request.form.get('depth')

        with open('api.pkl', 'rb') as inp:
            api_response = pickle.load(inp)

        # add the indexes to each entry of the api_response with key as 'index'
        for i in range(len(api_response)):
            api_response[i]['index'] = i

        landing_page = api_response[0]
        api_response = api_response[1:]

        hierarchy_pprint = json.dumps(landing_page['hierarchy'], indent=4)

        save_landing_page_dashboard(landing_page)

        return render_template('dashboard.html', input_url=input_url, depth=depth,
                               hierarchy_pprint=hierarchy_pprint,
                               landing_page=landing_page, responses=api_response)


if __name__ == '__main__':
    app.run(debug=True)
