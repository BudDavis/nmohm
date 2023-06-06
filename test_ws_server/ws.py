import asyncio

import websockets

import json

import time

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

def handle_command(C,state):
    print(C)
    r = {}
    try:
         CMD = json.loads(C)
         print(CMD)
         match (CMD['cmd'].upper() ):
             case "RESET":
                 print("it is a reset")
             case "FREEZE":
                 print("it is a freeze")
             case "RUN":
                 print("it is a run")
             case "STATUSREQUEST":
                 print("it is a status request")
                 r = {"cmd": "status", 
                      'id': state['id'],
                       'role':state['role'],
                       'mode':state['mode'],
                       'elapsedtime':state['elapsedtime'],
                       'kmlfile':state['kmlfile']}
             case "CONFIG":
                 print("it is a config")
                 state['kmlfile'] = CMD['kmlfile']
                 state['role'] = CMD['role']
                 #state['id'] = CMD['id']
                 #print(" in the case ")
                 #print(state['id'])
                 #print(CMD['id'])          
                 r = {}
             case "INIT":
                 print("it is an init")
                 state['id'] = CMD['id']
                 r = {}
             case "LOAD_WAYPOINTS":
                 print("it is a load waypoints")
             case "RETURN WAYPOINTS":
                 print("it is a return waypoints")

    except json.decoder.JSONDecodeError:
        print(">> " + C + " is not JSON")
        print(" id is ")
        print(state[id])
    return r
async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

async def handler(websocket):
    print(">> open connection")
    zero_time = time.monotonic()
    state = {"id":0,"role":"UNKNOWN","kmlfile":"unknown","mode":"unknown","elapsedtime":0}
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            print("<< closed connection")
            break
        #print(message)
        state['elapsedtime'] = time.monotonic() - zero_time;
        r = handle_command(message,state)
        print("sending "+json.dumps(r))
        print(time.monotonic())
        await websocket.send(json.dumps(r))


if __name__ == "__main__":
    asyncio.run(main())

