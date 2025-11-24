# utils/imgur_upload.py
import requests
import base64

def upload_to_imgur(uploaded_file):
    """Upload image to Imgur and return public link"""
    url = "https://api.imgur.com/3/image"
    try:
        # Read bytes from uploaded file
        bytes_data = uploaded_file.read()
        payload = base64.b64encode(bytes_data)
        headers = {'Authorization': 'Client-ID 546c25a59c58ad7'}
        r = requests.post(url, headers=headers, data=payload)
        if r.status_code == 200:
            return r.json()['data']['link']
        else:
            return ""
    except Exception as e:
        return ""