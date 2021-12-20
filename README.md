# 🚧 [WIP] HEIMBOARD
This is a project to better manage my homeserver and turn it off when idle. Also allows remote users to boot it with a tiny backend on a Raspberry Pi to run the WoL signal to boot the server.

Because my _desktop_ is basically just a VM thanks to vfio I needed a simpler way to manage them from my phone etc.

Hopefully I can expand it in the future to make it more generic & expandable for other users.

## Frontend
The frontend is based on vue3+vite and uses auth0 for login

## Backend
The backend is written in python with fastapi