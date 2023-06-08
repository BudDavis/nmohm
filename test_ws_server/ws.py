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
                 state['elapsedtime'] = 0
                 state['mode'] = "FREEZE"
                 # go to the first position on the list
             case "FREEZE":
                 print("it is a freeze")
                 state['mode'] = "FREEZE"
             case "RUN":
                 print("it is a run")
                 state['mode'] = "RUN"
             case "STATUSREQUEST":
                 print("it is a status request")
                 r = {"cmd": "status", 
                      'id': state['id'],
                       'role':state['role'],
                       'mode':state['mode'],
                       'elapsedtime':state['elapsedtime'],
                       'kmlfile':state['kmlfile']}
             case "INIT":
                 state['id'] = CMD['id']
                 r = {}
             case "LOADWAYPOINTS":
                 print("it is a load waypoints")
             case "WAYPOINTFILE":
                 print("it is WAYPOINTFILE")
                 state['kmlfile'] = CMD['filename']

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
    state = {"id":0,"role":"","kmlfile":"unknown","mode":"FREEZE","elapsedtime":0}
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            print("<< closed connection")
            break
        #print(message)
        #if state['mode']=='RUN':
        state['elapsedtime'] = time.monotonic() - zero_time;
        r = handle_command(message,state)
        print("sending "+json.dumps(r))
        print(time.monotonic())
        await websocket.send(json.dumps(r))


if __name__ == "__main__":
    asyncio.run(main())

