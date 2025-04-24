WITH m_cte AS (
            SELECT 
                COUNT(m.ticker) AS members_no,
                m.date,
                m.exchange,
                m.ticker AS unique_ticker
            FROM members m
            WHERE m.date = %s
            GROUP BY m.date, m.exchange, m.ticker
        ),
        o_cte AS (
            SELECT 
                COUNT(o.ticker) AS owners_no,
                o.date,
                o.exchange,
                o.ticker AS unique_ticker
            FROM owners o
            WHERE o.date = %s
            GROUP BY o.date, o.exchange, o.ticker
        ),
        it_cte AS (
            SELECT 
                COUNT(it.ticker) AS it_itd_no,
                it.date,
                it.exchange,
                it.ticker AS unique_ticker
            FROM insider_transactions it
            WHERE it.date = %s
            GROUP BY it.date, it.exchange, it.ticker
        )

        SELECT 
            c.index_date,
            c."tickerSymbol",
            c."exchangeSymbol",
            COALESCE(m_cte.members_no, 0) AS members_no,
            COALESCE(o_cte.owners_no, 0) AS owners_no,
            COALESCE(it_cte.it_itd_no, 0) AS it_itd_no
        FROM companies c
        LEFT JOIN m_cte ON c."tickerSymbol" = m_cte.unique_ticker AND c."exchangeSymbol" = m_cte.exchange
        LEFT JOIN o_cte ON c."tickerSymbol" = o_cte.unique_ticker AND c."exchangeSymbol" = o_cte.exchange
        LEFT JOIN it_cte ON c."tickerSymbol" = it_cte.unique_ticker AND c."exchangeSymbol" = it_cte.exchange
        WHERE c.index_date = %s
        ORDER BY c."exchangeSymbol" ASC;