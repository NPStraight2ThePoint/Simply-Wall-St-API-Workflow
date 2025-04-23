SELECT ec.index_date, ec.exchange, COUNT(*)
        FROM exchanges_counts ec
        WHERE ec.index_date = %s
        GROUP BY ec.index_date, ec.exchange
        HAVING COUNT(*) > 1;