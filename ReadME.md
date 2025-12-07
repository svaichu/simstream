# Run GUI apps in headless VM

This script runs GUI applications in a headless virtual machine (VM), it runs a noVNC server which can be accessed through a web browser.

### Clone with submodules
```bash
git clone --recurse-submodules https://github.com/svaichu/simstream.git
```


### Install dependencies

```bash
sudo apt update && sudo apt install xvfb x11vnc -y
```

### Run the script

```bash
cd ~/simstream
./start_server.sh
```
