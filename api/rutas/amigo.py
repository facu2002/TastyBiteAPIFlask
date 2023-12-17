from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


amigo_bp = Blueprint('amigo', __name__)


#########################################################################################################################################


@amigo_bp.route('<string:username>', methods=['GET']) 
def get_amigos(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM amigo WHERE username1 = '{username}';")
    usuarios1 = cursor.fetchall()
    usuarios1 = [{"amigo": usuario[1]} for usuario in usuarios1]
    
    cursor.execute(f"SELECT * FROM amigo WHERE username2 = '{username}';")
    usuarios2 = cursor.fetchall()
    usuarios2 = [{"amigo": usuario[0]} for usuario in usuarios2]
    
    usuarios = usuarios1 + usuarios2
    
    cursor.close()
    conn.close()
    if usuarios is None:
      return jsonify({"message": "Usuario no encontrado"}), 404
    return jsonify(usuarios), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500


#########################################################################################################################################


# recibimos parametros por el body de la peticion
@amigo_bp.route('', methods=['POST'])
def post_amigo():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute(f"INSERT INTO amigo (username1, username2) VALUES ('{data['username1']}', '{data['username2']}');")
    cursor.execute(f"SELECT * FROM amigo WHERE username1 = '{data['username1']}' AND username2 = '{data['username2']}';")
    amigos = cursor.fetchone()
    amigos = {
      "username1": amigos[0],
      "username2": amigos[1]
    }
    conn.commit()
    cursor.close()
    conn.close()
    # retonarmos el mensaje de exito y el usuario creado
    return jsonify({"message": "Amigos añadidos exitosamente", "amigos": amigos}), 201
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500



#########################################################################################################################################


@amigo_bp.route('<string:username>', methods=['DELETE'])
def delete_amigo(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()

    cursor.execute(f"DELETE FROM amigo WHERE username1 = '{data['username']}' AND username2 = '{username}';")
    cursor.execute(f"DELETE FROM amigo WHERE username1 = '{username}' AND username2 = '{data['username']}';")
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Amigos eliminados con éxito"}), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
