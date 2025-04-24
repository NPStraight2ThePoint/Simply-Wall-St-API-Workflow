SELECT l.date, l.id, COUNT(*)
        FROM listings l
        WHERE l.date = %s
        GROUP BY l.date, l.id
        HAVING COUNT(*) > 1
