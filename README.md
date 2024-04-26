# Docker_Hermes
Hermes is an Application who give information about a the route to take  and the weather of the City that we want to know. 

We can see all the informations in the localhost:5000 webpage.

You need docker installed and be in the same repository of the Dockerfile.

Command to run:
- sudo docker build --tag python-docker .
- sudo docker run -d -p 5000:5000 python-docker
