import vk_api
import vk
from PIL import Image, ImageDraw, ImageFont
import requests
import random
import words
import time
import os

token = 'group token'
group_id = 206170695
vks = vk_api.VkApi(token)
owner_id = -206170695     # owner id = -group_id
album_id = 280291786

while True:
    ph_num = random.randrange(1, 70+1)
    first_word = random.choice(words.words)
    second_word = random.choice(words.words)
    output = first_word + ' ' + second_word

    im = Image.open(f"photo/{ph_num}.jpg")
    d = ImageDraw.Draw(im)
    offset = 2
    shadowColor = 'black'
    font = ImageFont.truetype("impact.ttf", 45)
    imWidth, imHeight = im.size

    text = output

    x = imWidth - imWidth/1.5
    y = imHeight - imHeight/5

    for off in range(offset):
        d.text((x-off, y), str(text), font=font, fill=shadowColor)
        d.text((x+off, y), str(text), font=font, fill=shadowColor)
        d.text((x, y+off), str(text), font=font, fill=shadowColor)
        d.text((x, y-off), str(text), font=font, fill=shadowColor)
        d.text((x-off, y+off), str(text), font=font, fill=shadowColor)
        d.text((x+off, y+off), str(text), font=font, fill=shadowColor)
        d.text((x-off, y-off), str(text), font=font, fill=shadowColor)
        d.text((x+off, y-off), str(text), font=font, fill=shadowColor)
    d.text((x, y), str(text), font=font, fill="#fff")
    im.save(f'photo/{ph_num}_edited.jpg')

    stoken = 'service token for group'
    filename = f'photo/{ph_num}_edited.jpg'

    api = vk.API(vk.Session(access_token=stoken), v='5.130')
    upload_url = api.photos.getWallUploadServer(group_id=group_id)['upload_url']
    resp = requests.post(upload_url, files={
        'file': open(filename, 'rb')}).json()
    s = api.photos.saveWallPhoto(group_id=group_id, server=resp['server'], photo=resp['photo'], hash=resp['hash'])
    api.wall.post(owner_id=-group_id, message="", attachments=f"photo{s[0]['owner_id']}_{s[0]['id']}")
    os.remove(f'photo/{ph_num}_edited.jpg')
    print(f'Пост с картинкой {ph_num} и текстом {output} опубликован')
    time.sleep(3600)
