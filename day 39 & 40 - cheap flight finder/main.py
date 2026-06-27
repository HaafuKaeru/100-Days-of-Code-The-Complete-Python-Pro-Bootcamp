from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch
from flight_data import FlightData


def main():
    data_manager = DataManager()
    sheet_data = data_manager.api_get(use_cache=True)
    print(sheet_data)

    flight_search = FlightSearch()
    search_result = flight_search.api_get(sheet_data, use_cache=True)
    print(search_result)

    flight_data = FlightData(search_result)
    data = flight_data.format_info()
    print(data)

    notification_manager = NotificationManager()
    message = (f"Flight Alert!\n"
               f"Only £{data['price']} to fly from {data['from']} to {data['to']} on {data['time']}")
    notification_manager.api_post(message)


if __name__ == '__main__':
    main()