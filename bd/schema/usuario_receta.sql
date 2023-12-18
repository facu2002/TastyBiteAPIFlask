
CREATE TABLE usuario_receta (
  username TEXT,
  receta_id INTEGER,
  CONSTRAINT receta_id_unica UNIQUE (receta_id)
);

ALTER TABLE public.usuario_receta OWNER TO postgres;

ALTER TABLE ONLY public.usuario_receta
  ADD CONSTRAINT username_fkey FOREIGN KEY (username) REFERENCES public.usuario(username) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.usuario_receta
  ADD CONSTRAINT receta_id_fkey FOREIGN KEY (receta_id) REFERENCES public.receta(receta_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.usuario_receta
  ADD CONSTRAINT usuario_receta_pk PRIMARY KEY (username, receta_id);

CREATE OR REPLACE FUNCTION actualizar_ranking() RETURNS TRIGGER AS $$
BEGIN
  -- Actualizar el ranking del usuario si ya existe
  IF EXISTS (SELECT 1 FROM ranking WHERE username = NEW.username) THEN
    UPDATE ranking
    SET n_recetas = (SELECT COUNT(*) FROM usuario_receta WHERE username = NEW.username)
    WHERE username = NEW.username;
  -- Si no existe, insertar un nuevo registro en el ranking
  ELSE
    INSERT INTO ranking(username, n_recetas)
    VALUES (NEW.username, (SELECT COUNT(*) FROM usuario_receta WHERE username = NEW.username));
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER actualizar_ranking_trigger
AFTER INSERT OR UPDATE OR DELETE ON usuario_receta
FOR EACH ROW EXECUTE PROCEDURE actualizar_ranking();

CREATE OR REPLACE FUNCTION eliminar_receta() RETURNS TRIGGER AS $$
BEGIN
  DELETE FROM receta WHERE receta_id = OLD.receta_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER eliminar_receta_trigger
AFTER DELETE ON usuario_receta
FOR EACH ROW EXECUTE PROCEDURE eliminar_receta();
