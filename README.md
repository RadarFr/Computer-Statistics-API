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
as off site farms which cheaper electricity and provide benifts crypto mining.

This example isnt optmised for lower API calls, and calls quite a large ammount. In the future this will be fixed but the surgested
use for this is to make 1 call a second and save the JSON responce to set every varable in the code. This will lower the ammount of calls, decreasing
cpu usage, increaing internet bandwidth and making it sutable to crypto mine with.

NOTE: AMD gpus are supported, on linux, this is due to a limation in the libary used which throws a error when running on windows.
For the use case of cypto mining, this shouldnt be too much of a problem as most miners are on linux.

## Known API Improvements to be Made:
- Security
  > in the future I will have to add a better CORS policy as well as a password and roles system. These could include: ADMIN which can control
  > other parts of the PC such as shutting down and restarting the pc. OBSERVER which cannot control anything, but can view every statisitc. and
  > GUEST, which can only monitor GPU Temps, CPU Temps and Usages of both.
- Support for Multi-GPU configurations  
  > Will be hard, but doable because I don’t currently have two or more GPUs on hand.
- Support for Multi-CPU configurations  
  > This is a feature I will add in the later stages of the project, as most miners using this project will have multi-GPUs, not multi-CPUs, since CPU mining isn't very profitable.
