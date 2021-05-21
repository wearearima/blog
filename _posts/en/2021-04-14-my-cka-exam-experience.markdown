---
layout: post
title:  "My experience with the CKA exam"
date:   2021-04-14 8:00:00
author: urko
lang: en
categories: kubernetes, certifications, cloud
tags: kubernetes, certifications, cloud, exams, CKA
header-image: 2021-04-14-my-cka-exam-experience/header.jpg
---

Last Monday 22 March I took the exam for the [CKA](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/){:target="_blank"} certificate from the Linux Foundation, and I’m here to tell you about my experience of how I prepared for it and what to expect in the exam. I highly recommend that you also read a [post from my colleague Fernando from a few months ago about the CKAD exam]({{ site.baseurl }}/en/2020/04/28/examen-ckad){:target="_blank"}, which goes into much more detail about the aspects of these exams and helps you to pass them. I got some essential tips from reading his post!

### Previous experiences with Kubernetes

In all honesty, exactly a year ago I knew nothing about Kubernetes - it wasn’t because I had never worked with it, but that I wasn’t even clear about the concept of "container". It’s true that this last year I’ve been working with this tool frequently (which undoubtedly helped me when preparing for the exam), but I think you need no more than a little previous experience. 

### How I prepared for the exam

Despite the knowledge I already had of K8s resources, using `kubectl` or managing clusters, we felt that it was necessary for me to sign up for this course on Udemy: [link](https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests){:target="_blank"}. It begins by explaining the most basic concepts of both administration and Kubernetes resources, which can help people with less experience, and in no time it begins to explain more advanced content.

However, in the exam many questions are about the most basic content, so I personally recommend paying attention to these lessons as well. The course is made up of videos and practical labs, and even has some exams at the end with questions very similar to the real exam.

![Example of lab exercise](/assets/images/2021-04-14-my-cka-exam-experience/exercise.jpg){: .center }
<label style="text-align: center; display: block;">Example of lab exercise</label>

In short, the course does things so well that the syllabus seems quite easy. In my opinion, the exam difficulty does not lie in your knowledge, but in your confidence in operating the cluster and knowing how to manage time well. Looking back, I would say that the course is very complete and I would recommend it to anyone who wants to obtain the certification. 

### The exam

The test consists of 17 questions that have to be done in 2 hours. The difficulty of the questions varies between some very basic ones, such as starting a Pod with multiple containers or creating a Role with certain permissions, to other more complicated ones, such as creating a NetworkPolicy that restricts the traffic of a Pod in a certain way, and even a couple of questions that will really test your knowledge. An example of these questions was a cluster that had a node down and I had to identify the problem, without any type of clue.

As I said, the difficulty lies in how familiar you are with the tools that you’re going to use. For this reason, I want to highlight some of the advice that Fernando gives us in [his post]({{ site.baseurl }}/en/2020/04/28/examen-ckad){:target="_blank"}:

* Practice using the `kubectl` subcommands. Creating descriptors from `run` or `create <type> --dry-run=client -o yaml`, or using `explain` to understand the structure of a resource can save a lot of time.
* In case you’re not able to create these resources using `kubectl`, knowing how to navigate through the documentation and find the examples of the descriptors we need is also a good option. So, create bookmarks in your browser that take you directly to the areas of the documentation that you will use most.
* Personally, I used `alias k=kubectl` and it was great!
* Learn how to use the bash terminal and practice with its commands. The same with the editor that we are going to use (I used `vim`). Being effective in these areas will give us a lot of extra time to spend on more important tasks.

### Conclusion

I’m happy to have been able to obtain this certification, and to be able to become a recognized user by the CNCF. Most of the subject matter in the syllabus is easy to take in and with good preparation, I am sure that users who work with K8s on a day to day basis will be able to obtain this certification. It’s just a matter of practice.

I got a score of 87/100, so I'm assuming I messed on up one or two questions. I’m satisfied because I know that I’m capable of solving any of the exam exercises, which for me is the important thing: being able to understand the subject and apply the knowledge obtained to real-life cases. 

![Certification](/assets/images/2021-04-14-my-cka-exam-experience/certification.png){: .center }
<label style="text-align: center; display: block;">Certification</label>
