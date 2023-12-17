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

