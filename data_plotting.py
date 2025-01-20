import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
import webbrowser


def create_and_save_plot(data, ticker, period, filename=None, style="default"):
    plt.style.use(style)
    plt.figure(figsize=(12, 12))

    if 'Date' not in data.columns:
        data.reset_index(inplace=True)

    # График цены и скользящей средней
    plt.subplot(4, 1, 1)
    plt.plot(data['Date'], data['Close'], label='Close Price')
    plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
    plt.title(f"{ticker} Stock Price & Moving Average")
    plt.legend()

    # График RSI
    plt.subplot(4, 1, 2)
    plt.plot(data['Date'], data['RSI'], label='RSI')
    plt.axhline(70, linestyle='--', color='red')
    plt.axhline(30, linestyle='--', color='green')
    plt.title('RSI Indicator')
    plt.legend()

    # График MACD
    plt.subplot(4, 1, 3)
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
    Вычисляет и выводит среднюю цену закрытия акций за весь период.
    :param data: DataFrame с историей цен акций.
    :return: Средняя цена.
    """
    if 'Close' in data:
        average_price = data['Close'].mean()
        print(f"Средняя цена закрытия акций за указанный период: {average_price:.2f}")
        return average_price
    else:
        print("Колонка 'Close' отсутствует в данных.")
        return None


def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если колебания цены закрытия акций превышают заданный порог.
    :param data: DataFrame с историей цен акций.
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


def create_interactive_plot(data, ticker, filename=None):
    """
    Создает интерактивный график с использованием Plotly.
    :param data: DataFrame с данными.
    :param ticker: Тикер акций.
    :param filename: Имя файла для сохранения графика (опционально).
    """
    fig = go.Figure()

    # График цены закрытия
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))

    # Скользящая средняя
    if 'Moving_Average' in data.columns:
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Moving_Average'], mode='lines', name='Moving Average'))

    # Настройка графика
    fig.update_layout(
        title=f"{ticker} Stock Prices",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
    )

    if filename:
        fig.write_html(filename)
        print(f"Интерактивный график сохранен как {filename}")
        webbrowser.open(filename)
    else:
        fig.show()


def create_bokeh_plot(data, ticker, filename=None):
    """
    Создает интерактивный график с использованием Bokeh.
    :param data: DataFrame с данными.
    :param ticker: Тикер акций.
    :param filename: Имя файла для сохранения графика (опционально).
    """
    source = ColumnDataSource(data)

    p = figure(title=f"{ticker} Stock Prices", x_axis_label='Date', y_axis_label='Price', x_axis_type='datetime')
    p.line(x='Date', y='Close', source=source, legend_label='Close Price', line_width=2)

    if 'Moving_Average' in data.columns:
        p.line(x='Date', y='Moving_Average', source=source, color='orange', legend_label='Moving Average', line_width=2)

    p.legend.title = "Legend"
    if filename:
        output_file(filename)
        print(f"Интерактивный график сохранен как {filename}")
        webbrowser.open(filename)
    else:
        show(p)