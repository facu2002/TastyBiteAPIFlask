
CREATE TABLE comentario (
  comentario_id INTEGER NOT NULL,
  fecha DATE NOT NULL,
  contenido TEXT NOT NULL,
  CONSTRAINT contenido_comentario CHECK (char_length(contenido) > 0 AND char_length(contenido) <= 500)
);


ALTER TABLE public.comentario OWNER TO postgres;

CREATE SEQUENCE public.comentario_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE public.comentario_id_seq OWNER TO postgres;

ALTER SEQUENCE public.comentario_id_seq OWNED BY public.comentario.comentario_id;

ALTER TABLE ONLY public.comentario ALTER COLUMN comentario_id SET DEFAULT nextval('public.comentario_id_seq'::regclass);

ALTER TABLE ONLY public.comentario
  ADD CONSTRAINT comentario_pk PRIMARY KEY (comentario_id);


CREATE OR REPLACE FUNCTION establecer_fecha() RETURNS TRIGGER AS $$
BEGIN
  NEW.fecha := CURRENT_DATE;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER establecer_fecha_comentario
BEFORE INSERT ON comentario
FOR EACH ROW
EXECUTE PROCEDURE establecer_fecha();