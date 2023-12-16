import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

from rutas.usuario import usuario_bp


app = Flask(__name__)


app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')


if __name__ == '__main__':
  app.run(debug=True)