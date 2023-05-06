from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('home.html')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        input_url = request.form.get('input_url')
        return render_template('dashboard.html', input_url=input_url)


if __name__ == '__main__':
    app.run(debug=True)
