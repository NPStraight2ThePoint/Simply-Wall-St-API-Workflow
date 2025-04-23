SELECT st.ticker, st.exchange, st.date, COUNT(*)
        FROM statements st
        WHERE st.date = %s
        GROUP BY st.ticker, st.exchange, st.date
        HAVING COUNT(*) > 1;