sudo docker run \
  --rm \
  -v /srv/bloodybot:/bot \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name "bloodybot" \
  -it \
  -d \
  -t bloodybot:0 \
  bash
