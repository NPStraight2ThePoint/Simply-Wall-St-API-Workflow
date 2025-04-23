WITH c_l_counts AS (
            SELECT 
                c.index_date,
                c."tickerSymbol",
                c."exchangeSymbol",
                COUNT(DISTINCT c."tickerSymbol" || c."exchangeSymbol") AS c_counts,
                COUNT(DISTINCT l.ticker_symbol || l.exchange_symbol) AS l_counts
            FROM companies c
            LEFT JOIN listings l 
                ON c."tickerSymbol" = l.ticker_symbol 
               AND c."exchangeSymbol" = l.exchange_symbol
            WHERE c.index_date = %s
            GROUP BY c.index_date, c."tickerSymbol", c."exchangeSymbol"
        ),
        c_st_counts AS (
            SELECT 
                c.index_date,
                c."tickerSymbol",
                c."exchangeSymbol",
                COUNT(*) AS c_counts,
                COUNT(DISTINCT st.ticker || st.exchange) AS st_counts
            FROM companies c
            LEFT JOIN statements st 
                ON c."tickerSymbol" = st.ticker
               AND c."exchangeSymbol" = st.exchange
            WHERE c.index_date = %s
            GROUP BY c.index_date, c."tickerSymbol", c."exchangeSymbol"
        )
        SELECT 
            c_l.index_date,
            c_l."tickerSymbol",
            c_l."exchangeSymbol",
            c_l.c_counts AS companies_count,
            c_l.l_counts AS listings_count,
            c_st.st_counts AS statements_count
        FROM c_l_counts c_l
        LEFT JOIN c_st_counts c_st 
            ON c_l.index_date = c_st.index_date
           AND c_l."tickerSymbol" = c_st."tickerSymbol"
           AND c_l."exchangeSymbol" = c_st."exchangeSymbol"
        WHERE c_l.l_counts = 0 OR c_st.st_counts = 0
        ORDER BY c_l."exchangeSymbol" ASC;