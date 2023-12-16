
CREATE TABLE receta_ingrediente (
  receta_id INTEGER,
  ingrediente_id INTEGER
);

ALTER TABLE public.receta_ingrediente OWNER TO postgres;

ALTER TABLE ONLY public.receta_ingrediente
  ADD CONSTRAINT receta_id_fkey FOREIGN KEY (receta_id) REFERENCES public.receta(receta_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.receta_ingrediente
  ADD CONSTRAINT ingrediente_id_fkey FOREIGN KEY (ingrediente_id) REFERENCES public.ingrediente(ingrediente_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.receta_ingrediente
  ADD CONSTRAINT receta_ingrediente_pk PRIMARY KEY (receta_id, ingrediente_id);
