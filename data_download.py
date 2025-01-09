import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def export_data_to_csv(data, filename):
    data.to_csv(filename, index=False)
    print(f"Данные сохранены в файл: {filename}")