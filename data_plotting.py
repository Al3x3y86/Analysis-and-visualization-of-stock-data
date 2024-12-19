import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None):
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")


def calculate_and_display_average_price(data):
    """
     Функция вычисляет и выводит среднюю цену закрытия акций за весь период.
    :param data: DataFrame с историей цен акций.
    """
    if 'Close' in data:
        average_price = data['Close'].mean()
        print(f"Средняя цена закрытия акций за указанный период: {average_price:.2f}")
    else:
        print("Колонка 'Close' отсутствует в данных.")


def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если колебания цены закрытия акций превышают заданный порог.
    :param data: DataFrame с историей цен акций.
                 Ожидается наличие колонки 'Close' с ценами закрытия.
    :param threshold: Порог колебания в процентах (например, 5 для 5%).
    :return: None
    """
    if 'Close' in data:
        max_price = data['Close'].max()
        min_price = data['Close'].min()
        fluctuation = ((max_price - min_price) / min_price) * 100

        if fluctuation > threshold:
            print(f"⚠️ Сильные колебания! Цена закрытия изменилась на {fluctuation:.2f}%, что превышает порог {threshold}%.")
        else:
            print(f"Цена закрытия стабильна. Колебания составляют {fluctuation:.2f}%, что ниже порога {threshold}%.")
    else:
        print("Колонка 'Close' отсутствует в данных.")
