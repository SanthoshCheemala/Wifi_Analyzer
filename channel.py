from network import Network
class Channel:
    def __init__(self, identifier):
        if(0< identifier and identifier < 14):
            self.identifier = identifier
        else:
            print("Unavailable channel input: " + identifier)
        self.totalNetworks = 0
        self.totalStations = 0
        self.totalData = 0

    def getTotalData(self):
        return self.totalData

    def getId(self):
        return self.identifier
    
    def getTotalNetworks(self):
        return self.totalNetworks
    
    def getTotalStations(self):
        return self.totalStations
    
    def addNetwork(self, network):
        self.totalNetworks += 1
        self.totalStations += network.getStations()
        self.totalData += network.getTotalNetworkData()

#na ypologistei mesh isxys apo ta aps