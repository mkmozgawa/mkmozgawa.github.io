Title: Setting up shared folders in VirtualBox on Windows, or all the issues you can run into in a single afternoon
Date: 2018-09-30 20:00
Modified: 2018-09-30 20:00
Category: DevOps
Tags: devops, virtualbox
Slug: virtualbox-shared-folders
Authors: Magda Mozgawa
Summary: Setting up shared folders in VirtualBox on Windows, or all the issues you can run into in a single afternoon

### A little background

This year for Rails Girls Poznan we wanted to have VirtualBox-ready images that would (a) be lightweight enough (both size- and resources-wise) for non-developer computers, (b) be user-friendly (so if someone wanted to do something on their machine, they wouldn't feel completely lost, i.e. we needed an OS with a GUI), (c) most importantly, include the latest Ruby and Rails as well as other useful gimmicks (image magick etc), (d) support shared folders.

I went for [Lubuntu](https://lubuntu.net/) which, if you're not at all familiar with the Linux underworld, is a flavour of Ubuntu (tells you a lot!) which is more lightweight e.g. due to its minimal desktop LXDE (fascinating, huh?). If you don't know Ubuntu, then let's say it's a Debian-based distribution (duh).

The point is, its hardware requirements are pretty low. The target ova image weighed around 2.5GB (to put it into some perspective, the Windows ova files are 3x - 4x times this size), required a single CPU core and 1024MB RAM, and was beautifully user-friendly (or at least as user-friendly as Linux systems may be).

There was, however, one issue: setting up the shared folders. What a friggin' pain in the ass. In the end it worked, mostly because I spent several hours on research because, at that point, I felt too personally invested in the project to export an image without the shared folders working.

To make like easier for anyone googling "How to make shared folders work in Virtualbox on Windows with a Linux guest?", I present a few links from around the internet. I mean, I don't see the point in writing a full-blown guide, because the parts are already there, but let's say I'm going to present to you the most unfortunate scenario possible, and may the odds be in your favour.

### Potential issues 

__I went with "Install the system" but I got an error with a meditating guy and something. What's wrong?__

A plethora of things might have gone awry, but if you have an average- or better performing computer, you shouldn't be running into [issues with memory size](http://www.fixedbyvonnie.com/2014/09/heck-virtualbox-guru-meditation-error/#.W7Eb5xSxU5l). There is, however, one pesky error that I wasted about 30 minutes on: my Thinkpad's default BIOS settings. Turns out I had virtualization turned off in my computer. When I finally discovered what was wrong that was a [fairly easy fix](https://support.lenovo.com/pl/en/solutions/ht500006) (as long as you don't mention the fact that it's bloody hard to get into my Thinkpad's BIOS settings). Depending on your computer this might be an issue with yours as well. Just look in the logs (...\VirtualBox VMs\<Your Box Name>\Logs\VBox.log) and google (or duck duck go) it.

__Whenever I install rvm and restart the machine, rvm is gone. Why?__

I strongly suggest using rbenv over rvm as shown in [this tutorial](https://gorails.com/setup/ubuntu/18.04). That's what I did, at least.

But if you really want that rvm, make sure [you're including it in your PATH](https://stackoverflow.com/questions/28224408/adding-rvm-to-path-ubuntu).

__So if I have an app running on the guest machine on localhost:3000 there, why can't I see it in the browser on the host machine.__

Mainly because they are too separate machines ¯\_(ツ)_/¯ _but don't worry, we can make do, and easily. What we need to figure out is the IP address of your guest machine and to do some port-mapping magic. By default, the IP of the host machine on VirtualBox is set to 10.0.2.15, but there's a slight change something is different on your host, so open up the terminal and type `ifconfig`. (At that point, it may say sth like "I don't recognize this message, try downloading package nettoolssomething. Install the package and then retry with ifconfig.)
It will probably give you more data than you need, but we're looking for the `inet` value. Write it down. Next, turn off the machine, right-click it in VirtualBox, and choose Settings. Once you're there, choose Network, and inspect (most likely) Adapter 1, the one using NAT. Click Advanced.

The option "Port forwarding" is what you're interested in. Yours will at first be empty, but you can easily add new rules to make them look like this: [Port Forwarding Rules](https://i.imgur.com/jTAsWH2.png) Once you've saved your changes, launched the machine back, and started your app, you can go to http://localhost:port on your host machine and it will show you the app running on the guest machine.

__Can I ssh into that machine?__

I thought you'd never ask! Yes you can, and it's really sick in Windows. Windows 10 apparently has ssh (haven't tested it out, though) but most Windows folk know Putty. It has a GUI which I won't go into the details of, however setting up VirtualBox to work with ssh on Windows is [pure devil's work](https://unix.stackexchange.com/questions/145997/trying-to-ssh-to-local-vm-ubuntu-with-putty).

Basically:
1. Either change the adapter from NAT to host-only (meaning the guest machine won't have access to the Internet) or enable Adapter 2 and set it to host-only.
2. Change the forwarding rules on the respective adapter to map your host's whatever port you want to use (I went for 3022) to the guest's port 22.
3. Put that stuff into Putty and pray.

_Fun fact: if you disable Adapter 2 without changing the option "host-only" to "not connected" and later try to import this image on VirtualBox for Linux, it won't work. You have to disconnect the adapter before disabling it. On Windows, however, it works fine. Hell!_

__Can I have my shared folder now?__

Yes, and no. If you have a nicely working Internet connection you download Guest Additions (the ones available in VirtualBox by default _do not_ work), like described [here](https://askubuntu.com/questions/22743/how-do-i-install-guest-additions-in-a-virtualbox-vm). However, if you (a) like living dangerously, (b) like weird hacks, (c) cannot be bothered to download Guest Additions you can winscp into your machine and copy the GuestAdditionsISO from the VirtualBox directory (where you installed it) onto the machine and then mount it there.

__You've run into all these issues while setting up shared folders?__

Yes, and probably even more I don't even remember. VirtualBox is glorious (╯°□°）╯︵ ┻━┻
