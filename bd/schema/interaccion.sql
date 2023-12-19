CREATE TABLE interaccion (
  interaccion_id INTEGER NOT NULL,
  comentario_id INTEGER DEFAULT NULL,
  puntuacion_id INTEGER DEFAULT NULL,
  username TEXT NOT NULL,
  receta_id INTEGER NOT NULL,
  CONSTRAINT check_interaccion CHECK (
    (comentario_id IS NOT NULL AND puntuacion_id IS NULL) OR 
    (comentario_id IS NULL AND puntuacion_id IS NOT NULL))
);


ALTER TABLE public.interaccion OWNER TO postgres;

CREATE SEQUENCE public.interaccion_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE public.interaccion_id_seq OWNER TO postgres;

ALTER SEQUENCE public.interaccion_id_seq OWNED BY public.interaccion.interaccion_id;

ALTER TABLE ONLY public.interaccion ALTER COLUMN interaccion_id SET DEFAULT nextval('public.interaccion_id_seq'::regclass);

ALTER TABLE ONLY public.interaccion
  ADD CONSTRAINT interaccion_pk PRIMARY KEY (interaccion_id);

ALTER TABLE ONLY public.interaccion
  ADD CONSTRAINT username_fkey FOREIGN KEY (username) REFERENCES public.usuario(username) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.interaccion
  ADD CONSTRAINT receta_id_fkey FOREIGN KEY (receta_id) REFERENCES public.receta(receta_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.interaccion
  ADD CONSTRAINT comentario_id_fkey FOREIGN KEY (comentario_id) REFERENCES public.comentario(comentario_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.interaccion
  ADD CONSTRAINT puntuacion_id_fkey FOREIGN KEY (puntuacion_id) REFERENCES public.puntuacion(puntuacion_id) ON UPDATE CASCADE ON DELETE CASCADE;

CREATE OR REPLACE FUNCTION eliminar_comentario() RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM comentario WHERE comentario_id = OLD.comentario_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER eliminar_comentario_trigger
AFTER DELETE ON interaccion
FOR EACH ROW EXECUTE PROCEDURE eliminar_comentario();

CREATE OR REPLACE FUNCTION eliminar_puntuacion() RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM puntuacion WHERE puntuacion_id = OLD.puntuacion_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER eliminar_puntuacion_trigger
AFTER DELETE ON interaccion
FOR EACH ROW EXECUTE PROCEDURE eliminar_puntuacion();