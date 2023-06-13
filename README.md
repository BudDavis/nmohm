# nmohm


The test websocket server:
```
cd test_ws_server
python3 ws.py

```

http server
python3 -m http.server



a quick client
```
python3 -m websockets ws://localhost:8001/
```


https://github.com/Overv/openstreetmap-tile-server.git

docker volume create osm-data
docker run  -v $PWD/asia-latest.osm.pbf:/data/region.osm.pbf -v osm-data:/data/database/ overv/openstreetmap-tile-server import


bdavis@bdavis-Latitude-5420:~$ docker run \
    -p 8080:80 \
    -v osm-data:/data/database/ \
    -d overv/openstreetmap-tile-server 


https://websockets.readthedocs.io/en/stable/index.html
sudo apt install python3-websockets


References:

* https://websockets.readthedocs.io/en/stable/intro/tutorial1.html
* https://www.w3schools.com/bootstrap5/index.php
