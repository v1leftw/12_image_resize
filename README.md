# Image Resizer

Script resizes image that has been input by user.
Image can be resized by changing it's height, width or just by scaling it's size.
Available options:
```
-path  - path to user image
-height  - height of output image (can be used without width, heigth will be changed proprtionally)
-width  - width of output image (can be used without hegth, width will be changed proprtionally)
-scale  - scale's coefficient of output image (can not be used with height and width at once)
-output - path to output image. If not specified image will be saved in original path to given image
```

heigth, width, scale must be integer

# Quickstart
Examples of script launch on Linux, Python 3.5

```
$ python image_resize.py -path files/capture.PNG -scale 2
Image saved. Path to file: files/capture__750x1114.PNG
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
