-- ============================================================
-- init_db.sql — Creación manual de la base de datos
-- Práctica 5 — XSS — UPQ S-203
--
-- NOTA: Este script es OPCIONAL. La aplicación crea la base de
-- datos y la tabla automáticamente al ejecutarse (ver db.py,
-- función init_db). Usa este script solo si prefieres crear la
-- estructura manualmente desde psql o pgAdmin.
-- ============================================================

-- 1. Crear la base de datos (ejecutar conectado a la BD "postgres")
-- CREATE DATABASE xss_lab;

-- 2. Conéctate a xss_lab y ejecuta lo siguiente:

CREATE TABLE IF NOT EXISTS comentarios (
    id      SERIAL PRIMARY KEY,
    autor   VARCHAR(100) NOT NULL DEFAULT 'Anónimo',
    texto   TEXT NOT NULL,
    fecha   TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Comentario inicial de ejemplo (opcional)
INSERT INTO comentarios (autor, texto)
VALUES ('Admin', 'Bienvenidos al blog de seguridad. Este es el primer comentario.')
ON CONFLICT DO NOTHING;

-- 4. Verifica que la tabla se haya creado correctamente
SELECT * FROM comentarios;
