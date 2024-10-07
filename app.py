from flask import *
import hashlib
from datetime import date
import re

app=Flask(__name__)
app.config.from_pyfile("config.py")

from models import db
from models import Usuario,Cultivo,Etapa,Plantacion,Ideales,EtapaCultivo
from imageAnalisis import DatosClimaticos


@app.route("/")
def index():
	return render_template("consultation.html")

@app.route("/create_crop",methods=["POST","GET"])
def createCrop():
	location=request.form.get("ubicacion")
	name=request.form.get("cropName")
	type=request.form.get("cropType")
	date=request.form.get("date")

def crearUsuario(id,correo0):
	usuario=Usuario(id_usuario=id,correo=correo0)
	db.session.add(usuario)
	db.session.commit()

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		print(date.today())
		print(app.config['SQLALCHEMY_DATABASE_URI'])
		app.run()




# if __name__=="__main__":
#     input("ingrese hectareas: ")
#     input("Ingrese coordenadas: ")
#     input("cultivo: ")