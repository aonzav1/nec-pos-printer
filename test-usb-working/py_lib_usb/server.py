from flask import Flask, render_template, request
from datetime import datetime
import printer_manager
from flask_socketio import SocketIO,send,emit
from random_string_generator import generate_random_string
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

CORS(app)

printQueues = []

printer_manager.InitPrinters()

@app.route('/')
def index():
    return render_template('index.html')

#
# BASE CONENCTION
#

@socketio.on('connect')
def onConnect(auth):
    #using emit under @socket.io to response back   emit($eventname,$data)
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def onDisconnect():
    #No need to response back, just as server know the client is disconencted (We could capture and know who connect/disconnect and store list - but no need)
    print('Client disconnected')

def updateStatus(printer,status):
    #use socketio.emit($eventname,$data) to boardcast to all client, actually we don't need to do this - but for illustration
    socketio.emit('status', {"printerId":printer,"status":status})
    
#####################
#   Handle PRINTING
#####################

@socketio.on('message')
def handleTextMessage(message):
    #this is general message read from sample webpage
    print("Received message: "+message)
    if(message[0] == '/'):
      send(readCommand(message))  # come in use when we read /[command]
    send(message)

@socketio.on('json')
def handleJsonMessage(json):
    #just for testing on receiving json
    print("Received message: "+json)
    send(json, json=True)

#HTTP request getting status
@app.route('/status', methods=['GET'])
def requestStatus():
    body = request.get_json()
    #Check if valid infomation
    
    result = makePrintRequest(body.printId)
    
    return result, 201

#HTTP request to print
@app.route('/print', methods=['POST'])
def requestPrint():
    body = request.get_json()
    #Check if valid infomation
    
    result = makePrintRequest(body)
    
    return result, 201

##################
#   FUNCTIONS
##################

def readCommand(message):
  parsedComm = message.split()
  
  #Parse and read commands
  
  if parsedComm[0] == "/help":
    return "/printers - to see all printer and its status <br></br> /status [printerId] - to get printer status <br></br> /print [message] - to print the message"
  elif parsedComm[0] == "/printers":
    return printer_manager.GetPrinters()
  elif parsedComm[0] == "/status":
    if len(parsedComm) <= 1:
      return "Do you mean /status [printerId] ?"
    else:
      return printer_manager.GetStatus(parsedComm[1])
  elif parsedComm[0] == "/print":
    if len(parsedComm) <= 1:
      return "Do you mean /print [message] ?"
    else:
      return printer_manager.SendPrintOrder(0,parsedComm[1])
  elif parsedComm[0] == "/cut":
    printer_manager.CutOrder("TESY ORDER")
    return "CUT !!!"
  elif parsedComm[0] == "/bw1":
    printer_manager.FeedBW1()
    return "Feed BW 1"
  elif parsedComm[0] == "/bw2":
    printer_manager.FeedBW2()
    return "Feed BW 2"
  return message

def makePrintRequest(body):
  printQueues.append(body)
  print(body)
  #Get available printer
  printerId = printer_manager.AvailablePrinter()
  printer_manager.SendPrintOrder(printerId,body)
  updateStatus(printerId,"Received new")
  return {"requestId":generate_random_string(15), "receivedTime":datetime.now(), "printerId":printerId, "queueId":len(printQueues),"message": "You printer message is queued", "body": body }

if __name__ == '__main__':
    socketio.run(app)
