WITH c_counts AS (
            SELECT c."exchangeSymbol", COUNT(*) AS c_count
            FROM companies c
            WHERE c.index_date = %s
            GROUP BY c."exchangeSymbol"
        ),
        l_counts AS (
            SELECT l.exchange_symbol, COUNT(*) AS l_count
            FROM listings l
            WHERE l.date = %s
            GROUP BY l.exchange_symbol
        ),
        st_counts AS (
            SELECT st.exchange, COUNT(*) AS st_count
            FROM statements st
            WHERE st.date = %s
            GROUP BY st.exchange
        )

        SELECT 
            ec.*,
            COALESCE(cc.c_count, 0) AS c_count,
            COALESCE(cc.c_count, 0) - ec.company_count AS c_count_diff,
            COALESCE(lc.l_count, 0) AS l_count,
            COALESCE(lc.l_count, 0) - ec.company_count AS l_count_diff,
            COALESCE(sc.st_count, 0) AS st_count,
            COALESCE(sc.st_count, 0) - ec.company_count AS st_count_diff,
            (
                (COALESCE(cc.c_count, 0) - ec.company_count) +
                (COALESCE(lc.l_count, 0) - ec.company_count) +
                (COALESCE(sc.st_count, 0) - ec.company_count)
            ) / 3.0 AS avg_diff
        FROM exchanges_counts ec
        LEFT JOIN c_counts cc ON ec.exchange = cc."exchangeSymbol"
        LEFT JOIN l_counts lc ON ec.exchange = lc.exchange_symbol
        LEFT JOIN st_counts sc ON ec.exchange = sc.exchange
        ORDER BY avg_diff DESC;
