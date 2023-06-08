# Test Program to develop / debug the NMOHM web page.
# Pretends to be all of the "UE5 Stations".
#
# Top Level requirements
#   Only speak when spoken to.
#   Just enough functionality to stimulate the system
#
#
#

import asyncio

import websockets

import json

import time

def handle_command(C,state):
    # given a JSON string, that has a 'CMD' in it, this function
    # will do whatever is expected.
    #
    # the state maintains the current state of this specific 'station'
    #
    # it returns a json string if that is expected
    r = {}  # the 'return value'

    try:
         CMD = json.loads(C)
         #print(CMD)
         match (CMD['cmd'].upper() ):
             case "RESET":
                 state['elapsedtime'] = 0
                 state['mode'] = "FREEZE"
                 # reset is a transient state.  it does two things,
                 # first, it transitions the mode to FREEZE
                 # next it moves the ownship to the start of the
                 # waypoint list.  (however that is eventually implemented)
             case "FREEZE":
                 # in freeze, the ownship will not move in space.
                 state['mode'] = "FREEZE"
             case "RUN":
                 # in run, the ownship moves in space
                 state['mode'] = "RUN"
             case "STATUSREQUEST":
                 # replies with the current status, which is
                 # most of the 'state' variable
                 r = {"cmd": "status", 
                      'id': state['id'],
                       'role':state['role'],
                       'mode':state['mode'],
                       'elapsedtime':state['elapsedtime'],
                       'kmlfile':state['kmlfile']}
             case "INIT":
                 # is this needed or not?
                 # at this point, i think not, but it does provide some human readable
                 # debug to be in the communications.
                 #  the web page is saying "dude, you are id number xxx.  please include this when
                 #  you send me data
                 state['id'] = CMD['id']
                 r = {}
             case "WAYPOINTFILE":
                 # this just accepts the new waypoint file.
                 # the current waypoint file continues to run
                 # until a reset is received
                 state['kmlfile'] = CMD['filename']
    except json.decoder.JSONDecodeError:
        print(">> " + C + " is not JSON")
    return r

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

async def handler(websocket):
    print(">> open connection")
    #zero_time = time.monotonic()
    # every connection is going to start out in freeze.  that may not be how the
    # real system works.  in the real system you should be able to connect at anytime
    # and not impact what is currently being done
    state = {"id":0,"role":"","kmlfile":"unknown","mode":"FREEZE","elapsedtime":0,"lastruntime":0,"lastexectime":0}
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            print("<< closed connection")
            break
        #print(message)
        if state['mode'] == "RUN":
           state['elapsedtime'] = state['elapsedtime'] + time.monotonic() - state['lastexectime']
        r = handle_command(message,state)
        print("sending "+json.dumps(r))
        # lastexectime is the last time this instance was ran
        state['lastexectime'] = time.monotonic(); 
        print(time.monotonic())
        await websocket.send(json.dumps(r))


if __name__ == "__main__":
    asyncio.run(main())

