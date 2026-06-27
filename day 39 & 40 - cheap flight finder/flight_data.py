# This class is responsible for structuring the flight data.
class FlightData:

    def __init__(self, flight_search_results: list[dict]):
        self.flight_search_results = flight_search_results

    def format_info(self) -> list:
        result = []
        for flight in self.flight_search_results:
            formatted_data = {
                "price": flight["price"],
                "from": flight["flights"][0]["departure_airport"]["id"],
                "to": flight["flights"][0]["arrival_airport"]["id"],
                "time": flight["flights"][0]["departure_airport"]["time"],
            }
            result.append(formatted_data)
        return result