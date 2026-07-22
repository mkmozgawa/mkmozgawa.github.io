---
title: "hub.github.com, or how I have to do one click fewer"
date: 2019-07-08 10:00:00 +0000
categories:
  - Devops
tags:
  - Devops
  - TIL
---

HN turns out to be useful from time to time. During the weekend I came across [Hub](https://github.com/github/hub/), a project by GitHub which allows to navigate some of the features of GitHub from the command line level.

Since the workflow of this blog involves pushing to a branch other than master any time I have to do even the smallest of changes (and then putting up a PR and high-fiving myself ;)) it's always a welcome change when I can manage with one click fewer. I've changed my post-commit hook for the project from

`pelican content -o output -s pelicanconf.py && ghp-import output && git push origin gh-pages`

to

`pelican content -o output -s pelicanconf.py && ghp-import output && git push origin gh-pages && hub pull-request --force -b master -h gh-pages -m "Personal site update"`

and can now enjoy just clicking the url and hitting _Merge_. If you can see this post it means it works!

And yes, I know that opening pull requests with the same title every time isn't ideal...
