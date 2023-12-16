
DROP DATABASE IF EXISTS tastybite;

CREATE DATABASE tastybite WITH TEMPLATE = template0 ENCODING = 'UTF8';

ALTER DATABASE tastybite OWNER TO postgres;

\connect tastybite

CREATE SCHEMA IF NOT EXISTS public;

ALTER SCHEMA public OWNER TO postgres;


-- Creamos las tablas en la base de datos
\i ./schema/usuario.sql
\i ./schema/categoria.sql
\i ./schema/amigo.sql
\i ./schema/receta.sql
\i ./schema/ingrediente.sql
\i ./schema/ranking.sql
\i ./schema/usuario_receta.sql
\i ./schema/receta_ingrediente.sql
\i ./schema/patrocinador.sql
\i ./schema/puntuacion.sql
\i ./schema/comentario.sql
\i ./schema/interaccion.sql

-- Insertamos las entradas en las tablas
\i ./data/usuario_data.sql
\i ./data/categoria_data.sql
\i ./data/amigo_data.sql
\i ./data/receta_data.sql
\i ./data/ingrediente_data.sql
\i ./data/usuario_receta_data.sql
\i ./data/receta_ingrediente_data.sql
\i ./data/patrocinador_data.sql
\i ./data/puntuacion_data.sql
\i ./data/comentario_data.sql
\i ./data/interaccion_data.sql
