from data_manager import DataManager
from notification_manager import NotificationManager
from flight_search import FlightSearch


def main():
    data_manager = DataManager()
    sheet_data = data_manager.api_get(use_cache=True)
    print(sheet_data)

    flight_search = FlightSearch()
    flight_search.get_dates()

    notification_manager = NotificationManager()
    message = "This is an automated message"
    # notification_manager.api_post(message)


if __name__ == '__main__':
    main()