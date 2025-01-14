import data_download as dd
import data_plotting as dplt

def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): »")
    use_custom_dates = input("Хотите указать начальную и конечную даты? (да/нет): ").strip().lower()

    if use_custom_dates == 'да':
        start_date = input("Введите дату начала в формате ГГГГ-ММ-ДД: ")
        end_date = input("Введите дату окончания в формате ГГГГ-ММ-ДД: ")
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date, end_date=end_date)
    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        stock_data = dd.fetch_stock_data(ticker, period=period)

    # Добавление технических индикаторов
    stock_data = dd.add_moving_average(stock_data)
    stock_data = dd.add_technical_indicators(stock_data)

    # Уведомления и вывод данных
    threshold = float(input("Введите порог колебания в процентах (например, 5 для 5%): "))
    dplt.notify_if_strong_fluctuations(stock_data, threshold)
    dplt.calculate_and_display_average_price(stock_data)

    # Построение графика
    if use_custom_dates == 'да':
        dplt.create_and_save_plot(stock_data, ticker, f"{start_date} to {end_date}")
    else:
        dplt.create_and_save_plot(stock_data, ticker, period)

    # Экспорт данных в CSV
    if use_custom_dates == 'да':
        dd.export_data_to_csv(stock_data, f"{ticker}_{start_date}_to_{end_date}_stock_data.csv")
    else:
        dd.export_data_to_csv(stock_data, f"{ticker}_{period}_stock_data.csv")

if __name__ == "__main__":
    main()