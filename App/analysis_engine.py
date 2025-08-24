# File: analysis_engine.py
import pandas as pd
from .data_paths import (
    PRIMARY_DATA_FILE,
    CASCADING_DELAYS_FILE
)

def get_airport_traffic_analysis(airport_code="default"):
    """Calculates the busiest hours and best hours directly from the detailed flight data."""
    try:
        df = pd.read_excel(PRIMARY_DATA_FILE)
        summary_by_hour = df.groupby('Hour_of_Day').agg(
            Flight_Count=('Flight_ID', 'count'),
            Average_Delay_Minutes=('Arrival_Delay_Minutes', 'mean')
        ).reset_index()
        busiest_hours = summary_by_hour.nlargest(5, 'Flight_Count')
        best_hours = summary_by_hour.nsmallest(5, 'Average_Delay_Minutes')
        return {
            "airport": airport_code,
            "busiest_hours_by_flight_count": busiest_hours.to_dict('records'),
            "best_hours_by_lowest_delay": best_hours.to_dict('records')
        }
    except FileNotFoundError:
        return {"error": f"Data file not found: {PRIMARY_DATA_FILE}"}

def predict_delay(flight_details):
    """Predicts the average delay for a given hour directly from the detailed data."""
    try:
        hour = flight_details.get('hour')
        df = pd.read_excel(PRIMARY_DATA_FILE)
        hourly_data = df[df['Hour_of_Day'] == hour]
        if not hourly_data.empty:
            avg_delay = hourly_data['Arrival_Delay_Minutes'].mean()
            return {"message": f"Based on historical data, the predicted average delay for the {hour}:00 hour is {round(avg_delay)} minutes."}
        else:
            return {"error": f"No historical data found for hour {hour}."}
    except FileNotFoundError:
        return {"error": f"Data file not found: {PRIMARY_DATA_FILE}"}

# --- NEW FUNCTION: Runway Analysis ---
def get_runway_analysis(airport_code="default"):
    """Analyzes runway usage from the detailed data file."""
    try:
        df = pd.read_excel(PRIMARY_DATA_FILE)
        unique_runways = df['Runway'].unique()
        runway_count = len(unique_runways)
        busiest_runway = df['Runway'].mode()[0] # .mode()[0] gets the most frequent value
        return {
            "airport": airport_code,
            "runway_count": runway_count,
            "runway_names": list(unique_runways),
            "busiest_runway_by_traffic": busiest_runway
        }
    except FileNotFoundError:
        return {"error": f"Data file not found: {PRIMARY_DATA_FILE}"}

# --- NEW FUNCTION: Delay Reason Analysis ---
def get_delay_reason_analysis(delay_reason=None):
    """Analyzes delay reasons from the detailed data file."""
    try:
        df = pd.read_excel(PRIMARY_DATA_FILE)
        if delay_reason:
            # Analyze a specific delay reason
            reason_data = df[df['Delay_Reason'].str.lower() == delay_reason.lower()]
            if not reason_data.empty:
                avg_delay = reason_data['Arrival_Delay_Minutes'].mean()
                return {
                    "delay_reason": delay_reason,
                    "average_delay_minutes": round(avg_delay),
                    "occurrence_count": len(reason_data)
                }
            else:
                return {"error": f"No data found for delay reason: '{delay_reason}'"}
        else:
            # Provide a summary of all delay reasons
            top_reasons = df['Delay_Reason'].value_counts().nlargest(5)
            return {
                "summary": "Top 5 most common delay reasons",
                "top_delay_reasons": top_reasons.to_dict()
            }
    except FileNotFoundError:
        return {"error": f"Data file not found: {PRIMARY_DATA_FILE}"}

def find_high_impact_flights(airport_code="default"):
    """Reads the pre-analyzed data to find flights causing cascading delays."""
    try:
        df = pd.read_excel(CASCADING_DELAYS_FILE)
        impactful_flights = df[df['Causes_Cascade'] == True]
        top_impactful = impactful_flights.nlargest(10, 'Arrival_Delay_Minutes')
        return {
            "airport": airport_code,
            "high_impact_flights": top_impactful[['Flight_ID', 'Arrival_Delay_Minutes']].to_dict('records')
        }
    except FileNotFoundError:
        return {"error": "Cascading delays file not found."}