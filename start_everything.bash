#!/bin/bash
#
# This script starts the development environment for working on the 
# webpages on a standalone system.
# Each application needed is started in a window.

# First is an http server
xterm -e "python3 -m http.server" &

# Next, a websocket server
xterm -e "cd test_ws_server;python3 ws.py" &

# the tile server
docker run \
    -p 8080:80 \
    -v osm-data:/data/database/ \
    -d overv/openstreetmap-tile-server


