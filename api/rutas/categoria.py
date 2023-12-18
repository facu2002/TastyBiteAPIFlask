from flask import Blueprint, jsonify, request
from db_connection import get_db_connection


categoria_bp = Blueprint('categoria', __name__)


#########################################################################################################################################

# GET /api/categorias/:categoria_id

@categoria_bp.route('<int:categoria_id>', methods=['GET']) 
def get_categoria(categoria_id):
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Obtenemos la categoria con el id especificado
    cursor.execute(f"SELECT * FROM categoria WHERE categoria_id = '{categoria_id}';")
    categoria = cursor.fetchone()
    
    # Comprobamos si la categoria existe
    if categoria is None:
      return jsonify({"message": "categoria no encontrado"}), 404    
    
    cursor.close()
    conn.close()
    
    # Damos formato a la categoria
    categoria = {
      "categoria_id": categoria[0],
      "nombre": categoria[1],
      "descripcion": categoria[2]
    }
    return jsonify(categoria), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  


#########################################################################################################################################

# GET /api/categorias

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
    
    # Comprobamos que el número se pasa por el body de la petición y obtenemos las categorias
    if numero is not None:
      cursor.execute(f"SELECT * FROM categoria LIMIT {numero};")
    else:
      cursor.execute("SELECT * FROM categoria LIMIT 10;")

    # Damos formato a las categorias
    categorias = cursor.fetchall()
    categorias = [{"categoria_id": categoria[0], "nombre": categoria[1], "descripcion": categoria[2]} for categoria in categorias]
    return jsonify(categorias), 200
  except Exception as e:
    return jsonify({"message": "Ha ocurrido un error", "error": f"Errores con {e}"}), 500
  
  finally:
    cursor.close()
    conn.close()
