# queries.py

QUERY_EXCHANGES = """
{
  exchanges {
    symbol
    companiesCount
  }
}
"""

QUERY_ALL_COMPANIES = """
query Companies($exchange: String!, $offset: Int!, $limit: Int!) {
  companies(
    exchange: $exchange,
    offset: $offset,
    limit: $limit
  ) {
    id
    exchangeSymbol
    tickerSymbol
    name
    marketCapUSD
    primaryIndustry { name }
    secondaryIndustry { name }
    tertiaryIndustry { name }
    market { name iso2 }
    active
    classificationStatus
    insiderTransactions {
      type
      ownerName
      ownerType
      description
      tradeDateMin
      tradeDateMax
      shares
      priceMin
      priceMax
      transactionValue
      percentageSharesTraded
      percentageChangeTransShares
      isManagementInsider
      filingDate
    }
    statements {
      name
      title
      area
      type
      value
      outcome
      description
      state
      severity
      outcomeName
    }
    members {
      age
      name
      title
      tenure
      compensation
    }
    owners {
      name
      type
      sharesHeld
      holdingDate
      periodStartDate
      periodEndDate
      rankSharesHeld
      rankSharesSold
    }
  }
}
"""

QUERY_COMPANY_BY_ID = """
query Company($id: ID!) {
  company(id: $id) {
    id
    exchangeSymbol
    tickerSymbol
    name
    marketCapUSD
    primaryIndustry { name }
    secondaryIndustry { name }
    tertiaryIndustry { name }
    market { name iso2 }
    active
    classificationStatus
    insiderTransactions {
      type
      ownerName
      ownerType
      description
      tradeDateMin
      tradeDateMax
      shares
      priceMin
      priceMax
      percentageSharesTraded
      percentageChangeTransShares
      isManagementInsider
      filingDate
    }
    statements {
      name
      title
      area
      type
      value
      outcome
      description
      state
      severity
      outcomeName
    }
    members {
      age
      name
      title
      tenure
      compensation
    }
    owners {
      name
      type
      sharesHeld
      holdingDate
      periodStartDate
      periodEndDate
      rankSharesHeld
      rankSharesSold
    }
  }
}
"""

QUERY_ALL_COMPANIES_MINIMAL = """
query ($exchange: String!, $limit: Int!, $offset: Int!) {
  companies(exchange: $exchange, limit: $limit, offset: $offset) {
    id
    name
    tickerSymbol
    exchangeSymbol
    active
    marketCapUSD
  }
}
"""