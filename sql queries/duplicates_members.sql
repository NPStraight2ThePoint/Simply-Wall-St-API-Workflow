SELECT m.date, m.ticker, m.exchange, m.name, COUNT(*)
        FROM members m
        WHERE m.date = %s
        GROUP BY m.date, m.ticker, m.exchange, m.name
        HAVING COUNT(*) > 1
