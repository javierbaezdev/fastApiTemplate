DELIMITER //

CREATE PROCEDURE insert_default_roles()
BEGIN
    INSERT IGNORE INTO roles (id, name, created_at, updated_at, is_deleted)
    VALUES 
        (1, 'CLIENTS', NOW(), NOW(), 0), 
        (2, 'OPERATIONS', NOW(), NOW(), 0), 
        (3, 'WORKSHOPS', NOW(), NOW(), 0);
END//

DELIMITER ;


CALL insert_default_roles()
