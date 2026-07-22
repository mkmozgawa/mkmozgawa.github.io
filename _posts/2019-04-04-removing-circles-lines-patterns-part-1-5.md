---
title: "Removing circles, lines, and other patterns with OpenCV and Python, part 1 & 1/2"
date: 2019-04-04 10:00:00 +0000
categories:
  - OpenCV
tags:
  - Python
  - OpenCV
---

Why 1.5? Because I'm not addressing the issue of the overlay text and instead present a small improvement on removing the thick outlines.

```python
import matplotlib.pyplot as plt
import numpy as np
import cv2
%matplotlib inline

# a little helper function to display our image in a bigger plot
def display_img(image):
    fig = plt.figure(figsize=(20,16))
    ax = fig.add_subplot(111)
    ax.imshow(image, cmap="gray")
```

```python
img = cv2.imread('obfuscated.jpg', 0) #read in as a grayscale image
```

```python
display_img(img)
```

Note that in the previous post I found out that a naive removal method and the Hough transform worked better than the Suzuki algorithm for contour location. The method I'm about to present should work regardless of the methods applied previously to the image, but it comes at a price. Let's say I go with the naive method:

```python
img_med = cv2.medianBlur(img, ksize=15)
```

```python
ret, th = cv2.threshold(img_med, 80, 255, cv2.THRESH_BINARY)
```

```python
display_img(th)
```

The secret here is to erode the image using a wide enough kernel (3x3 in our case). Normally [erosion](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html) would make the outlines thinner, but because we're working with a white background and black foreground it actually makes the outlines thicker. (Which is something we need since by first blurring and thresholding the image to extract the contours we have "watered down" the outlines significantly, leaving some of their traces behind after switching their pixels from black to white.)

```python
kernel = np.ones((3,3),np.uint8)
eroded_img = cv2.erode(th,kernel,iterations=2)
display_img(eroded_img)
```

```python
img_dest = img.copy()
img_dest[eroded_img == 0] = 255
```

```python
display_img(img_dest)
```

And voilà! The geometric outlines are by and large gone. Unfortunately, this removes some of the letters as well (since they were covered by the outlines) but you can't have everything ¯\_(ツ)_/¯
