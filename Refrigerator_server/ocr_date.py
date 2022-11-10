import cv2
import requests

appkey = "88ba82fedc172fa6718efbf18cb0eac2"

def kakao_ocr(image, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()


    return requests.post(API_URL, headers=headers, files={"image": data})

# 88ba82fedc172fa6718efbf18cb0eac2


def receiveImg(img, appkey):
    output = kakao_ocr(img, appkey).json()
    i = 0
    words = ""
    while True:
        try:
            words = words + str(output['result'][i]['recognition_words'])[2:]
            print(words)
            words = words[:-2]
            i = i+1
        except:
            break
    return words
