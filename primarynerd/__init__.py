from flask import Flask, render_template
import os
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))


auth = OIDCAuthentication(app,
                          issuer=app.config['OIDC_ISSUER'],
                          client_registration_info=app.config['OIDC_CLIENT_CONFIG'])

@app.route("/")
@auth.oidc_auth
def hello():
    return render_template("base.html")


@app.route('/logout')
@auth.oidc_logout
def logout():
    return redirect(url_for('hello'), 302)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
