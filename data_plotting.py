import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker, period, filename=None, style="default"):
    plt.style.use(style)
    plt.figure(figsize=(12, 12))

    if 'Date' not in data.columns:
        data.reset_index(inplace=True)

    # График цены и скользящей средней
    plt.subplot(3, 1, 1)
    plt.plot(data['Date'], data['Close'], label='Close Price')
    plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
    plt.title(f"{ticker} Stock Price & Moving Average")
    plt.legend()

    # График RSI
    plt.subplot(3, 1, 2)
    plt.plot(data['Date'], data['RSI'], label='RSI')
    plt.axhline(70, linestyle='--', color='red')
    plt.axhline(30, linestyle='--', color='green')
    plt.title('RSI Indicator')
    plt.legend()

    # График MACD
    plt.subplot(3, 1, 3)
    plt.plot(data['Date'], data['MACD'], label='MACD')
    plt.plot(data['Date'], data['MACD_Signal'], label='MACD Signal')
    plt.title('MACD Indicator')
    plt.legend()

    # График стандартного отклонения
    plt.subplot(4, 1, 4)
    plt.plot(data['Date'], data['Standard_Deviation'], label='Standard Deviation', color='purple')
    plt.title('Standard Deviation of Closing Price')
    plt.legend()

    plt.tight_layout()
    if filename:
        plt.savefig(filename)
        print(f"График сохранен как {filename}")
    else:
        plt.show()


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
