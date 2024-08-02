CREATE OR REPLACE FUNCTION insert_default_roles()
RETURNS VOID AS $$
BEGIN
    INSERT INTO roles (id, name)
    VALUES 
        (1, 'CLIENTS'), 
        (2, 'OPERATIONS'), 
        (3, 'WORKSHOPS')
    ON CONFLICT (id) DO NOTHING; -- Evita insertar duplicados basados en el id
END;
$$ LANGUAGE plpgsql;

SELECT insert_default_roles();
