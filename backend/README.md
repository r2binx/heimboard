# FastAPI based backend
- Uses system libvirt connection
- Jellyfin API
- Tautulli for Plex API
- Sabnzbd API

## Usage
There are two ways of running the backend. Either by downloading the prebuilt binaries or straight from source.

The first thing to do is to get and setup [.config](https://github.com/r2binx/heimboard/blob/main/backend/.config) according to your neeeds.

### Prebuilt
- download the binary for you architecture e.g.: `wget https://github.com/r2binx/heimboard/releases/download/latest/heimboard-backend.linux-$(uname -m)`
- make sure it's executable `chmod +x heimboard-backend.linux-$(uname-m)`
- run it `./heimboard-backend.linux-$(uname-m)`
- make sure `.config` is in the same directory

### Manually
- configure `.config`
- Install dependencies: `make deps`
- run `make dev`

-----
### Wakeup server
The wakeup server is optional and is supposed to run on a different machine in your network.

Everything here applies to it as well. To set it up simply replace `heimboard-backend` by `wakeup` in the commands.


## Build
- install [pyinstaller](https://github.com/pyinstaller/pyinstaller) either
- Make sure your dependencies are installed (`make deps `) 
- run `make build`
