import config
import ccxt

def get_exchange():
    if hasattr(config, "APIKEY") and hasattr(config, "SECRET"):
        isauth = True
        args = {
            "apiKey": config.APIKEY,
            "secret": config.SECRET,
            "enableRateLimit": True,
        }
    else:
        isauth = False
        print("Warning: Using without authentication")
        args = {
            "enableRateLimit": True,
        }
    
    exchange = getattr(ccxt, config.EXCHANGE)(args)
    
    if isauth:
        exchange.checkRequiredCredentials()

    return exchange
