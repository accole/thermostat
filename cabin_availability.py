import datetime
import utils

UNIT_ID = "74932"
API_BASE_URL = f"https://bookings-mammothsierraonline.escapia.com/Unit/Availability/{UNIT_ID}"
STATUS_CODES = {
    "A": "Available",
    "O": "Checkout only (someone will checkin this afternoon)",
    "I": "Checkin only (someone will checkout this morning)",
    "U": "Unavailable"
}

def main():
    today = datetime.date.today().strftime('%m/%d/%Y')

    print(f"Checking for date: {today} ...")
    response = utils.get(API_BASE_URL, {'startDate': today,'endDate': today})

    if 'error' in response:
        print(response)
        return
    
    day_info = response.get('data')[0]
    availability_code = day_info.get('S')

    availability_description = STATUS_CODES.get(availability_code)
    print(f"Today is: {availability_description}")
    return

if __name__ == "__main__":
    main()
