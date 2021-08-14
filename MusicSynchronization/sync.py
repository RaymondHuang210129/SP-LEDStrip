#!/usr/bin/env python3

import argparse
import queue
import sys

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd

import socket
import time
import os


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
parser.add_argument(
    '-f', '--fft', action='store_true', help='show fft chart')
parser.add_argument(
    '-m', '--mfcc', action='store_true', help='show mfcc chart')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()

def sendColor(brightness, change=False):
    global colorIdx
    colors = [(255, 255, 255), (0, 255, 255), (255, 0, 255), 
        (255, 255, 0), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
    color = (int(colors[colorIdx][0] * brightness),
            int(colors[colorIdx][1] * brightness),
            int(colors[colorIdx][2] * brightness))
    data = '#' + '%02x%02x%02x' % color

    addr = ('192.168.1.33', 8700)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    data = bytes(data, 'utf-8')
    
    s.sendto(data, addr)
    s.close()

    if change:
        if colorIdx == 6:
            colorIdx = 0
        else:
            colorIdx += 1

def get_volume():
    output = os.popen('amixer -D pulse sget Master | grep -m1 -o "\\w*%"').read()
    try:
        volume = int(output[:-2])
        if volume == 0:
            return 1
        else:
            return volume / 100
    except Exception as e:
        print(output)
        print(e)
        return 1



def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    q.put(indata[::args.downsample, mapping])


def update_plot(frame):
    """This is called by matplotlib for each plot update.
    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.
    """
    global plotdata
    global args
    global pulse
    global lastPulseTime
    global volume

    minThreshold = 20.0

    while True:
        try:
            data = q.get_nowait()
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data

    fftdata = np.fft.fft2(plotdata)
    fftdata[25:-25] = fftdata[25:-25] * 0.02
    fftNormalizedData = np.multiply(np.power(abs(fftdata), 0.7), 0.1)
    bassEmphasizedData = np.fft.ifft2(fftdata)
    maxValinCurrentFrame = np.amax(abs(bassEmphasizedData)) * 200 / pow(volume, 2)
    if maxValinCurrentFrame / pulse > 1.15:
        pulse = maxValinCurrentFrame
        if time.time() - lastPulseTime > 0.15:
            lastPulseTime = time.time()
            sendColor(1.0, change=True)
    else:
        #sendColor(1.0)
        pulse = max(max(0.92 * (pulse - minThreshold) + minThreshold, maxValinCurrentFrame), 
            minThreshold)

    volume = get_volume()

    for column, line in enumerate(lines):
        if args.fft == True:
            line.set_ydata(fftNormalizedData[:, column])
        elif args.mfcc == True:
            pass
        else:
            #line.set_ydata(plotdata[:, column])
            line.set_ydata(bassEmphasizedData[:, column])
    return lines


try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

    pulse = 0.1
    colorIdx = 0
    lastPulseTime = time.time()
    volume = 1.0

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)
    if len(args.channels) > 1:
        ax.legend(['channel {}'.format(c) for c in args.channels],
                  loc='lower left', ncol=len(args.channels))
    ax.axis((0, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom=False, top=False, labelbottom=False,
                   right=False, left=False, labelleft=False)
    fig.tight_layout(pad=0)

    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    with stream:
        plt.show()
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))


