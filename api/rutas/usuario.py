from flask import Blueprint, jsonify, request
import psycopg2
from db_connection import get_db_connection


usuario_bp = Blueprint('usuario', __name__)


@usuario_bp.route('<string:username>', methods=['GET']) 
def get_user(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user is None:
      return jsonify({"message": "Usuario no encontrado"}), 404
    return jsonify(user), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500

# recibimos parametros por el body de la peticion
@usuario_bp.route('', methods=['POST'])
def post_user():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute(f"INSERT INTO usuario (username, password, nombre, apellido, email) VALUES ({data['username']}, {data['password']}, {data['nombre']}, {data['apellido']}, {data['email']})")
  
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Usuario creado exitosamente"}), 201
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
