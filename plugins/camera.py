from slackbot.bot import respond_to

import os
import time
from datetime import datetime

import re
import requests

import json
import base64

import picamera

import slackbot_settings

image_path = 'image.jpg'


def capture_image():
    camera = picamera.PiCamera()

    try:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # camera warm-up time
        time.sleep(2)
        camera.capture(image_path)
    except Exception as other:
        message.send(''.join(other.args))
        return
    finally:
        camera.close()


def get_predictions():
    img = open(image_path, 'rb')
    img_byte = img.read()
    img_content = base64.b64encode(img_byte).decode("utf-8")

    url = 'https://vision.googleapis.com/v1/images:annotate?key='
    google_api_url = url + slackbot_settings.GOOGLE_API_KEY

    google_req_body = json.dumps({
        'requests': [{
            'image': {
                'content': img_content
            },
            'features': [{
                'type': 'LABEL_DETECTION',
                'maxResults': 10,
            }]
        }]
    })

    res = requests.post(google_api_url, data=google_req_body)
    res_json = res.json()

    labels = res_json['responses'][0]['labelAnnotations']

    predictions = []
    for value in labels:
        label = value['description']
        predictions.append(label)

    return predictions


def has_person_in_image(predictions):
    human_characteristics = [
        'Hair', 'Arm', 'Chin', 'Hairstyle', 'Eyewear', 'Shoulder',
        'Glasses', 'Forehead', 'T-shirt', 'Jaw', 'Hair',
        'Finger', 'Elbow', 'Ear', 'Human leg', 'Human body'
    ]

    for characteristic in human_characteristics:
        if characteristic in predictions:
            return True

    return False


@respond_to('capture', re.IGNORECASE)
def capture(message):
    message.send('...')

    capture_image()
    predictions = get_predictions()
    message.send('Predictions: ' + ', '.join(predictions))

    retry_count = 0

    while retry_count < 3:
        if not has_person_in_image(predictions):
            break

        message.send('retry...')
        time.sleep(3)

        capture_image()
        predictions = get_predictions()
        message.send('Predictions: ' + ', '.join(predictions))

        retry_count += 1

    slackapi_params = {
        'token': slackbot_settings.API_TOKEN,
        'channels': slackbot_settings.IMAGE_SENT_TO,
        'title': datetime(*time.localtime(os.path.getctime(image_path))[:6]),
    }

    try:
        requests.post(
            'https://slack.com/api/files.upload',
            data=slackapi_params,
            files={
                'file': open(image_path, 'rb')
            }
        )

    except Exception as other:
        message.send(''.join(other.args))
        return
