from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


patrocinador_bp = Blueprint('patrocinador', __name__)



#########################################################################################################################################

# GET /api/patrocinadores/:username

@patrocinador_bp.route('<string:username>', methods=['GET']) 
def get_patrocinador(username):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtenemos la lista de donaciones del usuario
    cursor.execute(f"SELECT * FROM patrocinador WHERE username = '{username}';")
    patrocinadores = cursor.fetchall()
    
    # Comprobamos si el usuario existe en la tabla de patrocinadores
    if patrocinadores is None:
      return jsonify({"message": "Usuario no encontrado"}), 404
    
    # Damos formato a la lista de donaciones
    patrocinadores = [{"patrocinador_id": patrocinador[0], "username": patrocinador[1], "cantidad_donada": patrocinador[2]} for patrocinador in patrocinadores]
    cursor.close()
    conn.close()

    return jsonify(patrocinadores), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
    

#########################################################################################################################################

# GET /api/patrocinadores

@patrocinador_bp.route('', methods=['GET'])
def get_patrocinadores():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Comprobamos que el número se pasa por el body de la petición
    try:
      data = request.get_json()
    except:
      # si no se envia ningun parametro por el body de la peticion, data sera None
      data = None
    numero = data.get("numero") if (data is not None) else None
    
    # Obtenemos la lista de patrocinadores
    if numero is not None:
      cursor.execute(f"SELECT username, SUM(cantidad_donada) AS cantidad_total FROM patrocinador GROUP BY username ORDER BY cantidad_total DESC LIMIT {numero};")
    else:
      cursor.execute("SELECT username, SUM(cantidad_donada) AS cantidad_total FROM patrocinador GROUP BY username ORDER BY cantidad_total DESC LIMIT 10;")
    
    # Damos formato a la lista de patrocinadores
    patrocinadores = cursor.fetchall()
    patrocinadores = [{"username": patrocinador[0], "cantidad_donada": patrocinador[1]} for patrocinador in patrocinadores]
    return jsonify(patrocinadores), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
  finally:
    cursor.close()
    conn.close()
