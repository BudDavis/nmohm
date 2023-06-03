import asyncio

import websockets

import json

class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

def handle_command(C):
    print(C)
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
             case "STATUS":
                 print("it is a status")
             case "CONFIGURATION":
                 print("it is a config")
             case "LOAD_WAYPOINTS":
                 print("it is a load waypoints")
             case "RETURN WAYPOINTS":
                 print("it is a return waypoints")













    except json.decoder.JSONDecodeError:
        print(">> "+C+" is not JSON")

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

async def handler(websocket):
    print(">> open connection")
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            print("<< closed connection")
            break
        #print(message)
        handle_command(message)


if __name__ == "__main__":
    asyncio.run(main())

