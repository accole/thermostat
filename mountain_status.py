import utils

MAMMOTH_RESORT_ID = "60"
API_BASE_URL = f"https://www.mtnpowder.com/feed"

def clean(list, filter_keys=['Id', 'Name', 'MountainAreaName', 'StatusId', 'Status'], sort_fn=lambda x: (x['MountainAreaName'], x['Name'])):
    filtered = utils.filter_object_keys(list, filter_keys)
    return sorted(filtered, key=sort_fn)

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
    
    timestamp = utils.now()
    
    utils.save(f"outputs/lifts-{timestamp}.json", clean(lifts))
    utils.save(f"outputs/trails-{timestamp}.json", clean(trails))

    return

if __name__ == "__main__":
    main()
