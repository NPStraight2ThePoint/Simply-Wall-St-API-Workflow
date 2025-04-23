SELECT c.index_date, c.id, COUNT(*)
        FROM companies c
        WHERE c.index_date = %s
        GROUP BY c.index_date, c.id
        HAVING COUNT(*) > 1
