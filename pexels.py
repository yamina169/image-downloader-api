import requests
import os
import json

# API key
api_key = "enter your api key "
per_page = 200 # Number of images per page

# Queries and number of images to download for each query
queries = {"lifestyle": 1000, "sport": 1000, "war":1000}

for query, count in queries.items():
    # Create a directory for each query
    if not os.path.exists(query):
        os.makedirs(query)

    page = 1 # Initial page
    total_images = 0
    photos = []

    while total_images < count:
        # Build the URL for the API request
        url = f'https://api.pexels.com/v1/search?query={query}&per_page={per_page}&page={page}'
        headers = {
            "Authorization": api_key
        }
        r = requests.get(url, headers=headers)
        json_data = r.json()
        hits = json_data['photos']

        for image in hits:
            # Download the image
            name = image['id']
            img_url = image['src']['large']
            try:
                r = requests.get(img_url, stream=True)
                with open(os.path.join(query, str(name) + '.jpg'), 'wb') as f:
                    f.write(r.content)
                photos.append({"id": name, "query": query, "url": img_url})
                total_images += 1
            except Exception as e:
                print(f"Error downloading image {name}: {e}")
            if total_images >= count:
                break
        page += 1

    # Save the data for the downloaded images
    with open(os.path.join(query, 'photos.json'), 'w') as f:
        json.dump(photos, f, indent=4)

