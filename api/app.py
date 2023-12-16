import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect

from rutas.usuario import usuario_bp


app = Flask(__name__)

def get_db_connection():
  try:
    conn = psycopg2.connect(host='localhost',
    	database="tastybite",
        # user=os.environ['DB_USERNAME'],
        user="postgres",
        # password=os.environ['DB_PASSWORD']
        password="nueva_contraseña")
  except psycopg2.Error as e:
    print("Fallo en la conexión con la base de datos", e)
    raise e
  except Exception as e:
    print("Ha ocurrido un error", e)
    raise e
  return conn

# @app.route('/api/usuarios/<string:username>')
# def get_user(username)



app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')


if __name__ == '__main__':
  app.run(debug=True)