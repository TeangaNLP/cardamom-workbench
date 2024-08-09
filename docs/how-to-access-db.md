# how to access postgres docker container to check if data was added
  - sudo docker ps
  should show you the postrgres container id
  - copy the container id
  - sudo docker exec -it <container_id> psql -U cardamom -d workbench
