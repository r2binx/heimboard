# 🚧 HEIMBOARD [WIP] 🚧
Manage your homeserver.

features include:
- scheduled boot
- remote start/shutdown
- start/stop Libvirt VMs
- change memory for active VMs
- display system usage
- display storage for selected mounts
- external network usage ([fritzconnection](https://github.com/kbr/fritzconnection))

## Overview
This project was started to better manage my homeserver and turn it on/off remotely as well as start my VMs.
It's possible to to boot it with a tiny backend on a seperate macheine (Pi3 in my case) to send the [Wake-on-LAN](https://en.wikipedia.org/wiki/Wake-on-LAN) signal to the server.

Because my _desktop_ is basically just a VM thanks to vfio I needed a simpler way to manage them from my phone or other remote devices.
This milestone is reached and I am expanding it in the future to make it more generic & configurable for other users.

## Frontend
The frontend is based on [Vue3](https://github.com/vuejs/core) & [Vite](https://github.com/vitejs/vite).
It's using [auth0](https://auth0.com/) for login and permission management.

For more information and how to set it up check out this [README.md](https://github.com/r2binx/heimboard/blob/main/frontend/README.md)

## Backend
The backend is written with [FastAPI](https://fastapi.tiangolo.com/).
The endpoints are also secured by [auth0](https://auth0.com/).
You can find the latest server binaries [here](https://github.com/r2binx/heimboard/releases/tag/latest).

For more information and how to set it up check out this [README.md](https://github.com/r2binx/heimboard/blob/main/backend/README.md)

## Images
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151374368-916dca67-e796-4298-89e7-c4525fb39af1.png" width="500" />
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151374537-4da87f35-4ac9-4140-a464-6e8ea706c9f3.png" width="500" />
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151374635-35f76823-3f4f-4734-910a-75d371ca0a99.png" width="500" />
</p>
