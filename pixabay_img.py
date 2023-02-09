# www.Pixabay.com est un site web de partage d'images diffusées en licence libre 
import requests
import os
import json
api_key = "your api key "
per_page = 200  # Number of images per page
page = 1  # Initial page
queries = {"cars": 500, "dogs": 500, "flowers": 500}

for query, count in queries.items():
    if not os.path.exists(query):
        os.makedirs(query)

    total_images = 0
    photos = []

    while total_images < count:
        url = f'https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&pretty=true&per_page={per_page}&page={page}'
        r = requests.get(url)
        json_data = r.json()
        hits = json_data['hits']

        for image in hits:
            name = image['id']
            img_url = image['largeImageURL']
            r = requests.get(img_url, stream=True)
            with open(os.path.join(query, str(name) + '.jpg'), 'wb') as f:
                f.write(r.content)

            photos.append({"id": name, "query": query, "name": image['tags'], "url": img_url})

            total_images += 1

            if total_images >= count:
                break
        page += 1

    with open(os.path.join(query, 'photos.json'), 'w') as f:
        json.dump(photos, f, indent=4)


