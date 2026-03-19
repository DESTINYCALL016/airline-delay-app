def total_flights(flights):
    return flights['flight_id'].nunique()


def on_time_percentage(flights):

    on_time = flights[flights['flight_status'] == "On Time") | (flights['delay_minutes'] <= 15)]['flight_id'].nunique()
    total = flights.shape[0]

    return round((on_time/total)*100,2)


def average_delay(flights):

    delayed = flights[flights['flight_status'] == "Delayed"]

    return round(delayed['delay_minutes'].mean(),2)


def cancellation_rate(flights):

    cancelled = flights[flights['flight_status']=="Cancelled"].shape[0]
    total = flights.shape[0]

    return round((cancelled/total)*100,2)


def diversion_rate(flights):

    diverted = flights[flights['flight_status']=="Diverted"].shape[0]
    total = flights.shape[0]

    return round((diverted/total)*100,2)