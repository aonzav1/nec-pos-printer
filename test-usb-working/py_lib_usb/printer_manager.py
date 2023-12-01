
import print_test

#Pool of printer, could be define using Dict (string-based) or List (index-based)
printers = []

def InitPrinters():
    print("Initializing printers")
    #Assume now we only have 1 printer and connect on start server, so test out print
    print_test.InitTest()
    #Initialized printer all get all information
    return True

#May be we should handle onConnect and onDisconnect of printers to add/remove from printer pool

def GetPrinters():
    #Get all information of printer and its information
    return [{"printerId":"A","status":"printing"},{"printerId":"B","status":"available"},{"printerId":"B","status":"unavailable"}]

def AvailablePrinter():
    #Get only one printer that available at the moment
    return "AVPRINTER001" #return id or identifier of that printer

def SetActivePrinter(printerId, status):
    #Get only one printer that available at the moment
    return True #return result of active / deactiving the printer

def GetStatus(printerId):
    #Get the status of specific printer
    return {"printerId":printerId,"status":"available"}

def SendPrintOrder(device,message): #enter device info or id to specify which printer to print
    print("There's order to print "+str(message))
    print_test.PerformPrint(str(message))
    #Do send printing order and get immediate error if caught.
    return True

def CutOrder(device):
    print_test.PerformCut()
    return True

#NOT SURE WHAT IS BW1/BW2 YET (Thought it was back feed, but not tested well yet)
def FeedBW1():
    print_test.FeedBW1()
    return True

def FeedBW2():
    print_test.FeedBW2()
    return True