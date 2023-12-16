
DROP DATABASE IF EXISTS tastybite;

CREATE DATABASE tastybite WITH TEMPLATE = template0 ENCODING = 'UTF8';

ALTER DATABASE tastybite OWNER TO postgres;

\connect tastybite

CREATE SCHEMA IF NOT EXISTS public;

ALTER SCHEMA public OWNER TO postgres;


-- Creamos las tablas en la base de datos
\i ./bd/schema/usuario.sql
\i ./bd/schema/categoria.sql
\i ./bd/schema/amigo.sql
\i ./bd/schema/receta.sql
\i ./bd/schema/ingrediente.sql
\i ./bd/schema/ranking.sql
\i ./bd/schema/usuario_receta.sql
\i ./bd/schema/receta_ingrediente.sql
\i ./bd/schema/patrocinador.sql
\i ./bd/schema/puntuacion.sql
\i ./bd/schema/comentario.sql
\i ./bd/schema/interaccion.sql

-- Insertamos las entradas en las tablas
\i ./bd/data/usuario_data.sql
\i ./bd/data/categoria_data.sql
\i ./bd/data/amigo_data.sql
\i ./bd/data/receta_data.sql
\i ./bd/data/ingrediente_data.sql
\i ./bd/data/usuario_receta_data.sql
\i ./bd/data/receta_ingrediente_data.sql
\i ./bd/data/patrocinador_data.sql
\i ./bd/data/puntuacion_data.sql
\i ./bd/data/comentario_data.sql
\i ./bd/data/interaccion_data.sql
