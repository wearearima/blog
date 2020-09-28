---
layout: post
title:  Should you use privileged containers?
date:   2020-09-10 9:00:00
author: urko
lang: en
categories: docker
tags: docker
header-image: 2020-09-10-deberias-utilizar-contenedores-privilegiados/lock.jpg
---

When working with containers it is important to always keep in mind the security of the container, or more importantly, of the machine that runs it. A bad decision to deploy a container can grant you full access to the host, and this can have negative consequences if this container has a malicious purpose or if an unauthorized person gains access to it.

When reading about good practices to follow when running containers, one of the most common recommendations is: "*Do not run the container in privileged mode and give it only the capabilities it needs, if possible none*". It is a good recommendation, but some questions arise:
* What is privileged mode?
* Why is it not recommended to use it and what is it possible to do with a privileged container?
* Is it necessary to be a privileged user (*root*) or is any user inside a privileged container dangerous?
* Is there a way to prevent privileged containers from running?

## What is privileged mode?

Containers start with a number of Linux capabilities by default. In addition to the ones that come by default, there are many others that can be added to our container with the `--cap-add =` option. The full list of capabilities and what they do can be seen in the [official documentation](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities){:target="_blank"}. By starting the container in privileged mode, it is granted all capabilities, as well as access to all devices on the host and certain changes are made to AppArmor or SELinux in order to give the container similar access to those the other processes on the host have.
<p align="center">
    <img src="/assets/images/2020-09-10-deberias-utilizar-contenedores-privilegiados/no-devices.png">
</p>

<label style="text-align: center; display: block;">List of devices in a container</label>

<p align="center">
    <img src="/assets/images/2020-09-10-deberias-utilizar-contenedores-privilegiados/devices.png">
</p>

<label style="text-align: center; display: block;">List of devices in a container **in privileged mode**</label>

## Why is it not recommended to use it and what is it possible to do with a privileged container?

By definition, a container must be isolated from the host where it is running. This implies that it must have a different directory tree, its own users and groups, its own devices ... even the hardware resources of the machine may be different. This is so that a process running in a container does not know that a host exists, and that the container and its processes do not depend on the host.

By running a privileged container, we break this isolation, since the container gains access to the host's resources and devices, and also has all possible permissions to use them. Among other things, this allows it to perform actions such as:
* Modifying the host's filesystem.
* Controlling host processes.
* Granting permissions for host resource allocation.

## Is it necessary to be a privileged user (*root*) or is any user inside a privileged container dangerous?

In principle, all the actions that we have listed require administrator privileges within the container for them to be carried out. This means that, in theory, a non-privileged user inside a privileged container is not able to break this isolation.

However, it is common to find images (and build them) where the default user is a privileged user (usually *root*). This is often the case due to the image creator’s ignorance, because the creator prefers to delegate the responsibility of modifying the user, or because the image needs to execute a process with a privileged user.
<p align="center">
    <img src="/assets/images/2020-09-10-deberias-utilizar-contenedores-privilegiados/top5.png" height="420">
</p>

<label style="text-align: center; display: block;">The five most popular images in Docker Hub have a privileged user by default</label>

Additionally, vulnerabilities have also been found ([CVE-2019-5736 detected in February 2019](https://blog.dragonsector.pl/2019/02/cve-2019-5736-escape-from-docker-and.html){:target="_blank"}) where an unprivileged user is able to exploit the capabilities of a privileged container and access the host. Although much less common than the case of privileged users, it is a risk to bear in mind, because if there has been one, then more could be detected.

## Is there a way to prevent privileged containers from running?

There are *plugins* installed in the Docker daemon that allow functionalities to be extended. For this specific case, we are interested in the [*authorization plugin*s](https://docs.docker.com/engine/extend/plugins_authorization/){:target="_blank"}. As they say in the Docker documentation, the default authorization of `dockerd` is "all or nothing", in other words, either you have access to the daemon and you can do anything, or you don't have access to it at all.

> Note: Docker daemon or `dockerd` is a process that runs on the host and is in charge of managing its containers.

With authorization *plugin*s we have the freedom to define policies that allow us to regulate access in a granular way, giving permission, for example, to a specific user to perform certain actions that others cannot. And what does this have to do with the privileges of a container?

Well, each *plugin* works in a different way, but they all end up doing the same thing: they intercept the daemon's API call and check if that call is allowed or not, depending on the policies we have defined. That means **only calls that DO NOT attempt to run privileged containers will be executed**.

To demonstrate, we have chosen the *plugin* [opa-docker-authz](https://github.com/open-policy-agent/opa-docker-authz){:target="_blank"}, which in a simple and very visual way, lets us define this specific rule.

```rego
 package docker.authz

 default allow = false

 allow {
     not deny
 }

 deny {
     privileged
 }

 privileged {
     input.Body.HostConfig.Privileged == true
 }
```

The `input` document corresponds to the body of the call made to the Docker API. So, if this body contains an attribute called `Body.HostConfig.Privileged` with value `true`, we will deny the call. This is just an example, but much more elaborate policies can be created for each specific case.

As we have seen before, the greatest security risk comes from allowing the use of privileged mode for containers, so with a *plugin* like this, we could secure our installation to a great extent.

## Conclusions

**Using a privileged user or giving a container Linux capabilities is never to be recommended**. That said, there are times when there is no alternative, but we should try to grant the minimum number of possible priorities to a container, enough for it to fulfill its function and no more.

Privileged mode should be used for containers as little as possible, in closed environments where we know the people who are going to have access to that container and can trust them. Where there is a risk that a user we do not trust could access the container, we should discard privileged mode to prevent problems. If it is necessary to grant a user permissions to create containers, it is recommended to secure the host's dockerd with an authorization plugin.