# This class is responsible for structuring the flight data.
class FlightData:

    def __init__(self, flight_search_results: dict):
        self.flight_search_results = flight_search_results

    def format_info(self):
        formatted_data = {
            "price": self.flight_search_results["price"],
            "from": self.flight_search_results["flights"][0]["departure_airport"]["id"],
            "to": self.flight_search_results["flights"][0]["arrival_airport"]["id"],
            "time": self.flight_search_results["flights"][0]["departure_airport"]["time"],
        }
        return formatted_data