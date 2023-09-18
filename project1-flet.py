import flet as ft
from google.cloud import storage
import json
import base64 
from diskcache import Cache
# Import the Secret Manager client library.
from google.cloud import secretmanager
import requests

#Secret Manager
project_id = "project1-398709"
secret_id = "access-photos"
version_id = 1
# Create the Secret Manager client.
#client = secretmanager.SecretManagerServiceClient()
# Build the resource name of the secret version.
#name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
# Access the secret version.
#response = client.access_secret_version(request={"name": name})
#payload = response.payload.data.decode("UTF-8")

#to cache images as workaround for not working properly
def fetch_image(url: str) -> str:
    """Fetch image for given URL and return as base64 string. With caching."""
    key = "image-" + base64.b64encode(url.encode("utf-8")).decode("utf-8")
    with Cache() as cache:
        data: Optional[bytes] = cache.get(key)  # type: ignore
        if not data:
            #logger.info("Download image from url: %s", url)
            r = requests.get(url)
            r.raise_for_status()
            data = r.content
            IMAGES_MAX_AGE_HOURS = 1
            cache.set(key, data, expire=IMAGES_MAX_AGE_HOURS * 3600)
    encoded = base64.b64encode(data).decode("utf-8")
    return encoded


#get list of images
def list_bucket_objects(bucket_name):
    list_of_urls = list()
    client = storage.Client.from_service_account_info(json.loads(payload))
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    # Iterate over the list of objects and process them as needed
    for blob in blobs:
        list_of_urls.append(f"https://storage.googleapis.com/{bucket_name}/{blob.name}")
    return list_of_urls



def main(page: ft.Page):
    t = ft.Text(value="DATS Project 1 Webpage. This is the demonstration webpage that I (Jeremy) created for Project 1 of the DATS Practicum.", color="black")
    page.controls.append(t)
    page.update()
    
    page.title = "Project 1"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()
    
    image_urls = ["https://storage.googleapis.com/images-bucket987/OIP.jpeg", "https://storage.googleapis.com/images-bucket987/h7BcHU.jpg"] #deleted this temporarily to make the program simpler#list_bucket_objects('images-bucket987')

    images = ft.Row(expand=1, wrap=False, scroll="always")

    page.add(images)

    for i in image_urls:
        print(i)
        images.controls.append(
            ft.Image(src_base64=fetch_image(i),
                width=500,
                height=500,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()
    

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port = 8080)