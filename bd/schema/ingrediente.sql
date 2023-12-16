CREATE TABLE ingrediente (
  ingrediente_id INTEGER NOT NULL,
  nombre TEXT NOT NULL, 
  descripcion TEXT NOT NULL,
  unidad_medida TEXT NOT NULL,
  CONSTRAINT nombre_ingrediente UNIQUE (nombre),
  CONSTRAINT longitud_nombre CHECK (char_length(nombre) > 0 AND char_length(nombre) <= 50),
  CONSTRAINT longitud_descripcion CHECK (char_length(descripcion) > 0 AND char_length(descripcion) <= 100),
  CONSTRAINT unidad_medida_valida CHECK (unidad_medida IN ('kg', 'g', 'l', 'ml', 'taza', 'cda', 'pizca'))
);

ALTER TABLE public.ingrediente OWNER TO postgres;

CREATE SEQUENCE public.ingrediente_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE public.ingrediente_id_seq OWNER TO postgres;

ALTER SEQUENCE public.ingrediente_id_seq OWNED BY public.ingrediente.ingrediente_id;

ALTER TABLE ONLY public.ingrediente ALTER COLUMN ingrediente_id SET DEFAULT nextval('public.ingrediente_id_seq'::regclass);


ALTER TABLE ONLY public.ingrediente
  ADD CONSTRAINT ingrediente_pk PRIMARY KEY (ingrediente_id);

