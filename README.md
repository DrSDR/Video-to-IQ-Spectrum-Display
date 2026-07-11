here are matlab and python scripts that read in a small length mp4 file.
and take an ifft of each frame of the video file.

then an iq float32 file is saved at the end.

one can then use gnu radio file source to read in file and send to sdr tx device.

need high bandwidth sdr for tx (hackrf,  pluto sdr,  bladerf,  usrp)

to see the spectrum, best to use sdr angel with a hackrf or usrp device,  need a fast fft update to see video spectrum.

the trick is to adjust the tx sample rate in gnu radio , until the image fools the eye in seeing a static dancing pumpkins.

see thegmr140 for videos of this demo.

Paul the sdr guy, is also making a video about this as well.

thanks for reading.

