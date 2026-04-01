DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'proyectoree') THEN
      CREATE USER proyectoree WITH PASSWORD 'REE2026';
   END IF;
END
$$;

SELECT 'CREATE DATABASE ree_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ree_db')
\gexec

GRANT ALL PRIVILEGES ON DATABASE ree_db TO proyectoree;

\c ree_db

ALTER SCHEMA public OWNER TO proyectoree;

CREATE TABLE IF NOT EXISTS tipos_generacion (
    id SERIAL PRIMARY KEY,
    nombre TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS generacion (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP NOT NULL,
    tipo_id INTEGER NOT NULL,
    valor NUMERIC NOT NULL,
    
    CONSTRAINT fk_tipo
        FOREIGN KEY (tipo_id)
        REFERENCES tipos_generacion(id)
);

DO
$$
BEGIN
   IF NOT EXISTS (
      SELECT 1 FROM pg_constraint 
      WHERE conname = 'unique_fecha_tipo'
   ) THEN
      ALTER TABLE generacion
      ADD CONSTRAINT unique_fecha_tipo UNIQUE (fecha, tipo_id);
   END IF;
END
$$;

CREATE OR REPLACE VIEW generacion_completa AS
SELECT 
    g.fecha,
    t.nombre AS tipo,
    g.valor
FROM generacion g
JOIN tipos_generacion t ON g.tipo_id = t.id;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO proyectoree;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO proyectoree;