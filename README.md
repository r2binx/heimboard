# 🚧 HEIMBOARD [WIP] 🚧
Manage your homeserver.

**Features include:**
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
It's using [auth0](https://auth0.com/) for login and permission management. (Thanks [@wiomoc](https://github.com/wiomoc) for help setting it up!)

For more information and how to set it up check out this [README.md](https://github.com/r2binx/heimboard/blob/main/frontend/README.md)

## Backend
The backend is written with [FastAPI](https://fastapi.tiangolo.com/).
The endpoints are also secured by [auth0](https://auth0.com/) 

You can find the latest server binaries [here](https://github.com/r2binx/heimboard/releases/tag/latest) (shout-out to [hydrun](https://github.com/pojntfx/hydrun) for simple multi-architecture builds).

For more information and how to set it up check out this [README.md](https://github.com/r2binx/heimboard/blob/main/backend/README.md)

## Roadmap
- [x] System theme [Frontend]
- [ ] Own user role management
- [ ] Change backend settings/components
- [ ] Generate API endpoints dynamically for modules [Backend]
- [ ] Switch to GraphQL API
- [ ] Display [S.M.A.R.T.](https://en.wikipedia.org/wiki/S.M.A.R.T.) data for disks
- [ ] Display CPU temperature
- [ ] Docker images

## Preview
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151374368-916dca67-e796-4298-89e7-c4525fb39af1.png#gh-dark-mode-only" width="500" />
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151374537-4da87f35-4ac9-4140-a464-6e8ea706c9f3.png#gh-dark-mode-only" width="500" />
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151374635-35f76823-3f4f-4734-910a-75d371ca0a99.png#gh-dark-mode-only" width="500" />
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151377524-b43e3a28-e9b2-4f2b-9ea0-129e012b163b.png#gh-light-mode-only" width="500" />
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151377528-bce667ff-98cb-4f87-be97-d77555ce3b67.png#gh-light-mode-only" width="500" />
</p>
<p align="center">
<img src="https://user-images.githubusercontent.com/33635402/151377529-d7193dd3-faae-4957-a2d4-774f579aac35.png#gh-light-mode-only" width="500" />
</p>

