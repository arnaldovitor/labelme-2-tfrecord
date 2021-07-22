import cv2
import numpy as np
import json
import os


def drawBox(boxes, image):
    for i in range(0, len(boxes)):
        cv2.rectangle(image, (boxes[i][2], boxes[i][3]), (boxes[i][4], boxes[i][5]), (255, 0, 0), 1)
    cv2.imshow("img", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def cvTest(imgPath, boxes):
    newBoxes = []
    
    imageToPredict = cv2.imread(imgPath, 3)
    print(imageToPredict.shape)
    
    y_ = imageToPredict.shape[0]
    x_ = imageToPredict.shape[1]

    targetSize = 640
    x_scale = targetSize / x_
    y_scale = targetSize / y_
    print(x_scale, y_scale)
    img = cv2.resize(imageToPredict, (targetSize, targetSize));
    cv2.imwrite(imgPath, img)
    print(img.shape)
    img = np.array(img);

    for box in boxes:
        x = int(np.round(box[0] * x_scale))
        y = int(np.round(box[1] * y_scale))
        xmax = int(np.round(box[2] * x_scale))
        ymax = int(np.round(box[3] * y_scale))
        newBoxes.append([x, y, xmax, ymax])
        
    #drawBox([[1, 0, x, y, xmax, ymax]], img)

    return newBoxes

def getBox(jsonPath):
    f = open(jsonPath, "r")
    y = json.loads(f.read())
    boxes = []
    for i in range(len(y['shapes'])):
        origLeft = float(y['shapes'][i]['points'][0][0])
        origTop = float(y['shapes'][i]['points'][0][1])
        origRight = float(y['shapes'][i]['points'][1][0])
        origBottom = float(y['shapes'][i]['points'][1][1])
        boxes.append([origLeft, origTop, origRight, origBottom])
        
    f.close()
    return boxes

def setBox(jsonPath, newBoxes):
    with open(jsonPath, "r") as jsonFile:
        y = json.load(jsonFile)

    for i in range(len(newBoxes)):
        y['shapes'][i]['points'][0][0] = newBoxes[i][0]
        y['shapes'][i]['points'][0][1] = newBoxes[i][1]
        y['shapes'][i]['points'][1][0] = newBoxes[i][2]
        y['shapes'][i]['points'][1][1] = newBoxes[i][3]
    y['imageHeight'] = 640
    y['imageWidth'] = 640

    with open(jsonPath, "w") as jsonFile:
        json.dump(y, jsonFile)

def resize(imgSetPath, jsonSetPath):
    imgSet = os.listdir(imgSetPath)
    jsonSet = os.listdir(jsonSetPath)
    imgSet.sort()
    jsonSet.sort()

    for i in range(len(imgSet)):
        boxes = getBox(jsonSetPath+jsonSet[i])
        newBoxes= cvTest(imgSetPath+imgSet[i] , boxes)
        setBox(jsonSetPath+jsonSet[i], newBoxes)
    

resize(r"/home/arnaldo/Documents/datasets/frames-with-guns/", r"/home/arnaldo/Documents/datasets/json-with-guns/")
