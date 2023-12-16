from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


patrocinador_bp = Blueprint('patrocinador', __name__)



#########################################################################################################################################


@patrocinador_bp.route('<string:username>', methods=['GET']) 
def get_patrocinador(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM patrocinador WHERE username = '{username}';")
    patrocinadores = cursor.fetchall()
    patrocinadores = [{"patrocinador_id": patrocinador[0], "username": patrocinador[1], "cantidad_donada": patrocinador[2]} for patrocinador in patrocinadores]
    cursor.close()
    conn.close()
    if patrocinadores is None:
      return jsonify({"message": "Usuario no encontrado"}), 404

    return jsonify(patrocinadores), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500


#########################################################################################################################################


@patrocinador_bp.route('', methods=['GET'])
def get_patrocinadores():
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
      cursor.execute(f"SELECT username, SUM(cantidad_donada) AS cantidad_total FROM patrocinador GROUP BY username ORDER BY cantidad_total DESC LIMIT {numero};")
    else:
      cursor.execute("SELECT username, SUM(cantidad_donada) AS cantidad_total FROM patrocinador GROUP BY username ORDER BY cantidad_total DESC LIMIT 10;")
    patrocinadores = cursor.fetchall()
    patrocinadores = [{"username": patrocinador[0], "cantidad_donada": patrocinador[1]} for patrocinador in patrocinadores]
    return jsonify(patrocinadores), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()
