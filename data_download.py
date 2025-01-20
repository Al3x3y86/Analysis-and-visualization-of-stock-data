import yfinance as yf


def fetch_stock_data(ticker, period=None, start_date=None, end_date=None):
    stock = yf.Ticker(ticker)

    # Если указаны конкретные даты, использовать их
    if start_date and end_date:
        data = stock.history(start=start_date, end=end_date)
    else:
        # Использовать стандартный период, если даты не указаны
        data = stock.history(period=period)

    data.reset_index(inplace=True)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    return data


def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = short_ema - long_ema
    data['MACD_Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data


def export_data_to_csv(data, filename):
    data.to_csv(filename, index=False)
    print(f"Данные сохранены в файл: {filename}")


def add_technical_indicators(data):
    data = calculate_rsi(data)
    data = calculate_macd(data)
    data = calculate_standard_deviation(data)
    return data


def calculate_standard_deviation(data):
    """
    Вычисляет стандартное отклонение цены закрытия акций.
    :param data: DataFrame с колонкой 'Close'.
    :return: DataFrame с добавленной колонкой 'Standard_Deviation'.
    """
    if 'Close' in data:
        data['Standard_Deviation'] = data['Close'].rolling(window=10).std()
    else:
        print("Колонка 'Close' отсутствует в данных.")
    return data