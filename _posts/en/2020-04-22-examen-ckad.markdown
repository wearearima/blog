---
layout: post
title:  "How I prepared and passed the Certified Kubernetes Application Developer (CKAD) exam"
date:   2020-04-28 6:00:00
author: fernando
lang: en
categories: certifications
tags: certifications, exams, Kubernetes, CNCF, CKAD, CKA
header-image:	2020-04-22-examen-ckad/header-image.jpg
---

In this post I’m going to explain a bit about my experience and how I prepared for and passed the Certified Kubernetes Application Developer (CKAD) exam.

[The Linux Foundation](https://www.linuxfoundation.org/) and [Cloud Native Computing Foundation](https://www.cncf.io/)
offer two variants in the Kubernetes certification, CKAD and CKA. In a nutshell:

- [CKAD](https://www.cncf.io/certification/ckad/) is designed for software developers who wish to develop and implement their applications in Kubernetes.

- [CKA](https://www.cncf.io/certification/cka/) is designed for system administrators who manage Kubernetes clusters.

In general, CKA covers a broader agenda than CKAD. You can find information on the similarities and differences between the two exams [here](https://medium.com/faun/cka-vs-ckad-1dd45527505).
![CKAD / CKA](/assets/images/2020-04-22-examen-ckad/ckad-cka.png)

As I mentioned, CKAD is one of two programs designed by the CNCF and The Linux Foundation to certify users so that they can "design, build, configure, and expose cloud native applications for Kubernetes".

If you are a developer who uses Kubernetes-centred infrastructure on a daily basis, CKAD is a great method to measure your skills against the latest industry standards.

I should point out that Kubernetes is a tool that I had previously worked with and therefore I was familiar with most of the concepts.

## Why should you take this exam?

Despite the fact that in [ARIMA](https://arima.eu/) we are not generally in favor of measuring the knowledge of people or organizations based on the certificates they may possess, there are occasions when having a certificate issued by a third party can help as a cover letter when offering solutions that revolve around a tool such as Kubernetes. And even more so when it is from an organization of the prestige of the CNCF and a certificate that has a certain degree of difficulty such as the CKAD.

## Requirements

There are no official requirements for this exam, but I recommend having practical experience in **Docker** and **Linux**.

By constantly working with containers, we should understand what a Docker image is, how to run containers, extract and work with images, etc.

Linux is also essential for this exam, since, being 100% practical, you need to be quite competent when editing files, changing permissions, executing commands, etc.

## About the exam

This is a **totally practical** exam, it doesn't have multiple choice questions.

You will be given a set of problems that you have to solve from a command line displayed in a web application and it is expected that it will take approximately two hours to complete it.

You must solve **19 questions** in **2 hours** and each question has a different value, from **2% to 13%**, but most of the questions are between **5% and 8%**. The score does not correspond to the level of difficulty.

**To pass the exam it is necessary to get at least 66%.** In my case, I got 88% at the first attempt and I had just enough time to finish the 19 questions, even though I was quite fast in solving the problems. **Timing is everything in this exam.**

The price of the exam is **$ 300 USD** and you have another free attempt if you fail. The exam includes questions on the following topics:

- Core Concepts (13%)
- Configuration (18%)
- Multi-Container Pods (10%)
- Observability (18%)
- Pod Design (20%)
- Services & Networking (13%)
- State Persistence (8%)

In the exam, you are provided with **4 clusters** which you will have to work through to complete all the exercises. The operating system they use is **Ubuntu 16.04**.

![Clusters](/assets/images/2020-04-22-examen-ckad/clusters.png)

At the beginning of each question, you are given the command that you must run to go to the specific cluster. For example:

    $ kubectl config use-context k8s

### Types of question

The questions range from relatively short questions, such as those on the [Dgkanatsios CKAD exercises](https://github.com/dgkanatsios/CKAD-exercises) list, to longer questions of about 6 or 7 lines.

You need to feel comfortable creating *pods*, *developments*, *jobs*, *cronjobs*, *services*, etc. There will also be *rolling updates* and *rollbacks* exercises. Basically, they cover all the topics that are in the exam.

### Official exam resources

These are the resources that the CNCF itself makes available to students:

- Certified Kubernetes Application Developer: https://www.cncf.io/certification/ckad/
- Curriculum Overview: https://github.com/cncf/curriculum
- Candidate Handbook: https://training.linuxfoundation.org/go/cka-ckad-candidate-handbook
- Exam Tips: http://training.linuxfoundation.org/go//Important-Tips-CKA-CKAD
- FAQ: http://training.linuxfoundation.org/go/cka-ckad-faq

### Where to register

First you must register at **The Linux Foundation** from [here](https://identity.linuxfoundation.org/user/login). Then, you can register for the exam from [here](https://identity.linuxfoundation.org/pid/813), where the following screen will be displayed:

![Checkout](/assets/images/2020-04-22-examen-ckad/checkout.PNG)

Once you have paid for the exam, you will receive an email and you can log in from [this](https://training.cncf.io/portal) link to the portal where you must follow a series of steps before programming and taking the exam, such as checking your machine requirements, reading important information about the exam, etc.

![Checkout](/assets/images/2020-04-22-examen-ckad/cncf-checklist.PNG)

## How to prepare for the exam

### Courses

As I said before, in order to prepare for the exam, I took the following two [Udemy](https://www.udemy.com/) courses:

1. [Kubernetes for the Absolute Beginners - Hands-on](https://www.udemy.com/course/learn-kubernetes/)
2. [Kubernetes Certified Application Developer (CKAD) with Tests](https://www.udemy.com/course/certified-kubernetes-application-developer/)

I did the first, although I already had basic knowledge of Kubernetes, to check that my base in Kubernetes was sufficient. I learned practically nothing new in that course, so if you have already worked with Kubernetes, I would go directly to the second. In addition, in the second course, they review the most important concepts that are given in the first.

The second course gave me much more, since it is focused on the exam itself, and the practical exercises are very good. The test section is especially good (similar to the one you will find in the exam) and it really helped me to improve the speed with which I solved the problems.

### Practice exercises

Basically, these were the resources that I used to prepare for the exam, as well as those of the course itself. Some I did in full 2 or 3 times, as in the end, you must be able to read the question and without hesitation, know how to solve the problem, since, as I repeat, time is everything in this exam.

- https://github.com/bmuschko/ckad-prep
- https://github.com/dgkanatsios/CKAD-exercises
- https://codeburst.io/kubernetes-ckad-weekly-challenges-overview-and-tips-7282b36a2681

In total, between taking the two courses, studying and doing the practical exercises, it took me around **90hours** to pass the exam. I started preparing for it on March 30th and took the exam on April 15th.

## Useful tips and tricks

 - **Be fast and accurate. It’s a very long exam and with little time.** Don’t expect to be able to calmly answer all the questions in 120 minutes. There’s no time, not even to review your work.

    What I did in the exam was, if I saw any questions that were very long and had a value <3%, I left them until the end and returned to them after completing most of the other questions. If you get stuck, skip the question, you have to answer the maximum number of questions possible.

 - When creating resources in the cluster, **don't write YAML files from the beginning**. Use the arguments ``-o yaml --dry-run`` whenever you can. If you still don't know what it is, you’re a bit slow to learn it!

 - If you don't remember some syntax when writing YAML files, use ``kubectl explain`` instead of the documentation. It’s faster and has good support material. I recommend you practice it so it becomes automatic.

    For example, if you don't remember the ``livenessProbe`` options for the container, just type ``kubectl explain pod.spec.containers.livenessProbe`` and it will give you all the options with good guidance.

 - Always use aliases, both in your training and in the exam, they save you time. These were the ones that I used in the exam:

        alias k=kubectl
        alias ks='kubectl config set-context --current --namespace '

 - **Delete Kubernetes objects quickly**. Deleting objects in Kubernetes sometimes takes up to 30 seconds because it has a grace period. In the exam you are not interested in doing it, so it is best that you always force deletion of the resource.

        $ kubectl delete pod nginx --grace-period=0 --force

 - **Make sure you are in the right context and namespace**. You are going to have to constantly change context and namespace in the exam (I lost count how many times I did it), but it’s very important to make sure that you are always in the correct cluster and namespace.

7. **Use the browser bookmarks!** You are only allowed to have one extra tab to that of the exam with the Kubernetes material, but they do allow bookmarks. I’m putting [here](/assets/extra/2020-04-22-examen-ckad/CKAD-bookmarks.html) the bookmarks that I created and used in the exam, which are direct links to examples that will help you solve the problems faster.

    ![Marcadores](/assets/images/2020-04-22-examen-ckad/marcadores.png) 

8. **Remember to click the "End exam" button!** I spent five minutes without touching the keyboard wondering why it hadn’t ended yet until the exam supervisor reminded me. The button is hidden in the exam settings menu.

9. Before starting the exam, you must **remove everything you have on the table: desk lamp, drinks, food, etc.**, then you must show your ID or passport, your room and desk. I used a laptop with an external monitor, so make sure your cables are long enough or disconnect them completely.

10. Never cover your mouth with your hand or whisper because the examiner will reprimand you, which, at least for me, was distracting.

11. Use the same version of **Kubectl** and **Kubernetes** as the exam. In my case it was version 1.17. When using ``Minikube for Mac OS`` locally, changing the version of Kubernetes is very easy:

        minikube start --kubernetes-version v1.17.0

12. The **use of multiple monitors** is also allowed. I had the Kubernetes documentation on one monitor and the exam on the other. It was very helpful to have both screens at a glance. Of course, you will be asked in the exam to share both screens.

13. **Practice**. Just because it’s the last tip, doesn’t mean it’s the least important. Practice as much as you can. In the exam you’ll be glad you did.

## Results

Unfortunately, you don’t get the results immediately, it takes up to 36 hours. You don't know how long the wait was! But finally it came and here is the long-awaited certificate.

![Certificado](/assets/images/2020-04-22-examen-ckad/Certificate.PNG)

## Conclusion

I’m not going to kid you, this is not an easy exam. At first it appears complicated, but as you practice, you see the light. You have to practice a lot, be comfortable with the ``kubectl`` commands, editing files with ``Vim`` or ``Nano``, know how to get around the K8s documentation, etc.

I found it a very good way to complete my knowledge of Kubernetes and keep up to date with what the platform is offering.

Good luck with your CKAD exam!


