# Computer-Statistics-API
A Python API which can be used to monitor, collect, and track different statistics about a computer.
This has been tested on Python Version 3.11.X, but should be able to work on others.

The python script uses ```FastApi``` to create a API that is public to the internet, as well as ```pynvml``` and ```psutil``` to
collect information on the computer. This comes together to get a local API which can be called on and read.

# Examples
This repo also contains examples of what the data can be used for. In this repo, it has been used to make a simple Web Monitoring 
Application which can be access over the internet with the right configuration and port forwarding. The site uses ```Chart.js```
as well as ```Bootstrap``` to give structure and display data which is readable to humans, with our backend being the ```FastAPI```
to host and collect the data from the local machine as well as ```Node.Js``` to host our front end and serve it to users.

This can be useful for people in the crypto space with monitoring their servers which are not in their immediate access, such
as off site farms which cheaper electricity and such.

This example isnt optmised for lower API calls, and calls quite a large ammount. 
TODO: Fix this.

## Known API Improvements to be Made:
- CPU Temp Monitoring
  >Will have to add as its a very useful statistic to have on hand.
- Support for Multi-GPU configurations  
  > Will be hard, but doable because I don’t currently have two or more GPUs on hand.
- Support for Multi-CPU configurations  
  > This is a feature I will add in the later stages of the project, as most miners using this project will have multi-GPUs, not multi-CPUs, since CPU mining isn't very profitable.
- Support for AMD GPUs  
  > I will have to add this soon to accommodate red-team users and GPU miners.

**Last Major Update:** 22/02/2025
