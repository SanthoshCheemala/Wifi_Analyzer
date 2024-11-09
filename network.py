class Network:
    def __init__(self, channel):
        if(channel > 0 and channel < 14):
            self.channel = channel
        else:
            print("Unavailable channel input: " + channel)
        self.totalData = 0
        self.stations = 0

    def addStation(self, packets):
        self.stations += 1
        self.totalData += packets

    def getChannel(self):
        return self.channel

    def getStations(self):
        return self.stations

    def getTotalNetworkData(self):
        return self.totalData

#kathe ap exei isxy