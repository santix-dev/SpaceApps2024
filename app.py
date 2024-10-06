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
	print("2")


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