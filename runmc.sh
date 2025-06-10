#!/bin/bash
docker run --name "mc" --rm --network=host -it -p 25565:25565 -v /srv/mc/:/mc -t -d mc:latest
