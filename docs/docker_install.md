## Install Docker as non-root user
Install Docker as non-root user:

If you installed Docker 20.10 or later with RPM/DEB packages, you should have dockerd-rootless-setuptool.sh in /usr/bin.

Run dockerd-rootless-setuptool.sh install as a non-root user to set up the daemon:

```bash
dockerd-rootless-setuptool.sh install
[INFO] Creating /home/testuser/.config/systemd/user/docker.service
...
[INFO] Installed docker.service successfully.
[INFO] To control docker.service, run: `systemctl --user (start|stop|restart) docker.service`
[INFO] To run docker.service on system startup, run: `sudo loginctl enable-linger testuser`

[INFO] Make sure the following environment variables are set (or add them to ~/.bashrc):

export PATH=/usr/bin:$PATH
export DOCKER_HOST=unix:///run/willeke.acampo/1000/docker.sock
```

Check if env variables are set:
echo $PATH | grep -q "/usr/bin" && echo "Found" || echo "Not found"

### Install Docker Image

```bash
# pull image from docker hub repository
docker pull osgeo/gdal:ubuntu-small-latest

# create the container and enter it
docker run -it osgeo/gdal:ubuntu-small-latest

root@<container-id>:/#
```

### Check the pre-installed package versions in the image

```bash
root@049c755ca6ff:/# python
Python 3.10.6 (main, Nov 14 2022, 16:10:14) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import gdal
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'gdal'
>>> from osgeo import gdal
>>> gdal.__version__
'3.7.0dev-8ec21bbf7073f9105a2b4bf70adb6dce0d295874'
# exit python
>>> exit()
```

```bash
# exit docker container
root@049c755ca6ff:/# exit
```


### Create Dockerfile which install sadditional packages

**pip, pipx, poetry**
See docker file

## Build image
```bash
# build docker image
docker build .
docker build -t <image-name>:<image-tag> .

# list docker images
docker images

# enter docker image
docker run -it <image-id>

# remove docker image
docker rmi <image-id>

# remove all unused docker objects
docker system prune
```

### STEPS FROM COMMAND LINE
1. create a container image from a dockerfile
- cd /path/to/Dockerfile/location
- docker build -t <image-name><tag> .
- docker build -t gdal-python:0.0.1 .
- -t tag, . build from cwd

2. List information
- docker images (container images)
- docker ps (running containers)
- docker ps -a (started and stopped containers)

3. enter container
- docker run -it <image-id>

4. stop container & delete all stopped containers
- docker stop <container-id> && docker system prune

5. add folder (volume) to container
- /home/willeke.acampo/ac_config
- /data/P-Prosjekter2/152022_itree_eco_ifront_synliggjore_trars_rolle_i_okosyst/data
- docker run --rm -it -v /path/to/local/or/nework/folder/:/mnt/ <image-name>:<image-tag>
  > starts a new container, remove it if it exists mount folder to /mnt/ inside the container and run container in interactive mode.
- docker run -v /path/to/local/or/nework/folder/:/mnt/ <image-name>:<image-tag>
  > starts a new container in detached mode. This means that the container will run in the background even after you exit the terminal.

## STEPS IN VS CODE
1. creates a container from the devcontainer.json
   - devcontainer.json specifies how to build the container: which image, which folders to mount etc.
   - if you don't have a devcontainer.json, vs code can build one from your dockerfile or from standard templates.
2. Open VS code in the container
  - CTRL + SHIFT + P
  - Dev Contains: Reopen Folder in container ...
3. Close container in VS code
  - CTRL + SHIFT + P
  - Dev Contains: Reopen Folder locally ...

**NOTE**:
VS Code automatically "mounts" your workspace folder to the container:
/workspaces/project-name/
See [template_devcontainer.json](.devcontainer/template_devcontainer.json) on how to customize your vs code in the container and how to mount folders to the /workspace/project-name/ container path.
