import cv2
import time
import json
import base64
import requests
import pandas as pd
import numpy as np
from authKey import SECRET_KEY
import csv

cam = cv2.VideoCapture(1)
while True:

    _, img = cam.read()
    key = cv2.waitKey(1) & 0xff
    cv2.imshow("LicensePlate", img)
    if (key == ord('q')):

        cv2.destroyAllWindows()
        print("Captured successfully")
        cv2.imwrite("first.jpg", img)
        time.sleep(5)
        IMAGE_PATH = 'first.jpg'

        with open(IMAGE_PATH, 'rb') as image_file:
            img_base64 = base64.b64encode(image_file.read())

        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
        r = requests.post(url, data=img_base64)

        num_plate = (json.dumps(r.json(), indent=2))
        info = (list(num_plate.split("candidates")))
        # print(info)
        plate = info[1]
        plate = plate.split(',')[0:3]
        p = plate[1]
        p1 = p.split(":")
        number = p1[1]
        number = number.replace('"', '')
        number = number.lstrip()
        print(number)

        box = []
        t = []
        with open('Licensed Plate.csv', 'r+') as csvFile:
            reader = csv.reader(csvFile)
            for row in reader:
                if len(row) > 2:
                    box.append(row[1])
                    t.append(row)
            if number in box:
                name = t[box.index(number)][2]
                add = t[box.index(number)][3]
                print("-------------DATA FOUND IN DATABASE ---------------")
                print("Owner Name: {}".format(name))
                print("Vehicle Number: %s" % number)
                print("Address: {}".format(add))

            elif number not in box:
                reader = csv.writer(csvFile)

                reader.writerow([len(box), number, input("Enter name:"), input("Enter address:")])

    elif key == 27:
        break

cam.release()
cv2.destroyAllWindows()
