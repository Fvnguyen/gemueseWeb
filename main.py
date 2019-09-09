from flask import Flask, render_template,Markup,request
import gunicorn
import redis
import os
import pandas as pd
import pickle
import veg_processes as vp

app = Flask(__name__)

# Gemüse
@app.route("/<endpoint>")
def gemuese(endpoint):
    print(endpoint)
    endpoint = str(endpoint)
    result = getattr(vp,endpoint)()
    if len(result) > 2:
        title = result[0]
        image = result[2]
        label = result[3]
        url = result[4]
        source = result[5]
        return render_template('rezept.html',title=title, url = url,label = label, image = image, source = source)
    else:
        label = result[0]
        result = result[1]
        print(result)
        if isinstance(result, str):
            return render_template('gemuese.html',title=label, result = [result])
        else:
            return render_template('gemuese.html',title=label, result = result)         

@app.route("/look_up")
def look_up():
    return render_template('look_up.html', label = 'Welches Gemüse möchtest Du prüfen?')

@app.route('/look_up', methods=['POST'])
def my_form_post():
    text = request.form['text']
    text.strip()
    result = vp.look_up(text)
    return render_template('gemuese.html',title='Ist dieses Gemüse saisonal?', result = [result])

# Exceptions

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def page_not_found(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = False)