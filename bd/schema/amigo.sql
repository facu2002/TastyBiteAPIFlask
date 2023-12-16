CREATE TABLE amigo (
  username1 TEXT,
  username2 TEXT,
  CONSTRAINT amigos_diferentes CHECK (username1 != username2)
);

ALTER TABLE public.amigo OWNER TO postgres;

ALTER TABLE ONLY public.amigo
  ADD CONSTRAINT username1_fkey FOREIGN KEY (username1) REFERENCES public.usuario(username) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.amigo
  ADD CONSTRAINT username2_fkey FOREIGN KEY (username2) REFERENCES public.usuario(username) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.amigo
  ADD CONSTRAINT amigo_pk PRIMARY KEY (username1, username2);


CREATE OR REPLACE FUNCTION comprobar_amistad() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT 1 FROM amigo WHERE (username1 = NEW.username2 AND username2 = NEW.username1)) THEN
    RAISE EXCEPTION 'La amistad ya existe.';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER comprobar_amistad_before_insert
BEFORE INSERT ON amigo
FOR EACH ROW EXECUTE PROCEDURE comprobar_amistad();