from scapy.all import *
import pandas as pd
import numpy as np
from network import Network
from channel import Channel
import datetime

wifiData = pd.read_csv("networks.csv", sep='\t')

#df = pd.read_csv("testing-02.csv", sep=',', nrows = 1)
#print(df.columns)

#df2 = pd.read_csv("testing-02.csv", sep=',', skiprows = 4)

#print(df)
#print(df2)
    
def findChannels(wifiData):
    availableChannels = [] 
    for index, row in wifiData.iterrows():
    #p = sub.Popen(['airodump-ng','--bssid', row["BSSID"], '--essid', row["SSID"], '-c', str(row["Channel"]), '-w', "testing", '--output-format', 'csv', 'wlan0mon'])
        channel = row["Channel"]
        exists = channel in availableChannels
        if (not exists):
            availableChannels.append(channel)
    return availableChannels
        
    
def prepareChannels(availableChannels):
    channels = initiateChannels(availableChannels)
    

    for i in range(1, len(wifiData)):
        #len(wifiData)
        #fileName = "testing-02.csv"
        fileName = "network-"
        if (i < 10):
            fileName += "0"
        fileName += str(i) + ".csv"

        # df = pd.read_csv("testing-02.csv", sep=',', nrows = 1)
        df = pd.read_csv(fileName, sep=',', nrows = 1)
        #print(fileName)
        channel = df[" channel"].iloc[0]
        #print(channel == " Power")
        power = df[" Power"].iloc[0]
        #print(power)

        #stations = pd.read_csv(fileName, sep=',', skiprows = 4)
        
        if (channel != " Power"):
            #print("Channel is ", channel)
            stations = pd.read_csv(fileName, sep=',', skiprows = 4)
            network = Network(channel)
            if (len(stations) > 0):
            	# packets per station
                for index, row in stations.iterrows():
                    packets = row[" # packets"]
                    network.addStation(packets)
                    #print ("packets per station is ", packets)

            channels[getIndex(availableChannels, channel)].addNetwork(network)

            #print("packets for channel " + str(channel) + " is ", numberOfPacketsPerChannel[int(channel) - 1])
            #print("packets for channel " + str(channel) + " is ", numberOfStationsPerChannel[int(channel) - 1])
    # for () => fun gia c1 = numberOfPacketsPerChannel[1]*0.7 + numberOfStationsPerChannel[1]*0.3 ( numberpwrperchannel[1]*0.1) => 23.2 
    #return numberOfPacketsPerChannel, numberOfStationsPerChannel, numberOfNetworksPerChannel
    #for i in range(0, len(availableChannels)):
     #    print("Packets for channel " + str(channels[i].getId()) + " is ", channels[i].getTotalData())
     #    print("Stations for channel " + str(channels[i].getId()) + " is ", channels[i].getTotalStations())
     #    print("Networks for channel " + str(channels[i].getId()) + " is ", channels[i].getTotalNetworks())

    return channels

def getIndex(availableChannels, channel):
    for i in range(0, len(availableChannels)):
        if (channel == availableChannels[i]):
            return i

def initiateChannels(availableChannels):
    channels = []
    for i in range(0, len(availableChannels)):
        channels.append(Channel(availableChannels[i]))
    return channels

def getPercentages(sets):
    total = 0
    percentages = []
    for i in range(0, len(sets)):
        total += sets[i]
    
    for i in range(0, len(sets)):
        percentages.append(sets[i]/total)
    
    return percentages

def getAllIDs(channels):
    channelIDs = []
    for i in range(0, len(channels)):
        channelIDs.append(channels[i].getId())
    
    return channelIDs

def getAllPackets(channels):
    channelPackets = []
    for i in range(0, len(channels)):
        channelPackets.append(channels[i].getTotalData())
    
    return channelPackets

def getAllStations(channels):
    channelStations = []
    for i in range(0, len(channels)):
        channelStations.append(channels[i].getTotalStations())
    
    return channelStations

def getAllNetworks(channels):
    channelNetworks = []
    for i in range(0, len(channels)):
        channelNetworks.append(channels[i].getTotalNetworks())
    
    return channelNetworks

def evaluateChannels(availableChannels, channels):
    ids = getAllIDs(channels)
    packets = getPercentages(getAllPackets(channels))
    stations = getPercentages(getAllStations(channels))
    networks = getPercentages(getAllNetworks(channels))
    evaluations = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    for i in range(0, 14):
        if ((i + 1) in ids):
            channel = getIndex(availableChannels, (i + 1))
            #print(channel)
            evaluations[i] = 0.45*packets[channel] + 0.2*stations[channel] + 0.35*networks[channel]
        else:
            evaluations[i] = 0
    
    return evaluations

def evaluateNeighboringChannels(evaluations):
    hevaluations = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    nevaluations = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    oevaluations = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fileName = ""
    if (datetime.datetime.now().hour == 12):
        fileName = "morning_measurements.txt"
        oevaluations = openFile(fileName)
    elif (datetime.datetime.now().hour == 16):
        fileName = "noon_measurements.txt"
        oevaluations = openFile(fileName)
    elif (datetime.datetime.now().hour == 21):
        fileName = "night_measurements.txt"
        oevaluations = openFile(fileName)
    
    for i in range(0, 14):
        if (i == 0):
            nevaluations[i] = 0.7*evaluations[i] + 0.3*(0.5*evaluations[i+1])
        elif (i==13):
            nevaluations[i] = 0.7*evaluations[i] + 0.3*(0.5*evaluations[i-1])
        else:
            nevaluations[i] = 0.7*evaluations[i] + 0.3*(0.5*evaluations[i-1] + 0.5*evaluations[i+1])
        
        hevaluations[i] = 0.8*nevaluations[i] + 0.2*oevaluations[i]
    
    print(fileName)
    writeFile(fileName, hevaluations)
    
    return hevaluations
        
def openFile(fileName):
    oevaluations = []
    with open(fileName) as f:
        line = f.readline()
        #oevaluations.append(float(line))
        while line:
            print(float(line))
            oevaluations.append(float(line))
            line = f.readline()
    
    return oevaluations

def writeFile(fileName, hevaluations):
    print("Writing to ", fileName)
    with open(fileName, 'w') as f:
        nline = 1
        for line in hevaluations:
            f.write(str(line))
            if (nline != 14):
                f.write('\n')
            nline += 1
          
def findBestChannels(hevaluations):
    bestChannel = min(hevaluations)
    bestChannels = []
    for i in range(0, 14):
        if (bestChannel == hevaluations[i]):
            bestChannels.append(i+1)
    
    return bestChannels

if __name__ == '__main__':
    print(findChannels(wifiData))
    availableChannels = findChannels(wifiData)
    #f(channels)
    channels = prepareChannels(availableChannels)
    evaluations = evaluateChannels(availableChannels, channels)
    hevaluations = evaluateNeighboringChannels(evaluations)
    
    for i in range(0, 14):
        print("Channel " + str(i+1), evaluations[i])
    
    print("----")
    for i in range(0, 14):
        print("Channel " + str(i+1), hevaluations[i])
        
    print(findBestChannels(hevaluations))