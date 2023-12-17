from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


comentario_bp = Blueprint('comentario', __name__)


#########################################################################################################################################


@comentario_bp.route('<int:comentario_id>', methods=['GET']) 
def get_comentario(comentario_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM comentario WHERE comentario_id = '{comentario_id}';")
    comentario = cursor.fetchone()
    cursor.close()
    conn.close()
    if comentario is None:
      return jsonify({"message": "comentario no encontrado"}), 404
    
    comentario = {
      "comentario_id": comentario[0],
      "fecha": comentario[1],
      "contenido": comentario[2]
    }
    return jsonify(comentario), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500


#########################################################################################################################################



# recibimos parametros por el body de la peticion
@comentario_bp.route('', methods=['POST'])
def post_comentario():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    data = request.get_json()
    if data.get('username') is None:
      return jsonify({"message": "No se ha enviado el username"}), 400
    if data.get('receta_id') is None:
      return jsonify({"message": "No se ha enviado el id de la receta"}), 400
    if data.get('contenido') is None:
      return jsonify({"message": "No se ha enviado el contenido del comentario"}), 400
    

    cursor.execute(f"INSERT INTO comentario (contenido) VALUES ('{data['contenido']}') RETURNING *;")
    nuevo_comentario = cursor.fetchone()
    cursor.execute(f"INSERT INTO interaccion (comentario_id, puntuacion_id, username, receta_id) VALUES ({nuevo_comentario[0]}, null, '{data['username']}', {data['receta_id']}) RETURNING *;")
    nueva_interaccion = cursor.fetchone()
    
    comentario = {
      "comentario_id": nuevo_comentario[0],
      "fecha": nuevo_comentario[1],
      "contenido": nuevo_comentario[2],
      "username": nueva_interaccion[3],
      "receta_id": nueva_interaccion[4]
    }
    
    conn.commit()
    cursor.close()
    conn.close()
    # retonarmos el mensaje de exito y el comentario creado
    return jsonify({"message": "comentario creado exitosamente", "comentario": comentario}), 201
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500


