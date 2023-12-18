CREATE TABLE ranking (
  username TEXT,
  n_recetas INTEGER
);

ALTER TABLE ONLY public.ranking
  ADD CONSTRAINT username_fkey FOREIGN KEY (username) REFERENCES public.usuario(username) ON UPDATE CASCADE ON DELETE CASCADE;
