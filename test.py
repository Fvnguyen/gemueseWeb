from flask import Flask, render_template, abort, request
import gunicorn
import redis
import os
import pandas as pd
import pickle
import veg_processes as vp

wallOfMusic = [
    {'genre':'vaporwave','title':'V A P O R W A V E !','image':'vaporwave.gif','video':'https://www.youtube.com/embed/UJsUpeXK6Jo?autoplay=1'},
    {'genre':'outrun','title':'Outrun! The 80&quot;s are out to get you','image':'outrun.gif','video':'https://www.youtube.com/embed/ZEMwJPym_OM?autoplay=1'},
    {'genre':'bollywood','title':'Bollywood! Look they are dancing','image':'bollywood.gif','video':'https://www.youtube.com/embed/5DK-ZWyxZ8k?autoplay=1'},
    {'genre':'chillwave','title':'Chillwave! It&quot;s not even a real genre','image':'chillwave.gif','video':'https://www.youtube.com/embed/GuPGZZgNFsU?autoplay=1'},
    {'genre':'rock','title':'Rock! No fucks given','image':'rock.gif','video':'https://www.youtube.com/embed/TRVCtbfuDqw?autoplay=1'},
    {'genre':'indie','title':'Indie! That&quot;s so last year','image':'indie.gif','video':'https://www.youtube.com/embed/SWSz_PAfgNc?autoplay=1'},
    ]

# r = redis.from_url(os.environ.get("REDIS_URL"))

# def loadDB(userID):
#     try:
#         db = pickle.loads(r.get(userID))
#         print("loaded db")
#         return db
#     except:
#         print("did not load db")
#         return {}

# def loadAlert(userID):
#     try:
#         filename = userID+'alert'
#         alert = pickle.loads(r.get(filename))
#         print("loaded alerts")
#         return alert
#     except:
#         print("did not load alerts")
#         return {}

# def loadDF(userID):
#     db = loadDB(userID)
#     if any(db):
#         df = pd.DataFrame.from_dict(db)
#         df['Tag'] = pd.DatetimeIndex(df['Zeit']).day
#         df['Monat'] = pd.DatetimeIndex(df['Zeit']).month
#         df['Jahr'] = pd.DatetimeIndex(df['Zeit']).year
#         df['Type'] = df['Type'].str.lower()
#         df['Betrag'] = pd.to_numeric(df['Betrag'])
#         print('DF returned')
#         return df
#     else:
#         df = False
#         print('No DF')
#         return df

app = Flask(__name__)

# Wall of Music
@app.route("/")
def index():
    title = 'Wall of Music'
    wom = wallOfMusic
    return render_template('main.html', title=title, wom = wom)

@app.route("/<genre>")
def music(genre):
    try:
        wom = wallOfMusic.copy()
        genre.lower()
        genre_id = [i for i,_ in enumerate(wom) if _['genre'] == genre][0]
        top_genre = wom.pop(genre_id)
        return render_template('genre.html',genre = top_genre, wom = wom)
    except (IndexError, ValueError, TypeError) as error:
        print(error)
        return render_template('404.html')

# Gemüse
@app.route("/gemuese/<endpoint>")
def gemuese(endpoint):
    print(endpoint)
    endpoint = str(endpoint)
    result = getattr(vp,endpoint)()
    if len(result) > 2:
        label = result[0]
        image = result[2]
        result = Markup(result[1])
        return render_template('rezept.html',title=label, result = result, image = image)
    else:
        label = result[0]
        result = result[1]
        print(result)
        if isinstance(result, str):
            return render_template('gemuese.html',title=label, result = [result])
        else:
            return render_template('gemuese.html',title=label, result = result)

@app.route("/gemuese/look_up")
def look_up():
    return render_template('look_up.html', label = 'Welches Gemüse möchtest Du prüfen?')

@app.route('/gemuese/look_up', methods=['POST'])
def my_form_post():
    text = request.form['text']
    text.strip()
    result = vp.look_up(text)
    return render_template('gemuese.html',title='Ist dieses Gemüse saisonal?', result = [result])

# Expense console
# @app.route("/ausgaben/keys")
# def keys():
#     keys = []
#     for key in r.scan_iter():
#        keys.append(key)
#     return str(keys)

# @app.route("/ausgaben/<userid>")
# def ausgaben_total(userid):
#     df = loadDF(str(userid))
#     return df.to_html()

# Exceptions

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def page_not_found(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = False)