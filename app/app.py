import sys
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
site_title = "Hello, World!"

@app.route('/', methods=['GET', 'POST'])
def index():
    print("HELLO-1")
    if request.method == 'GET':
        return render_template('main.html', site_title=site_title)

    # otherwise if post
    print("HELLO-2")
    print(request.form)
    form_data = request.form
    print("the input number is: ", form_data["inputNum_01"])
    print("HELLO-3")
    result = ""
    return render_template('main.html', site_title=site_title, result=result)
    #return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
