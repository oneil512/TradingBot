import urllib2
import numpy as np
import json
from xml.dom.minidom import parse, parseString


def getPriceByDay():

    response = urllib2.urlopen("https://blockchain.info/charts/market-price?timespan=all&format=json")
    html = response.read()

    data = json.loads(html)

    dataFile = open("data.txt","w+")

    for instance in data['values']:
        price = instance['y']
        dataFile.write(str(price) + ",")
        
def shapeData(higher, lower):
    data = zip(higher, lower)
    random.shuffle(data)

    train_data = []
    train_class = []

    for record in data:
        F, T = record
        F_data, F_class = F
        T_data, T_class = T

        train_data.append(F_data)
        train_data.append(T_data)
        train_class.append([F_class])
        train_class.append([T_class])

    train_class = to_categorical(train_class)

    print train_data.shape
    print train_class.shape
    
    return (train_data, train_class)


def getPriceAndVolumeByTime():
    price = []
    volume = []
    weightedPrice = []

    with open("priceandvolume.txt","r") as f:
        for line in f:
            parsedData = line.split()

            if '\xe2\x80\x94' in parsedData:
                continue

            if len(parsedData) < 8:
                continue

            price.append(float(parsedData[4]))
            volume.append(float(parsedData[6]))
            weightedPrice.append(float(parsedData[7]))

    return (price, volume, weightedPrice)


def partitionData(n, price, volume):
    higher = []
    lower = []

    length = len(price)
    count = n - 1

    while(count < length - 1):

        priceInstance = price[count - (n - 1) : count + 1]
        volumeInstance = volume[count - (n - 1) : count + 1]

        instance = priceInstance + volumeInstance

        if(price[count + 1] > price[count]):
            higher.append((instance, 1))

        else:
            lower.append((instance , 0))

        count += 1


    return (higher, lower)


