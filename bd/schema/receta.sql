CREATE TABLE receta (
  receta_id INTEGER NOT NULL,
  titulo TEXT NOT NULL,
  categoria_id INTEGER,
  instrucciones TEXT NOT NULL,
  tiempo INTEGER NOT NULL,
  raciones INTEGER NOT NULL,
  dificultad INTEGER NOT NULL,
  CONSTRAINT tiempo_no_negativo CHECK (tiempo >= 0),
  CONSTRAINT raciones_no_negativas CHECK (raciones >= 0),
  CONSTRAINT rango_dificultad CHECK (dificultad >= 1 AND dificultad <= 5),
  CONSTRAINT longitud_instrucciones CHECK (LENGTH(instrucciones) <= 1000),
  CONSTRAINT longitud_titulo CHECK (LENGTH(titulo) <= 100 AND LENGTH(titulo) > 0)
);

ALTER TABLE public.receta OWNER TO postgres;


CREATE SEQUENCE public.receta_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE public.receta_id_seq OWNER TO postgres;

ALTER SEQUENCE public.receta_id_seq OWNED BY public.receta.receta_id;

ALTER TABLE ONLY public.receta ALTER COLUMN receta_id SET DEFAULT nextval('public.receta_id_seq'::regclass);

ALTER TABLE ONLY public.receta
  ADD CONSTRAINT receta_pk PRIMARY KEY (receta_id);

ALTER TABLE ONLY public.receta
  ADD CONSTRAINT categoria_id_fkey FOREIGN KEY (categoria_id) REFERENCES public.categoria(categoria_id) ON UPDATE SET NULL ON DELETE SET NULL;
