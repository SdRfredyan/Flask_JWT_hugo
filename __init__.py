from flask import Flask
from flask import render_template
from flask import json
from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
# Configuration du module JWT  #aa
app.config["JWT_SECRET_KEY"] = "Ma_clé_secrete"  # Ma clée privée
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Expiration du token après 1h
jwt = JWTManager(app)
  
@app.route('/')
def hello_world():
    return render_template('accueil.html')  #a

# Création d'une route qui vérifie l'utilisateur et retour un Jeton JWT si ok.
# La fonction create_access_token() est utilisée pour générer un jeton JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
  
@app.route("/admin", methods=["POST"])
def admin():
    username = request.json.get("username", None)
    password = request.json.get("password", None) 
    if username != "admin" or password != "secure":
        return jsonify({"msg": "Mauvais utilisateur ou mot de passe"}), 401
    # Génération du token si l'authentification réussit
    access_token = create_access_token(identity=username)
    # Renvoie à la fois le message de succès et le token
    return jsonify({
        "msg": "Connecté en admin",
        "access_token": access_token})

@app.route('/formulaire')
def hello_world():
    return render_template('formulaire.html')

# Route protégée par un jeton valide
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
                                                                                                               
if __name__ == "__main__":
  app.run(debug=True)
  
