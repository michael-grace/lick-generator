import wave
import numpy
import pygame

def lick_maths(start_freq, tempo):
    calc_tempo = tempo / 30
    return [
        (start_freq, 1.0/calc_tempo),
        (start_freq*1.125, 1.0/calc_tempo),
        (start_freq*1.2, 1.0/calc_tempo),
        (start_freq*(4/3), 1.0/calc_tempo),
        (start_freq*1.125, 2.0/calc_tempo),
        (start_freq*(8/9), 1.0/calc_tempo),
        (start_freq, 5.0/calc_tempo)
    ]

sfile = wave.open('lick.wav', 'w')
sfile.setframerate(48000)
sfile.setnchannels(2)
sfile.setsampwidth(2)
pygame.init()
pygame.mixer.init(frequency=48000, channels=2)

for note in lick_maths(500, 300):
    ncycles = note[1] * note[0]
    spc = int((48000 * note[1]) / ncycles)

    sine = numpy.arange(0, 2*numpy.pi, (2*numpy.pi)/spc)
    sine = numpy.sin(sine)
    sine *= 8000
    sine = numpy.hstack(int(ncycles)*list(sine))
    sine = numpy.repeat(sine, 2, axis=0)
    sine.reshape(len(sine)//2,2)

    snd = pygame.mixer.Sound(sine.astype('int16'))
    sfile.writeframesraw(snd.get_raw())

sfile.close()