

import math
import pyaudio
import struct
from matplotlib import pyplot as plt
import numpy as np

plt.ion()           # Turn on interactive mode so plot gets updated

WIDTH     = 2         # bytes per sample
CHANNELS  = 1         # mono
RATE      = 8000     # Sampling rate (samples/second)
BLOCKSIZE = 1024      # length of block (samples)
DURATION  = 8        # Duration (seconds)
freq=650
op_blk = BLOCKSIZE * [0]
NumBlocks = int( DURATION * RATE / BLOCKSIZE )


print('BLOCKSIZE =', BLOCKSIZE)
print('NumBlocks =', NumBlocks)
print('Running for ', DURATION, 'seconds...')

DBscale = False
# DBscale = True
#---------------------======
# Initialize plot window:
#plt.figure(1)
fig = plt.figure(1)
fig.subplots_adjust(hspace=1) #space between plots

plt.subplot(211)
if DBscale:
    plt.ylim(0, 150)
else:
    plt.ylim(0, 20*RATE)
# Frequency axis (Hz)
# plt.xlim(0, 0.5*RATE)         # set x-axis limits
plt.xlim(0, 2000) 
plt.xlabel('Frequency (Hz)')
f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)
line, = plt.plot([], [], color = 'blue')  # Create empty line
line.set_xdata(f)                         # x-data of plot (frequency)
plt.title('input signal')


plt.subplot(212)
if DBscale:
    plt.ylim(0, 150)
else:
    plt.ylim(0, 20*RATE)
# Frequency axis (Hz)
# plt.xlim(0, 0.5*RATE)         # set x-axis limits
plt.xlim(0, 2000)   
plt.xlabel('Frequency (Hz)')
f = RATE/BLOCKSIZE * np.arange(0, BLOCKSIZE)
line_, = plt.plot([], [], color='red')  # Create empty line
line_.set_xdata(f)  # x-data of plot (frequency)
plt.title('output AM signal')
#--------------------------


#For AM of input we initialize the phase
om = 2*math.pi*freq/RATE
theta = 0#initialize the theta value to 0


# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(
    format    = PA_FORMAT,
    channels  = CHANNELS,
    rate      = RATE,
    input     = True,
    output    = True)#set to true to demonstrate the real time plots


for i in range(0, NumBlocks):
    input_bytes = stream.read(BLOCKSIZE)                     # Read audio input stream
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert
    X = np.fft.fft(input_tuple)

    # Update y-data of plot
    if DBscale:
        line.set_ydata(20 * np.log10(np.abs(X)))
    else:
        line.set_ydata(np.abs(X))

    for n in range(0, BLOCKSIZE):
        # For AM of the input signal :
        theta = theta + om
        op_blk[n] = int( input_tuple[n] * math.cos(theta) ) #equation for AM
    while theta > math.pi:
        theta = theta - 2*math.pi

        
    X = np.fft.fft(op_blk) #computing FFT of the AM output

    output_bytes = struct.pack('h' *BLOCKSIZE, *op_blk)

    if DBscale:#Plot line for AM
        line_.set_ydata(20 * np.log10(abs(X)))
    else:
        line_.set_ydata(abs(X))

    plt.pause(0.001)
    plt.draw()

    # plt.draw()
    stream.write(output_bytes)
fig.savefig("Comparison of input and AM output FFT.pdf")
plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')
