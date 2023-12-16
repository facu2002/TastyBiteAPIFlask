from flask import Blueprint, jsonify, request
import psycopg2
from db_connection import get_db_connection


usuario_bp = Blueprint('usuario', __name__)


#########################################################################################################################################


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



#########################################################################################################################################


@usuario_bp.route('', methods=['GET'])
def get_users():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()   
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion, data sera None
      data = None
    numero = data.get("numero") if (data is not None) else None
    if numero is not None:
      cursor.execute("SELECT * FROM usuario LIMIT %s;", (numero,))
    else:
      cursor.execute("SELECT * FROM usuario LIMIT 10;")
    users = cursor.fetchall()
    return jsonify(users), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()


#########################################################################################################################################


# recibimos parametros por el body de la peticion
@usuario_bp.route('', methods=['POST'])
def post_user():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute(f"INSERT INTO usuario (username, nombre, apellidos, descripcion_perfil, email) VALUES ('{data['username']}', '{data['nombre']}', '{data['apellidos']}', '{data['descripcion_perfil']}', '{data['email']}');")
    conn.commit()
    cursor.close()
    conn.close()
    # retonarmos el mensaje de exito y el usuario creado
    return jsonify({"message": "Usuario creado exitosamente", "usuario": data}), 201
  except Exception as e:
    if 'duplicate key value violates unique constraint' in str(e):
      return jsonify({"message": "El username ya existe"}), 409
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500


#########################################################################################################################################

