CREATE TABLE categoria (
  categoria_id INTEGER NOT NULL,
  nombre TEXT NOT NULL,
  descripcion TEXT NOT NULL,
  CONSTRAINT nombre_categoria UNIQUE (nombre),
  CONSTRAINT no_espacios_nombre CHECK (nombre ~ '^[A-Za-z\s]*$' AND nombre !~ '^\s|\s$'),
  CONSTRAINT longitud_descripcion CHECK (LENGTH(descripcion) <= 250)
);

ALTER TABLE public.categoria OWNER TO postgres;

CREATE SEQUENCE public.categoria_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE public.categoria_id_seq OWNER TO postgres;

ALTER SEQUENCE public.categoria_id_seq OWNED BY public.categoria.categoria_id;

ALTER TABLE ONLY public.categoria ALTER COLUMN categoria_id SET DEFAULT nextval('public.categoria_id_seq'::regclass);

ALTER TABLE ONLY public.categoria
  ADD CONSTRAINT categoria_pk PRIMARY KEY (categoria_id);

