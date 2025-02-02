
import requests
import json
import time

# Get list of users from Discourse enpoint

users = []
users_info = []

i = 0
endpoint_users = "https://community.getstation.com/admin/users/list/active.json?order=created&show_emails=true"

while i < 100:
    i += 1

    payload = {
    "Api-Key": "???",
    "Api-Username": "julien"
    }

    parameters = {
    "page": i
    }

    paged_users = requests.get(endpoint_users, headers=payload, params=parameters).json()

    users.append(paged_users)

    print(len(paged_users))

    # Specific variables to extract
    for d in paged_users:
        info = {
            "userID": d['id'],
            "name": d['name'] or d['username'],
            "email": d['email'],
            "created": d['created_at'],
            "avatarURL": "https://community.getstation.com"
            + d['avatar_template'].replace("{size}", "240"),
        }

        users_info.append(info)

    nb_users_exported = len(paged_users)

    if nb_users_exported < 100:
        break

# Create a formatted string of the JSON object (for easy reading)
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Ensure the data is being extracted
print(len(users_info))


# Import data to Canny endpoint

endpoint_canny = "https://station.canny.io/api/v1/users/find_or_create"

payload2 = {
'apiKey': '???'
}

count = 0

for user in users_info:

    import_canny = requests.post(endpoint_canny, params=payload2, data=user)

    print(import_canny.content)

    count = count+1
    print(f'count {str(count)}')
    if count == 25:
        print("sleeping")
        time.sleep(2)
        count = 0
