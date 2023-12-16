import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

from rutas.usuario import usuario_bp
from rutas.ingrediente import ingrediente_bp
from rutas.receta import receta_bp


app = Flask(__name__)


app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
app.register_blueprint(ingrediente_bp, url_prefix='/api/ingredientes')
app.register_blueprint(receta_bp, url_prefix='/api/recetas')


if __name__ == '__main__':
  app.run(debug=True)