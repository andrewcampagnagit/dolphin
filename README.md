# dolphin 

[![Generic badge](https://img.shields.io/badge/python-3.7-blue)](https://shields.io/)
[![Generic badge](https://img.shields.io/badge/dolphin-beta--3-orange)](https://shields.io)
[![Generic badge](https://img.shields.io/badge/kubernetes-1.18.0-blue)](https://shields.io)

#### Beta 3 is here!

We intend Beta 3 to be a final development prior to starting any gamma testing! Though probably buggy
this will serve as the code base for many future versions of Dolphin.

#### Summary

Dolphin aims to ease the multistage cloud application deployment process
by creating instruction blocks for each part of the process. What makes this
process different is the robust set of functionality that dolphin features
in its templates. You can specify instruction blocks to store
variables from deployed resources along the way dynamically. Another great 
feature is the ability to impose a wait instruction on a resource; this halts 
all operations from that point in the deployment until a specific condition is
met, like a pod in Running status. These features come with our of the box
BlockProcessors, but you can write your own processor easily.

#### Fast start guide

Dolphin is packaged into a Red Hat Enterprise Linux container image for the best cross platform compatability.

**For Linux users** We reccomend podman
**For Windows, Mac, and all other OS** We reccomend docker

Pull down the image from quay.io
```bash
podman pull quay.io/dolphin/dolphin:latest
```
or 
```bash
docker pull quay.io/dolphin/dolphin:latest
```

Run the example instructions
```bash
podman run dolphin:latest deploy -mF /dolphin/example/manifest.json
```
or
```bash
docker run dolphin:latest deploy -mF /dolphin/example/manifest.json
```

**Comprehensive guide** <URL_TO_GUIDE>

**Project contribution rules** <URL_TO_HOW_TO_CONTRIBUTE>


