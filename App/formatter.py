# File: formatter.py

def format_time(hour):
    """Converts 24-hour format to 12-hour AM/PM format."""
    if hour == 0:
        return "12 AM"
    if hour == 12:
        return "12 PM"
    if hour < 12:
        return f"{hour} AM"
    return f"{hour - 12} PM"

def format_traffic_analysis(data):
    """Formats the traffic analysis data into two HTML tables."""
    busiest_html = "<h5> busiest_hours_by_flight_count</h5><ul class='list-disc pl-5 space-y-1'>"
    for item in data.get('busiest_hours_by_flight_count', []):
        hour = format_time(item['Hour_of_Day'])
        flights = item['Flight_Count']
        busiest_html += f"<li><strong>{hour}:</strong> {flights} flights</li>"
    busiest_html += "</ul>"

    best_html = "<h5> best_hours_by_lowest_delay</h5><ul class='list-disc pl-5 space-y-1'>"
    for item in data.get('best_hours_by_lowest_delay', []):
        hour = format_time(item['Hour_of_Day'])
        delay = round(item['Average_Delay_Minutes'])
        best_html += f"<li><strong>{hour}:</strong> {delay} min average delay</li>"
    best_html += "</ul>"

    return f"<div class='space-y-3'>{busiest_html}{best_html}</div>"

def format_runway_analysis(data):
    """Formats the runway analysis data into a simple paragraph."""
    count = data.get('runway_count', 0)
    names = ", ".join(data.get('runway_names', []))
    busiest = data.get('busiest_runway_by_traffic', 'N/A')
    return f"<p>The analysis shows there are <strong>{count} runways</strong> ({names}). The most frequently used runway is <strong>{busiest}</strong>.</p>"

def format_delay_reason_analysis(data):
    """Formats the delay reason data."""
    if "summary" in data:
        reasons_html = "<ul class='list-disc pl-5 space-y-1'>"
        for reason, count in data.get('top_delay_reasons', {}).items():
            reasons_html += f"<li><strong>{reason}:</strong> {count} occurrences</li>"
        reasons_html += "</ul>"
        return f"<p>Here are the top 5 most common reasons for delays:</p>{reasons_html}"
    else:
        reason = data.get('delay_reason', 'N/A')
        delay = data.get('average_delay_minutes', 0)
        count = data.get('occurrence_count', 0)
        return f"<p>For delays caused by <strong>{reason}</strong>, the average delay is <strong>{delay} minutes</strong>, based on {count} recorded incidents.</p>"

def format_predict_delay(data):
    """Formats the predicted delay message."""
    return f"<p>{data.get('message', 'No prediction available.')}</p>"

def format_high_impact_flights(data):
    """Formats the high-impact flights into a list."""
    flights_html = "<h5>Top High-Impact Flights by Delay</h5><ul class='list-disc pl-5 space-y-1'>"
    for flight in data.get('high_impact_flights', []):
        flight_id = flight['Flight_ID']
        delay = flight['Arrival_Delay_Minutes']
        flights_html += f"<li><strong>{flight_id}:</strong> {delay} min delay</li>"
    flights_html += "</ul>"
    return flights_html

def format_response(function_name, data):
    """Dispatcher function to call the correct formatter."""
    if function_name == "get_airport_traffic_analysis":
        return format_traffic_analysis(data)
    if function_name == "get_runway_analysis":
        return format_runway_analysis(data)
    if function_name == "get_delay_reason_analysis":
        return format_delay_reason_analysis(data)
    if function_name == "predict_delay":
        return format_predict_delay(data)
    if function_name == "find_high_impact_flights":
        return format_high_impact_flights(data)
    
    # Fallback for any other data
    return f"<pre class='bg-gray-800 text-white p-3 rounded-md text-sm whitespace-pre-wrap'><code>{json.dumps(data, indent=2)}</code></pre>"

