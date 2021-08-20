import os
import glob
import pandas as pd
import json
import pickle
import random

def json_to_csv():
    
    path_to_json= '/home/arnaldo/Documents/datasets/gun-detection/with-resize-512/json-with-guns/'
    path_to_jpeg = '/home/arnaldo/Documents/datasets/gun-detection/with-resize/frames-with-guns/'

    
    fjpeg = os.listdir(r"/home/arnaldo/Documents/datasets/gun-detection/with-resize-512/frames-with-guns/")
    json_files = os.listdir(r"/home/arnaldo/Documents/datasets/gun-detection/with-resize-512/json-with-guns/")
    fjpeg.sort()
    json_files.sort()

#    zipado = list(zip(fjpeg, json_files))

#    random.shuffle(zipado)

#    fjpeg, json_files = zip(*zipado)
    train_size = int(len(json_files)*0.5)
    train = json_files[0:train_size]
    test = json_files[train_size:len(json_files)]
                      
    print(len(train)+len(test))
    n=0
    csv_list_train = []
    csv_list_test = []
    labels=[]
    for j in train:
        print(path_to_json+j)
        data_file=open(path_to_json+j)   
        data = json.load(data_file)
        width,height=data['imageWidth'],data['imageHeight']
        for i in range(len(data["shapes"])):
                name="gun"
                labels.append(name)
                xmin=data['shapes'][i]['points'][0][0]
                ymin=data['shapes'][i]['points'][0][1]
                xmax=data['shapes'][i]['points'][1][0]
                ymax=data['shapes'][i]['points'][1][1]

                if xmin==0:
                    xmin+=1
                elif ymin==0:
                    ymin+=1
                elif xmax==0:
                    xmax+=1
                elif ymax==0:
                    ymax+=1

                nxmin = min(xmin, xmax)
                nxmax = max(xmin, xmax)
                nymin = min(ymin, ymax)
                nymax = max(ymin, ymax)
                                
                value = (fjpeg[n],
                         width,
                         height,
                         name,
                         nxmin,
                         nymin,
                         nxmax,
                         nymax
                         )
                csv_list_train.append(value)
        n=n+1
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    csv_train_df = pd.DataFrame(csv_list_train, columns=column_name)

    for j in test:
        print(path_to_json+j)
        data_file=open(path_to_json+j)   
        data = json.load(data_file)
        width,height=data['imageWidth'],data['imageHeight']
        for i in range(len(data["shapes"])):
                name="gun"
                labels.append(name)
                xmin=data['shapes'][i]['points'][0][0]
                ymin=data['shapes'][i]['points'][0][1]
                xmax=data['shapes'][i]['points'][1][0]
                ymax=data['shapes'][i]['points'][1][1]

                
                if xmin==0:
                    xmin+=1
                elif ymin==0:
                    ymin+=1
                elif xmax==0:
                    xmax+=1
                elif ymax==0:
                    ymax+=1

                nxmin = min(xmin, xmax)
                nxmax = max(xmin, xmax)
                nymin = min(ymin, ymax)
                nymax = max(ymin, ymax)
                                
                value = (fjpeg[n],
                         width,
                         height,
                         name,
                         nxmin,
                         nymin,
                         nxmax,
                         nymax
                         )
                csv_list_test.append(value)
        n=n+1
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    csv_test_df = pd.DataFrame(csv_list_test, columns=column_name)
    
    
    labels_train=list(set(labels))
    with open("train_labels.txt", "wb") as fp:   #Pickling
        pickle.dump(labels_train, fp)

        
    return csv_train_df, csv_test_df

def main():
    csv_train_df, csv_test_df = json_to_csv()
    csv_train_df.to_csv('/home/arnaldo/Documents/datasets/train_labels.csv', index=None)
    csv_test_df.to_csv('/home/arnaldo/Documents/datasets/test_labels.csv', index=None)

    print('Successfully converted json to csv.')

main()
