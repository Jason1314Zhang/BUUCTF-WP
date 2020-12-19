import os 
from flask import (Flask
        import render_template
        import request
        import url_for
        import redirect
        import session
        import render_template_string) from flask_session
import Session
app = Flask(__name__) execfile('flag.py')
execfile('key.py')
FLAG = flag
app.secret_key = key


@app.route("/n1page", methods=["GET", "POST"])
def n1page():
    if request.method != "POST":
        return redirect(url_for("index"))
    n1code = request.form.get("n1code") or None 
    if n1code is not None:
        n1code = n1code.replace(".", "").replace(
            "_", "").replace("{", "").replace("}", "")
    if "n1code" not in session or session['n1code'] is None:
        session['n1code'] = n1code
        template = None
    if session['n1code'] is not None:
        template = '''<h1>N1 Page</h1> <div class="row> <div class="col-md-6 col-md-offset-3 center"> Hello : %s, why you don't look at our <a href='/article?name=article'>article</a>? </div> </div> ''' % session[
            'n1code']
        session['n1code'] = None
        return render_template_string(template)


@app.route("/", methods=["GET"])
def index():
    return render_template("main.html")


@app.route('/article', methods=['GET'])
def article():
    error = 0
    if 'name' in request.args:
        page = request.args.get('name')
    else:
        page = 'article'
    if page.find('flag') >= 0:
        page = 'notallowed.txt'
        try:
            template = open(
                '/home/nu11111111l/articles/{}'.format(page)).read()
        except Exception as e:
            template = e return render_template('article.html', template=template) if __name__ == "__main__": app.run(host='0.0.0.0', debug=False)
