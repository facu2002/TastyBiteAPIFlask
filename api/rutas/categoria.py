from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


categoria_bp = Blueprint('categoria', __name__)


@categoria_bp.route('<int:categoria_id>', methods=['GET']) 
def get_categoria(categoria_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM categoria WHERE categoria_id = '{categoria_id}';")
    categoria = cursor.fetchone()
    cursor.close()
    conn.close()
    if categoria is None:
      return jsonify({"message": "categoria no encontrado"}), 404    
    categoria = {
      "categoria_id": categoria[0],
      "nombre": categoria[1],
      "descripcion": categoria[2]
    }
    return jsonify(categoria), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500


#########################################################################################################################################


@categoria_bp.route('', methods=['GET'])
def get_categorias():
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
      cursor.execute(f"SELECT * FROM categoria LIMIT {numero};")
    else:
      cursor.execute("SELECT * FROM categoria LIMIT 10;")
    categorias = cursor.fetchall()
    # convertimos la lista de tuplas en una lista de diccionarios
    categorias = [{"categoria_id": categoria[0], "nombre": categoria[1], "descripcion": categoria[2]} for categoria in categorias]
    return jsonify(categorias), 200
  except Exception as e:
    print("Ha ocurrido un error", e)
    return jsonify({"message": "Ha ocurrido un error"}), 500
  finally:
    cursor.close()
    conn.close()
