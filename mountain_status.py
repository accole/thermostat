import utils
import datetime

MAMMOTH_RESORT_ID = "60"
API_BASE_URL = f"https://www.mtnpowder.com/feed"

def clean(list, filter_keys=['Id', 'Name', 'MountainAreaName', 'StatusEnglish'], sort_fn=lambda x: (x['MountainAreaName'], x['Name'])):
    filtered = utils.filter_object_keys(list, filter_keys)
    return sorted(filtered, key=sort_fn)

# def create_status_map(list):
#     map = {}
#     for item in list:
#         status_id = item.get("StatusId")
#         status_description = item.get("StatusEnglish")
#         if status_id not in map:
#             map[status_id] = status_description
#     return map

def main():
    print("Checking lift and trail status ...")
    response = utils.get(API_BASE_URL, {'resortId': MAMMOTH_RESORT_ID})

    if 'error' in response:
        print(response)
        return
    
    data = response.get('data')
    mountain_areas = data.get('MountainAreas')

    lifts = []
    trails = []

    for area in mountain_areas:
        if area.get('OpenTrailsCount') > 0:
            lifts.extend(area.get('Lifts'))
            trails.extend(area.get('Trails'))

    output = {
        'lifts': clean(lifts),
        'trails': clean(trails)
    }

    today = datetime.date.today().strftime('%Y-%m-%d')
    utils.save(f"outputs/{today}.json", output)

    # status = create_status_map(lifts) | create_status_map(trails)
    # utils.save(f"outputs/status-{today}.json", utils.alphabetize(status))

    return

if __name__ == "__main__":
    main()
