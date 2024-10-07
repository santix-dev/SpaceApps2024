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
	plantaciones=db.session.query(Plantacion).filter(Plantacion.id_usuario==1).all()
	print(plantaciones)
	return render_template("myCrops.html",plantaciones=plantaciones)

@app.route("/create_crop",methods=["POST","GET"])
def createCrop():
	location=request.form.get("ubicacion")
	name=request.form.get("cropName")
	type=request.form.get("cropType")
	date=request.form.get("date")

@app.route("/plantation",methods=["POST","GET"])
def plantation():
	plantacion={
		"variedad": "red globe",
		"ubicacion": "calingasta",
		"recomendacion": """1. Water Management
	Apply 296,000 gallons of water
	in the next 3 days. Increase 
	irrigation to 144,700 gallons 
	next week to account for rising 
	temperatures. \n
2. Canopy Control
	Manage the canopy to prevent 
	sunburn as temperatures rise. 
	Ensure leaves protect grapes from 
	direct sunlight. Don't stress vines
	during stage II (rapid cell 
	division and berry growth); 
	the fruit is very susceptible 
	to sunburn during this critical 
	phase.\n
3. Temperature Impact on Wine Quality
	Rising temperatures can lead
	to faster ripening, reducing 
	acidity and increasing sugar 
	levels. Monitor closely to 
	maintain balance for optimal 
	Zinfandel flavor."""
	}
	return render_template("plantation.html", plantacion=plantacion)




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