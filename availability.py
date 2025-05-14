import requests
import datetime
import json

UNIT_ID = "74932"
API_BASE_URL = f"https://bookings-mammothsierraonline.escapia.com/Unit/Availability/{UNIT_ID}"

# Status codes mapping based on user information
STATUS_CODES = {
    "A": "Available",
    "O": "Checkout only (someone checking in during the afternoon)",
    "I": "Checkin only (someone checking out during the morning)",
    "U": "Unavailable"
}

def check_date_availability_api(target_date_str=None):
    """
    Checks if a given date is available for the specified unit using the API.

    Args:
        target_date_str (str, optional): The date to check in 'YYYY-MM-DD' format

    Returns:
        str: A message indicating availability status or an error.
    """
    try:
        params = {
            'startDate': target_date_str,
            'endDate': target_date_str
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json'
        }

        response = requests.get(API_BASE_URL, params=params, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        api_data = response.json()

        if not api_data:
            return f"API returned no data for {target_date_str}. It might be outside the queryable range or an issue with the API."

        # Since we queried for a single day (startDate == endDate),
        # the first item in the list corresponds to our target_date
        day_info = api_data[0]

        status_code = day_info.get('S')
        
        return status_code

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err} - Response: {response.text if 'response' in locals() else 'N/A'}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Error connecting to API: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"API request timed out: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"An error occurred during the API request: {req_err}"
    except json.JSONDecodeError:
        return f"Failed to decode JSON response from API. Response was: {response.text if 'response' in locals() else 'N/A'}"
    except ValueError as val_err: # For strptime errors
        return f"Date formatting error: {val_err}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    today = datetime.date.today().strftime('%m/%d/%Y')

    print(f"Checking for date: {today} ...\n")
    availability_code = check_date_availability_api(today)

    availability_description = STATUS_CODES.get(availability_code)
    print(f"Today is {availability_description}")
