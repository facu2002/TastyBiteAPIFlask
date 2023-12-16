
CREATE TABLE patrocinador(
  patrocinador_id INTEGER NOT NULL,
  username TEXT,
  cantidad_donada DECIMAL(6,2),
  CONSTRAINT cantidad_donada_no_negativa CHECK (cantidad_donada >= 0)
);


ALTER TABLE public.patrocinador OWNER TO postgres;

CREATE SEQUENCE public.patrocinador_id_seq
  AS integer
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE public.patrocinador_id_seq OWNER TO postgres;

ALTER SEQUENCE public.patrocinador_id_seq OWNED BY public.patrocinador.patrocinador_id;

ALTER TABLE ONLY public.patrocinador ALTER COLUMN patrocinador_id SET DEFAULT nextval('public.patrocinador_id_seq'::regclass);


ALTER TABLE ONLY public.patrocinador
  ADD CONSTRAINT username_fkey FOREIGN KEY (username) REFERENCES public.usuario(username) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.patrocinador
  ADD CONSTRAINT patrocinador_pk PRIMARY KEY (patrocinador_id);