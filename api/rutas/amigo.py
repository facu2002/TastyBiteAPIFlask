from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


amigo_bp = Blueprint('amigo', __name__)


#########################################################################################################################################

# GET /api/amigos/:username

@amigo_bp.route('<string:username>', methods=['GET']) 
def get_amigos(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtenemos los amigos del username especificado para un sentido
    cursor.execute(f"SELECT * FROM amigo WHERE username1 = '{username}';")
    usuarios1 = cursor.fetchall()
    usuarios1 = [{"amigo": usuario[1]} for usuario in usuarios1]
    
    # Obtenemos los amigos del username especificado para el otro sentido
    cursor.execute(f"SELECT * FROM amigo WHERE username2 = '{username}';")
    usuarios2 = cursor.fetchall()
    usuarios2 = [{"amigo": usuario[0]} for usuario in usuarios2]
    
    # Unimos los dos conjuntos de amigos
    usuarios = usuarios1 + usuarios2
    
    cursor.close()
    conn.close()
    if usuarios is None:
      return jsonify({"message": "Usuario no encontrado"}), 404
    return jsonify(usuarios), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  


#########################################################################################################################################

# POST /api/amigos

@amigo_bp.route('', methods=['POST'])
def post_amigo():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    
    # Insertamos el amigo en la base de datos
    cursor.execute(f"INSERT INTO amigo (username1, username2) VALUES ('{data['username1']}', '{data['username2']}');")
    cursor.execute(f"SELECT * FROM amigo WHERE username1 = '{data['username1']}' AND username2 = '{data['username2']}';")
    amigos = cursor.fetchone()
    
    # Damos formato al amigo
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

# DELETE /api/amigos/:username

@amigo_bp.route('<string:username>', methods=['DELETE'])
def delete_amigo(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()

    # Eliminamos el amigo de la base de datos en ambos sentidos
    cursor.execute(f"DELETE FROM amigo WHERE username1 = '{data['username']}' AND username2 = '{username}';")
    cursor.execute(f"DELETE FROM amigo WHERE username1 = '{username}' AND username2 = '{data['username']}';")
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Amigos eliminados con éxito"}), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
