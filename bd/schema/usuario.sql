CREATE TABLE usuario (
  username TEXT,
  nombre TEXT NOT NULL,
  apellidos TEXT NOT NULL,
  descripcion_perfil TEXT NOT NULL,
  email TEXT NOT NULL,
  CONSTRAINT no_espacios_username CHECK (username !~ '\s'),
  CONSTRAINT no_espacios_nombre CHECK (nombre ~ '^[A-Za-z\s]*$' AND nombre !~ '^\s|\s$'),
  CONSTRAINT longitud_username CHECK (LENGTH(username) <= 20 AND LENGTH(username) > 0),
  CONSTRAINT longitud_nombre CHECK (LENGTH(nombre) <= 50),
  CONSTRAINT no_espacios_apellidos CHECK (nombre ~ '^[A-Za-z\s]*$' AND nombre !~ '^\s|\s$'),
  CONSTRAINT longitud_apellidos CHECK (LENGTH(apellidos) <= 50),
  CONSTRAINT longitud_descripcion CHECK (LENGTH(descripcion_perfil) <= 250),
  CONSTRAINT email_valido CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

ALTER TABLE public.usuario OWNER TO postgres;


ALTER TABLE ONLY public.usuario
  ADD CONSTRAINT username_pk PRIMARY KEY (username);
