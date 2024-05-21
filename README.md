# Image_Processing_Project
CSCI 0452 Final Project

## Exploring Object Detection & Tracking in Frequency Domain
#### Team Members: Henry, Zeyi, Sally


In our project, we explored object detection and tracking in the frequency domain. The idea of using frequency domain to track objects may seem counterintuitive, as in oberving an image in frequency domain, we lose any idea of localization. Indeed for or an ordinary object that contains no high frequency data, a fourier transform into frequency space is unlikely to help us track an object, since it's frequency data will blend in with that of the surrounding environment. High frequency patterns, however, stand out in frequency domain, and strongly influence the appearence of a log-shifted display of fourier transform magnitudes. Thus, in this project, we explore the idea of tracking high frequency patterns we call "stickers" in frequency domain, with the idea that we could apply the stickers to ordinary objects and then use frequecny domain to track those objects.


We have two major goals for this project:

1. Apply the concept of spectrograms to our 2-D images. In the case of this project, the concept of spectrograms allows us to partition our image in order to gain the location information we've lost by moving to frequency domain.
2. Use frequency space to track and detect our stickers.