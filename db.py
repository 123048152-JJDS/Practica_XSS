"""
db.py — Configuración de base de datos PostgreSQL con SQLAlchemy
Práctica 5 — Seguridad Informática — UPQ S-203

Define la conexión a PostgreSQL y el modelo de datos para los
comentarios usados en la demostración de XSS Almacenado.
"""

import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class Comentario(db.Model):
    """
    Tabla de comentarios — usada para demostrar XSS Almacenado.

    El campo `texto` se guarda TAL CUAL llega del formulario (sin
    sanitizar) a propósito, para que la ruta /vulnerable/almacenado
    pueda mostrar cómo un payload persiste en la base de datos real
    y se ejecuta cada vez que se lee.
    """
    __tablename__ = "comentarios"

    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(100), nullable=False, default="Anónimo")
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Comentario {self.id} de {self.autor}>"


def init_db(app):
    """
    Inicializa SQLAlchemy con la app de Flask y crea las tablas
    si no existen todavía.
    """
    db_user = os.environ.get("DB_USER", "postgres")
    db_pass = os.environ.get("DB_PASSWORD", "postgres")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "xss_lab")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Sembrar un comentario inicial si la tabla está vacía
        if Comentario.query.count() == 0:
            db.session.add(Comentario(
                autor="Admin",
                texto="Bienvenidos al blog de seguridad. Este es el primer comentario."
            ))
            db.session.commit()
