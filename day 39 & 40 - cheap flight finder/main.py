from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch
from flight_data import FlightData


def main():
    data_manager = DataManager()
    sheet_data = data_manager.get_required_flights(use_cache=True)
    print(sheet_data)
    customer_data = data_manager.get_customer_emails(use_cache=True)
    print(customer_data)

    flight_search = FlightSearch()
    search_result = flight_search.api_get(sheet_data, use_cache=False)
    print(search_result)

    flight_data = FlightData(search_result)
    flights_list = flight_data.format_info()
    print(flights_list)

    notification_manager = NotificationManager()
    for flight in flights_list:
        message = (f"Flight Alert!\n"
                   f"Only GBP{flight['price']} to fly from {flight['from']} to {flight['to']} on {flight['time']}")
        notification_manager.send_sms(message)
        notification_manager.send_emails(customer_data, message)


if __name__ == '__main__':
    main()