from __main__ import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Usuario(db.Model):
	__tablename__="usuario"
	id_usuario=db.Column(db.Integer,primary_key=True)
	correo=db.Column(db.String(50),nullable=False)





class Cultivo(db.Model):
     __tablename__="cultivo"
     nombre_cultivo=db.Column(db.String(50),nullable=False)
     variedad=db.Column(db.String(50),nullable=False)
     id_cultivo=db.Column(db.Integer,primary_key=True)

class Etapa(db.Model):
    __tablename__="etapa"
    id_etapa=db.Column(db.Integer,primary_key=True)
    nombre_etapa=db.Column(db.String(50),nullable=False)
    dia_inicio=db.Column(db.Integer,nullable=False)
    dia_fin=db.Column(db.Integer,nullable=False)
        
class Ideales(db.Model):
    
    __tablename__="ideales"
    id_ideales=db.Column(db.Integer,primary_key=True)
    id_cultivo=db.Column(db.Integer,db.ForeignKey("cultivo.id_cultivo"))
    temp=db.Column(db.Integer,nullable=False)
    precip=db.Column(db.Integer,nullable=False)
    viento=db.Column(db.Integer,nullable=False)
    hum=db.Column(db.Integer,nullable=False)
    et=db.Column(db.Integer,nullable=False)
    rad=db.Column(db.Integer,nullable=False)

class EtapaCultivo(db.Model):
    __tablename__="etapa_cultivo"
    id_etapa_cultivo=db.Column(db.Integer,primary_key=True)
    id_etapa=db.Column(db.Integer,db.ForeignKey("etapa.id_etapa"))
    id_cultivo=db.Column(db.Integer,db.ForeignKey("cultivo.id_cultivo"))
    nec_hid=db.Column(db.String(20),nullable=False)

class Plantacion(db.Model):
    __tablename__="plantacion"
    id_plantacion=db.Column(db.Integer,primary_key=True)
    id_usuario=db.Column(db.Integer,db.ForeignKey("usuario.id_usuario"))
    id_cultivo=db.Column(db.Integer,db.ForeignKey("cultivo.id_cultivo"))
    fecha_plantacion=db.Column(db.Date,nullable=False)
    coordenadas=db.Column(db.String(22),nullable=False)
    
