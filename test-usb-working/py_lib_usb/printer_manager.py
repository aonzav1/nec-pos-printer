
import print_test

printers = []

def InitPrinters():
    print("Initializing printers")
    print_test.InitTest()
    #Initialized printer all get all information
    return True

#May be we should handle onConnect and onDisconnect of printers

def GetPrinters():
    #Get all information of printer and its information
    return [{"printerId":"A","status":"printing"},{"printerId":"B","status":"available"},{"printerId":"B","status":"unavailable"}]

def AvailablePrinter():
    #Get only one printer that available at the moment
    return "AVPRINTER001" #return id or identifier of that printer

def GetStatus(printerId):
    return {"printerId":printerId,"status":"available"}

def SendPrintOrder(device,message): #enter device info or id to specify which printer to print
    print("There's order to print "+str(message))
    print_test.PerformPrint(str(message))
    #Do send printing order and get immediate error if caught.
    return True

def CutOrder(device):
    print_test.PerformCut()
    return True

def FeedBW1():
    print_test.FeedBW1()
    return True

def FeedBW2():
    print_test.FeedBW2()
    return True