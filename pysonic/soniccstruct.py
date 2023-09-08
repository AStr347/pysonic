from ctypes import *

class sonicStreamStruct(Structure):
    '''
    class for acces to C sonicStream structure
    '''
    _fields_ = [("inputBuffer", c_void_p),#short*
                ("outputBuffer", c_void_p),#short*
                ("pitchBuffer", c_void_p),#short*
                ("downSampleBuffer", c_void_p),#short*
                ("userData", c_void_p),#void*
                ("speed", c_float),
                ("volume", c_float),
                ("pitch", c_float),
                ("rate", c_float),
                ("samplePeriod", c_float),
                ("inputPlayTime", c_float),
                ("timeError", c_float ),
                ("oldRatePosition", c_int),
                ("newRatePosition", c_int),
                ("quality", c_int),
                ("numChannels", c_int),
                ("inputBufferSize", c_int),
                ("pitchBufferSize", c_int),
                ("outputBufferSize", c_int),
                ("numInputSamples", c_int),
                ("numOutputSamples", c_int),
                ("numPitchSamples", c_int),
                ("minPeriod", c_int),
                ("maxPeriod", c_int),
                ("maxRequired", c_int),
                ("remainingInputToCopy", c_int),
                ("sampleRate", c_int),
                ("prevPeriod", c_int),
                ("prevMinDiff", c_int)]
