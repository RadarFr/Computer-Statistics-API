# Computer-Statistics-API
A Python API which can be used to monitor, collect, and track different statistics about a computer.
This has been tested on Python Version 3.11.X, but should be able to work on others.

The python script uses ```FastApi``` to create a API that is public to the internet, as well as ```pynvml``` and ```psutil``` to
collect information on the computer.

# Examples
This repo also contains examples of what the data can be used for. In this repo, it has been used to make a simple Web Monitoring 
Application, which can be access over the internet with the right configuration and port forwarding. The site uses ```Chart.js```
as well as ```Bootstrap``` to give structure and display data which is readable to humans.

This can be useful for people in the crypto space with monitoring their servers which are not in their immediate access, such
as off site farms which cheaper electricity and such.

# Known improvements to be made:
>Cpu Temp Monitoring
>Support Mutli GPU configurations
>Support Multi CPU configurations
>Support AMD GPU's
