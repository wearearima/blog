---
layout: post
title:  "Using Docker inside Kubernetes"
date:   2020-11-11 9:00:00
author: urko
lang: en
categories: docker, kubernetes
tags: docker, kubernetes, k8s, jenkins, privileged
header-image: 2020-11-11-docker-en-kubernetes/whale.jpg
---

In a [previous post]({{ site.baseurl }}/en/2020/09/10/deberias-utilizar-contenedores-privilegiados){:target="_blank"} I talked about the problem of granting privileges to a container and the risks that this entails. Today I want to present a specific case in which privileges are granted to a container and give some alternatives.

One of the most popular Continuous Integration tools is [Jenkins](https://www.jenkins.io/){:target="_blank"}. It stands out for the amount of *plugins* that its community makes available to users and the freedom it grants to create *pipelines*. In addition, it offers us images with which it can be deployed in containers, including in a Kubernetes cluster!

And you would imagine that doing this should be pretty easy: you write a deployment that has a pod with the Jenkins image and you already have it (apart from installing plugins and configuring it). But what if I want to *build* images inside a *pipeline*?   

Then you need the Docker CLI or [Docker plugin for Jenkins](https://plugins.jenkins.io/docker-plugin/){:target="_blank"}. But these in turn need a Docker daemon to be able to make the corresponding requests. Things start getting complicated. 

In this post we are going to explore, step by step, different approaches to deploying Jenkins with Docker in Kubernetes, and explain the evolution of each one.

## Deployments

### 1. Docker in Docker

The most straightforward deployment is: You need a Docker daemon, so you install it. You take the Jenkins base image, install the Docker Engine, and create a custom image with both programs. Done!

This is possible; you can try it and it works. But it has certain implications that make it a bad option:

* **Storage drivers**: This problem arises from incompatibilities between different container file systems. Without going into detail, the containers use their own file systems (AUFS, BTRFS, Device Mapper, ...) and these may not be compatible with each other. Depending on the type of system used by the node's *container runtime* and that used by the container's Docker daemon, problems can occur. These incompatibilities will probably be resolved as new versions of DinD (Docker in Docker) are released, but the risk remains latent.
* **Cache**: If you want to use the Docker cache, which you probably will, and you want this cache to be accessible between different replicas, you should mount `/var/lib/docker` as a volume in each container. But Docker is intended to have exclusive access to this directory, and having two or more daemons accessing it at the same time can lead to data corruption problems.
* **Security**: In order to run the Docker daemon inside a container, it must be run with privileges (`--privileged` in Docker or `securityContext.privileged: true` in Kubernetes). **It is a requirement**. This implies serious security risks, which we explain in [this post]({{ site.baseurl }}/en/2020/09/10/deberias-utilizar-contenedores-privilegiados){:target="_blank"}.

<p align="center">
    <img src="/assets/images/2020-11-11-docker-en-kubernetes/dind.png">
</p>

### 2. Docker out of Docker

In this variant, the cluster node Docker Daemon is used. To do this, you need to use an image with Jenkins and Docker CLI, mount the socket from the node to the container, and run the container with a group that has access to the socket.

Advantages over Docker in Docker:

* Fixes cache and storage driver issues, which are inherent in Docker in Docker.
* We no longer create Docker daemons, but now reuse the existing one, which minimizes the use of resources.
* Avoids using privileged containers.

But even so, it too has its problems:

* We maintain security risks, since by having access to the Docker socket, we can very easily run a privileged container that will give us access to the *host*
* Mounting node directories in a *pod* is bad practice. In fact, in this particular case, we cannot assume that the Docker socket will exist in the node. Depending on the *container runtime* of the cluster, it may not, so this solution might not be possible
  > Note: At the time of writing, the three major Kubernetes cloud providers (AWS, Azure and Google Cloud) provide nodes with the Docker runtime container, which does have a Docker socket.
* As we are using the node daemon, all the containers we run are siblings of the container from which we created them. This carries risks in itself, since problems can occur when naming containers (naming two containers the same, or two volumes). Also, containers that have not been run from Kubernetes are not managed by Kubernetes, so we can run into resource allocation issues (container uses node resources but Kubernetes isn't aware of it).

<p align="center">
    <img src="/assets/images/2020-11-11-docker-en-kubernetes/dood.png">
</p>

### 3. Docker in Docker sidecar

The last alternative is to deploy two containers in the same pod, one with Jenkins and Docker CLI (as in Docker out of Docker) and another with Docker Engine, and use the TCP socket, since the network in the same pod is shared.

Although at first it may seem like taking a step backwards, there is an explanation: we are able to modify the Docker daemon options. And what do we want that for? We can install authorization *plugins* that prevent running privileged containers on that daemon (explained in more detail [in the previous post]({{ site.baseurl }}/es/2020/09/10/deberias-utilizar-contenedores-privilegiados){:target="_blank"}).

Advantages over Docker out of Docker:

* We resolve security problems. By having no permissions to run privileged containers and not mounting any node directories, the node is isolated from the pod.

Disadvantages:

* We take a step backwards and return to the possible problems of cache and storage drivers.
* The container with Docker Engine will have to be run in privileged mode.

<p align="center">
    <img src="/assets/images/2020-11-11-docker-en-kubernetes/dind-sidecar.png">
</p>

## Conclusion

None of the methods for deploying Jenkins in Kubernetes is good. They all carry security risks and certain drawbacks, and we will have to decide which of them we prefer for our deployment. For interest, in the [official Helm chart](https://github.com/helm/charts/tree/master/stable/jenkins){:target="_blank"} they resolve it by mounting the node *socket* (DooD) and without running privileged containers, but as we explained, this still has security risks.

The recommendation is not to use Docker as an image *building* tool in Jenkins. There are *daemonless* solutions that avoid the problems described in this document, which we will explore in a future post.