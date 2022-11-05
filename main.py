from flask import Flask, render_template, request, session, url_for,redirect
from livereload import Server
import random

app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True
app.secret_key = b'6hc/_gsh,./;2ZZx3c6_s,1//'
@app.route('/')
def base_page():
    return render_template(
		'alku.html'
	)

def seuraava_lasku(taulut:list, kertomat:list):
    tulokset = {}
    kertoja = random.sample(taulut, k=1)
    kerrottava = random.sample(kertomat, k=1)
    tulokset["kertoja"] = int(kertoja[0])
    tulokset["kerrottava"] = int(kerrottava[0])
    tulokset["tulos"] = kertoja[0] * kerrottava[0]
    return tulokset

@app.route('/laskut',methods = ['POST', 'GET'])
def laskut():
    if request.method == 'POST':
        lasku = request.form.to_dict()
        if list(lasku.keys())[0][0:5] == "taulu":
            kertomat = [1,2,3,4,5,6,7,8,9,10]
            taulut = []
            for avain, arvo in lasku.items():
                taulut.append(int(avain[5:]))
            session['taulut'] = taulut
            session['kertomat'] = kertomat
            session['pisteet'] = 0
            session['virheet'] = 0
            session['erä'] = 0
            #pisteet = session('pisteet')
        else:
            # jos oikea vastaus, lisätään piste
            if int(lasku['vastaus']) == session['tulos']:
                session['pisteet'] = session.get('pisteet') + 1
            else:
                session['virheet'] = session.get('virheet') + 1
            session['erä'] = session.get('erä') + 1
            if session['erä'] == session['pisteet_max']:
                return redirect(url_for('tulokset'))

        session['pisteet_max'] = 20
        session['piste_prosentti'] = laske_piste_prosentti(session['pisteet'], session['pisteet_max'])
        session['virhe_prosentti'] = laske_piste_prosentti(session['virheet'], session['pisteet_max'])
        
        tulokset = seuraava_lasku(session['taulut'], session["kertomat"])
        session['kertoja'] = tulokset['kertoja']
        session['kerrottava'] = tulokset['kerrottava']
        session['tulos'] = tulokset['tulos']

        return render_template("laskut.html")	

def laske_piste_prosentti(pisteet:int, pisteet_max:int):
    if pisteet == 0:
        return 0
    else:
        return 100 * pisteet/pisteet_max 

@app.route('/tulokset/')
def tulokset():
    session["var"] = 0
    return render_template(
		'tulokset.html'
	)


if __name__ == "__main__": 
    server = Server(app.wsgi_app)
    server.serve()
	