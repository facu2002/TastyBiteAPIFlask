
CREATE TABLE puntuacion (
  puntuacion_id INTEGER NOT NULL,
  fecha DATE NOT NULL,
  nota INTEGER NOT NULL,
  CONSTRAINT nota_check CHECK (nota > 0 AND nota <= 5)
);


ALTER TABLE public.puntuacion OWNER TO postgres;

CREATE SEQUENCE public.puntuacion_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE public.puntuacion_id_seq OWNER TO postgres;

ALTER SEQUENCE public.puntuacion_id_seq OWNED BY public.puntuacion.puntuacion_id;

ALTER TABLE ONLY public.puntuacion ALTER COLUMN puntuacion_id SET DEFAULT nextval('public.puntuacion_id_seq'::regclass);

ALTER TABLE ONLY public.puntuacion
  ADD CONSTRAINT puntuacion_pk PRIMARY KEY (puntuacion_id);


CREATE OR REPLACE FUNCTION establecer_fecha() RETURNS TRIGGER AS $$
BEGIN
  NEW.fecha := CURRENT_DATE;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER establecer_fecha_puntuacion
BEFORE INSERT ON puntuacion
FOR EACH ROW
EXECUTE PROCEDURE establecer_fecha();