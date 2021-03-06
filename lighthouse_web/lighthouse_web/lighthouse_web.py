# all the imports
import os

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from neopixel import *

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , lighthouse-web.py

app.config.from_envvar('LIGHTHOUSE_SETTINGS', silent=True)

lighthouse = Lighthouse()

@app.route('/')
def show_entries():
    return render_template('index.html')
    
@app.route('/set', methods=['POST'])
def set():
#    if not session.get('logged_in'):
#        abort(401)

    op = request.form['op']
    color  = request.form['color']
    
    print "Op: %s - Color %s", op, color
    
    if op == 'aus':
        lighthouse.colorWipe(Color(0, 0, 0), ALL)
    elif op == 'zeile1':
        lighthouse.zeile(HexColor(color), ZEILE1)
    elif op == 'zeile2':
        lighthouse.zeile(HexColor(color), ZEILE2)
    elif op == 'zeile3':
        lighthouse.zeile(HexColor(color), ZEILE3)
    else:
        lighthouse.test()
        
    print 'New entry was successfully posted'
    return redirect(url_for('show_entries'))

@app.route('/level', methods=['POST'])
def level():
    zeile = request.form['zeile']
    level = request.form['level']
    on_color  = request.form['on_color']
    off_color  = request.form['off_color']
    
    if   zeile== 'zeile1': zeile = ZEILE1
    elif zeile== 'zeile2': zeile = ZEILE2
    elif zeile== 'zeile3': zeile = ZEILE3
    else: zeile = ALL
    
    
    lighthouse.level(HexColor(on_color), HexColor(off_color), zeile, int(level))
    
    print 'New entry was successfully posted'
    return redirect(url_for('show_entries'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
	
if __name__ == '__main__':
    app.run('0.0.0.0')    