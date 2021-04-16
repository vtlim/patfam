import sys
import flask

app = flask.Flask(__name__)
site_title = "PatFam | Identify related members of a patent family"

@app.route('/')
def index():
    return flask.render_template('main.html', site_title=site_title)

@app.route('/run_patfam')
def run_patfam():

    # define locations of flag output icons
    iconUS = "/static/images/icon_us.png";
    iconPCT = "/static/images/icon_world.png";
    iconEU = "/static/images/icon_eu.png";
    iconJP = "/static/images/icon_jp.png";

    # get data from frontend
    #print("HELLO-2")
    #print(request.form)
    #form_data = request.form
    #print("the input number is: ", form_data["inputNum_01"])
    #print("HELLO-3")

    # json output
    treeData = {"appNo":"123456789", "pubNo":"abcdefgh", "title":"Do the best you can until you know better. Then when you know better, do better.", "img":iconUS, "children" : [
        {"appNo":"234567891", "pubNo":"bcdefghi", "title":"Your level of success will seldom exceed your level of personal development.", "img":iconPCT },
        {"appNo":"345678912", "pubNo":"cdefghij", "title":"The most courageous decision that you can make each day is to be in a good mood.", "img":iconEU },
        {"appNo":"456789123", "pubNo":"defghjik", "title":"Anger has a honey tip, but a poison source.", "img":iconJP, "children": [
            {"appNo" : "567891234", "pubNo" : "efghijkl", "title" : "Success hinges less on getting everything right than on how you handle getting things wrong.", "img": iconUS },
            {"appNo" : "678912345", "pubNo" : "fghijklm", "title" : "We don’t see things as they are; we see them as we are.", "img": iconEU }
        ]}
    ]};

    uncatData = "blah blah blah, stuff that was not found"

    return flask.jsonify({
        "treeData": treeData,
        "uncatData": uncatData,
    })

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
