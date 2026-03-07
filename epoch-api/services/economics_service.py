import os
import requests
import yfinance as yf

# Map country names to their currency code and major stock index ticker
COUNTRY_ECONOMIC_DATA = {
    "United States": {"currency": "USD", "index": "^GSPC", "index_name": "S&P 500"},
    "Canada": {"currency": "CAD", "index": "^GSPTSE", "index_name": "TSX"},
    "Mexico": {"currency": "MXN", "index": "^MXX", "index_name": "IPC"},
    "Iran": {"currency": "IRR", "index": None, "index_name": None},
    "Iraq": {"currency": "IQD", "index": None, "index_name": None},
    "Israel": {"currency": "ILS", "index": "^TA125.TA", "index_name": "TA-125"},
    "Palestine": {"currency": "ILS", "index": None, "index_name": None},
    "Syria": {"currency": "SYP", "index": None, "index_name": None},
    "Yemen": {"currency": "YER", "index": None, "index_name": None},
    "Saudi Arabia": {"currency": "SAR", "index": "^TASI.SR", "index_name": "Tadawul"},
    "Turkey": {"currency": "TRY", "index": "XU100.IS", "index_name": "BIST 100"},
    "Lebanon": {"currency": "LBP", "index": None, "index_name": None},
    "Jordan": {"currency": "JOD", "index": None, "index_name": None},
    "Afghanistan": {"currency": "AFN", "index": None, "index_name": None},
    "Pakistan": {"currency": "PKR", "index": "^KSE100", "index_name": "KSE 100"},
    "Kuwait": {"currency": "KWD", "index": None, "index_name": None},
    "Qatar": {"currency": "QAR", "index": None, "index_name": None},
    "UAE": {"currency": "AED", "index": "^DFMGI", "index_name": "DFM"},
    "Oman": {"currency": "OMR", "index": None, "index_name": None},
    "Egypt": {"currency": "EGP", "index": "^EGX30", "index_name": "EGX 30"},
    "Russia": {"currency": "RUB", "index": None, "index_name": None},
    "Ukraine": {"currency": "UAH", "index": None, "index_name": None},
    "United Kingdom": {"currency": "GBP", "index": "^FTSE", "index_name": "FTSE 100"},
    "France": {"currency": "EUR", "index": "^FCHI", "index_name": "CAC 40"},
    "Germany": {"currency": "EUR", "index": "^GDAXI", "index_name": "DAX"},
    "China": {"currency": "CNY", "index": "^SSEC", "index_name": "Shanghai Composite"},
    "India": {"currency": "INR", "index": "^BSESN", "index_name": "BSE Sensex"},
    "Japan": {"currency": "JPY", "index": "^N225", "index_name": "Nikkei 225"},
    "South Korea": {"currency": "KRW", "index": "^KS11", "index_name": "KOSPI"},
    "North Korea": {"currency": "KPW", "index": None, "index_name": None},
    "Brazil": {"currency": "BRL", "index": "^BVSP", "index_name": "Bovespa"},
    "Argentina": {"currency": "ARS", "index": "^MERV", "index_name": "MERVAL"},
    "Nigeria": {"currency": "NGN", "index": None, "index_name": None},
    "South Africa": {"currency": "ZAR", "index": "^JN0U.JO", "index_name": "JSE"},
    "Australia": {"currency": "AUD", "index": "^AXJO", "index_name": "ASX 200"},
}

def get_exchange_rate(currency_code: str) -> dict:
    """Get exchange rate vs USD for a currency code."""
    if currency_code == "USD":
        # Skip currency display for USD since it's the base currency
        return None
    try:
        api_key = os.getenv("EXCHANGE_RATE_API_KEY")
        if not api_key:
            print("EXCHANGE_RATE_API_KEY not set in environment")
            return None
        r = requests.get(
            f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD",
            timeout=10
        )
        r.raise_for_status()
        data = r.json()
        if "conversion_rates" not in data:
            print(f"Invalid response from exchange rate API: {data}")
            return None
        rate = data["conversion_rates"].get(currency_code)
        if not rate:
            print(f"Currency code {currency_code} not found in API response")
            return None
        return {
            "rate": rate,
            "formatted": f"1 USD = {rate:,.2f} {currency_code}"
        }
    except requests.exceptions.RequestException as e:
        print(f"Exchange rate API request error: {e}")
        return None
    except Exception as e:
        print(f"Exchange rate API error: {e}")
        return None

def get_stock_fallback(ticker: str, index_name: str) -> dict:
    """Fallback method to get stock data from Yahoo Finance API directly."""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        r.raise_for_status()
        data = r.json()
        meta = data["chart"]["result"][0]["meta"]
        current = meta["regularMarketPrice"]
        prev = meta.get("previousClose") or meta.get("chartPreviousClose")
        if not prev:
            print(f"No previous close price found for {ticker}")
            return None
        change_pct = ((current - prev) / prev) * 100
        arrow = "↑" if change_pct >= 0 else "↓"
        return {
            "index_name": index_name,
            "value": f"{current:,.2f}",
            "change_pct": round(change_pct, 2),
            "formatted": f"{index_name}  {current:,.2f}  {arrow} {abs(change_pct):.2f}%",
            "direction": "up" if change_pct >= 0 else "down"
        }
    except Exception as e:
        print(f"Stock fallback failed for {ticker}: {e}")
        return None

def get_stock_index(ticker: str, index_name: str) -> dict:
    """Get today's stock index performance."""
    if not ticker:
        return None
    # Try yfinance first
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="2d")
        if hist.empty:
            print(f"No data returned for ticker {ticker}, trying fallback")
            return get_stock_fallback(ticker, index_name)
        if len(hist) < 2:
            # If only one day of data, try fallback
            print(f"Only one day of data for {ticker}, trying fallback")
            return get_stock_fallback(ticker, index_name)
        prev_close = hist['Close'].iloc[-2]
        current = hist['Close'].iloc[-1]
        change_pct = ((current - prev_close) / prev_close) * 100
        arrow = "↑" if change_pct >= 0 else "↓"
        return {
            "index_name": index_name,
            "value": f"{current:,.2f}",
            "change_pct": round(change_pct, 2),
            "formatted": f"{index_name} {current:,.2f} {arrow} {abs(change_pct):.2f}%",
            "direction": "up" if change_pct >= 0 else "down"
        }
    except Exception as e:
        print(f"Stock index error for {ticker}: {e}")
        import traceback
        print(traceback.format_exc())
        # Try fallback if yfinance fails
        print(f"Trying fallback API for {ticker}")
        return get_stock_fallback(ticker, index_name)

def get_economic_pulse(country: str) -> dict:
    """Get full economic pulse for a country."""
    meta = COUNTRY_ECONOMIC_DATA.get(country)
    if not meta:
        print(f"No economic data mapping found for country: {country}")
        return {"currency_code": None, "currency": None, "stock": None}
    
    print(f"Fetching economics for {country}: currency={meta['currency']}, index={meta['index']}")
    
    currency = None
    if meta["currency"]:
        currency = get_exchange_rate(meta["currency"])
        if currency:
            print(f"Currency data retrieved: {currency.get('formatted')}")
        else:
            print(f"Failed to retrieve currency data for {meta['currency']}")
    
    stock = None
    if meta["index"]:
        stock = get_stock_index(meta["index"], meta["index_name"])
        if stock:
            print(f"Stock data retrieved: {stock.get('formatted')}")
        else:
            print(f"Failed to retrieve stock data for {meta['index']}")
    
    result = {
        "currency_code": meta["currency"],
        "currency": currency,
        "stock": stock,
    }
    print(f"Economic pulse result for {country}: {result}")
    return result
