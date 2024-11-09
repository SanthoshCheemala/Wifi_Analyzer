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

def findBestChannels(hevaluations):
    bestChannel = min(hevaluations)
    bestChannels = []
    for i in range(0, 13):
        if (bestChannel == hevaluations[i]):
            bestChannels.append(i+1)
    
    return bestChannels

if __name__ == '__main__':
    hevaluations = openFile("morning_measurements.txt")
    print(findBestChannels(hevaluations))