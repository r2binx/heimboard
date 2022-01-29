# FastAPI based backend
- Uses system libvirt connection
- Jellyfin API
- Tautulli for Plex API
- Sabnzbd API

## Usage
There are two ways of running the backend. Either by downloading the prebuilt binaries or straight from source.

The first thing to do is to get and setup [.config](https://github.com/r2binx/heimboard/blob/main/backend/.config) according to your neeeds.

### Prebuilt
- Download the binary for you architecture e.g.: `wget https://github.com/r2binx/heimboard/releases/download/latest/heimboard-backend.linux-$(uname -m)`
- Make sure it's executable `chmod +x heimboard-backend.linux-$(uname-m)`
- Mun it `./heimboard-backend.linux-$(uname-m)`
- Make sure `.config` is in the same directory

### Manually
- Configure `.config`
- Install dependencies: `make deps`
- Run `make dev`

-----
### Wakeup server
The wakeup server is optional and is supposed to run on a different machine in your network.

Everything here applies to it as well. To set it up simply replace `heimboard-backend` by `wakeup` in the commands.

**I reimplemented it in Go to improve compatibility and efficiency. You'll find releases available [here](https://github.com/r2binx/heimboard-wakeup-go) soon.**


## Build
- Install [pyinstaller](https://github.com/pyinstaller/pyinstaller) e.g. by running `pip3 install pyinstaller`  
- Make sure your dependencies are installed (`make deps `) 
- Run `make build`
