
from flask import Flask, render_template, request, url_for, redirect

from rutas.usuario import usuario_bp
from rutas.ingrediente import ingrediente_bp
from rutas.receta import receta_bp
from rutas.categoria import categoria_bp
from rutas.comentario import comentario_bp
from rutas.puntuacion import puntuacion_bp
from rutas.amigo import amigo_bp
from rutas.ranking import ranking_bp
from rutas.patrocinador import patrocinador_bp

app = Flask(__name__)


app.register_blueprint(usuario_bp, url_prefix='/api/usuarios')
app.register_blueprint(ingrediente_bp, url_prefix='/api/ingredientes')
app.register_blueprint(receta_bp, url_prefix='/api/recetas')
app.register_blueprint(categoria_bp, url_prefix='/api/categorias')
app.register_blueprint(comentario_bp, url_prefix='/api/comentarios')
app.register_blueprint(puntuacion_bp, url_prefix='/api/puntuaciones')
app.register_blueprint(amigo_bp, url_prefix='/api/amigos')
app.register_blueprint(ranking_bp, url_prefix='/api/ranking')
app.register_blueprint(patrocinador_bp, url_prefix='/api/patrocinadores')


if __name__ == '__main__':
  app.run(debug=True)