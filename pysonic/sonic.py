from ctypes import *
from ctypes import cdll, CDLL

class Sonic:
    '''
    type for work with Sonic from Python
    use .so for access to C functions
    give posible to change speed, pitch, rate...
    '''
    __obj: c_void_p
    __so: CDLL
    width: int

    def __init__(self, sampleRate: int, numChannels: int, sampleWidth: int) -> None:
        '''
        load SharedObject and create sonicStream object
        sampleWidth - width of sample in bytes (16bit = 2, 32bit = 4)
        '''
        so = cdll.LoadLibrary("libsonic.so", winmode=0)
        self.__so = so
        self.__obj = so.sonicCreateStream(sampleRate, numChannels)
        self.width = sampleWidth
        # ctypes BUG, float return must be hard set
        so.sonicGetSpeed.restype = c_float
        so.sonicGetPitch.restype = c_float
        so.sonicGetRate.restype = c_float
        so.sonicGetVolume.restype = c_float

    def __del__(self):
        self.__so.sonicDestroyStream(self.__obj)

    # public methods for work with wave streams
    def writebytes(self, samples: bytearray) -> int:
        '''
        simple write to stream from wave library
        '''
        numSamples = int(len(samples) / self.width)
        result = self.__so.sonicWriteShortToStream(self.__obj, samples, numSamples)
        return result

    def readbytes(self, numSamples: int) -> bytearray:
        '''
        simple read from stream for wave library
        '''
        w = self.width
        # create any type buffer
        dtype = (c_char) if (1 == w) else ((c_short) if (2 == w) else (c_float))
        arr = (dtype * numSamples)(0)
        
        result = 0
        match(w):
            case 1:
                result = self.__so.sonicWriteUnsignedCharToStream(self.__obj, arr, numSamples)
            case 2:
                result = self.__so.sonicReadShortFromStream(self.__obj, arr, numSamples)
            case 4:
                result = self.__so.sonicReadFloatFromStream(self.__obj, arr, numSamples)
        
        if(0 == result):
            return b''

        # read needed size of any type buffer
        res = (dtype * result)(0)
        for i in range(result):
            res[i] = arr[i]
        return bytearray(res)

    # Sonic.c stream write/read functions
    def sonicWriteFloatToStream(self, samples: list[float]) -> int:
        '''/* Use this to write floating point data to be speed up or down into the stream.
        Values must be between -1 and 1.  Return 0 if memory realloc failed,
        otherwise 1 */'''
        numSamples = len(samples)
        arr = (c_float * numSamples)(*samples)
        result = self.__so.sonicWriteFloatToStream(self.__obj, arr, numSamples)
        return result

    def sonicWriteShortToStream(self, samples: list[c_short]) -> int:
        '''/* Use this to write 16-bit data to be speed up or down into the stream.
        Return 0 if memory realloc failed, otherwise 1 */'''
        numSamples = len(samples)
        arr = (c_short * numSamples)(*samples)
        result = self.__so.sonicWriteShortToStream(self.__obj, arr, numSamples)
        return result

    def sonicWriteUnsignedCharToStream(self, samples: list[c_char]) -> int:
        '''/* Use this to write 8-bit unsigned data to be speed up or down into the stream.
        Return 0 if memory realloc failed, otherwise 1 */'''
        numSamples = len(samples)
        arr = (c_char * numSamples)(*samples)
        result = self.__so.sonicWriteUnsignedCharToStream(self.__obj, arr, numSamples)
        return result

    def sonicReadFloatFromStream(self, samples: list[float]) -> int:
        '''/* Use this to read floating point data out of the stream.  Sometimes no data
        will be available, and zero is returned, which is not an error condition. */'''
        numSamples = len(samples)
        arr = (c_float * numSamples)(0)
        result = self.__so.sonicReadFloatFromStream(self.__obj, arr, numSamples)
        for i in range(result):
            samples[i] = arr[i]
        return result

    def sonicReadShortFromStream(self, samples: list[c_short]) -> int:
        '''/* Use this to read 16-bit data out of the stream.  Sometimes no data will
        be available, and zero is returned, which is not an error condition. */'''
        numSamples = len(samples)
        arr = (c_short * numSamples)(0)
        result = self.__so.sonicReadShortFromStream(self.__obj, arr, numSamples)
        for i in range(result):
            samples[i] = arr[i]
        return result

    def sonicReadUnsignedCharFromStream(self, samples: list[c_char]) -> int:
        '''/* Use this to read 8-bit unsigned data out of the stream.  Sometimes no data
        will be available, and zero is returned, which is not an error condition. */
        '''
        numSamples = len(samples)
        arr = (c_char * numSamples)(0)
        result = self.__so.sonicReadUnsignedCharFromStream(self.__obj, arr, numSamples)
        for i in range(result):
            samples[i] = arr[i]
        return result

    def sonicFlushStream(self) -> int:
        '''/* Force the sonic stream to generate output using whatever data it currently
        has.  No extra delay will be added to the output, but flushing in the middle
        of words could introduce distortion. */
        '''
        return self.__so.sonicFlushStream(self.__obj)

    def sonicSamplesAvailable(self) -> int:
        '''/* Return the number of samples in the output buffer */'''
        return self.__so.sonicSamplesAvailable(self.__obj)
    
    # parametters getters/setters
    @property
    def Speed(self) -> c_float:
        '''/* Get the speed of the stream. */'''
        return self.__so.sonicGetSpeed(self.__obj)

    @Speed.setter
    def Speed(self, speed: float):
        '''/* Set the speed of the stream. */'''
        self.__so.sonicSetSpeed(self.__obj, c_float(speed))

    @property
    def Pitch(self) -> c_float :
        '''/* Get the pitch of the stream. */'''
        return self.__so.sonicGetPitch(self.__obj)
    
    @Pitch.setter
    def Pitch(self, pitch: float):
        '''/* Set the pitch of the stream. */'''
        self.__so.sonicSetPitch(self.__obj, c_float(pitch))
    
    @property
    def Rate(self) -> c_float :
        '''/* Get the rate of the stream. */'''
        return self.__so.sonicGetRate(self.__obj)
    
    @Rate.setter
    def Rate(self, rate: float):
        '''/* Set the rate of the stream. */'''
        self.__so.sonicSetRate(self.__obj, c_float(rate))
    
    @property
    def Volume(self) -> c_float :
        '''/* Get the scaling factor of the stream. */'''
        return self.__so.sonicGetVolume(self.__obj)
    
    @Volume.setter
    def Volume(self, volume: float):
        '''/* Set the scaling factor of the stream. */'''
        self.__so.sonicSetVolume(self.__obj, c_float(volume))

    @property
    def Quality(self) -> c_int :
        '''/* Get the quality setting. */'''
        return self.__so.sonicGetQuality(self.__obj)

    @Quality.setter
    def Quality(self, quality: int):
        '''/* Set the "quality".  Default 0 is virtually as good as 1, but very much
        * faster. */'''
        self.__so.sonicSetQuality(self.__obj, c_int(quality))
    
    @property
    def SampleRate(self) -> c_int :
        '''/* Get the sample rate of the stream. */'''
        return self.__so.sonicGetSampleRate(self.__obj)
    
    @SampleRate.setter
    def SampleRate(self, sampleRate: int):
        '''/* Set the sample rate of the stream.  This will drop any samples that have not
        * been read. */'''
        self.__so.sonicSetSampleRate(self.__obj, c_int(sampleRate))
    
    @property
    def NumChannels(self) -> c_int :
        '''/* Get the number of channels. */'''
        return self.__so.sonicGetNumChannels(self.__obj)
    
    @NumChannels.setter
    def NumChannels(self, numChannels: int):
        '''/* Set the number of channels.  This will drop any samples that have not been
        * read. */'''
        self.__so.sonicSetNumChannels(self.__obj, c_int(numChannels))



import wave
import os

def SonicReSpeedFiles(src_path: str, dst_path: str, speed: float = 1.0, pitch: float = 1.0) -> bool:
    '''
    just change speed, pitch of src file and write it to dst file
    '''
    src_exist = os.path.isfile(src_path)
    if(False == src_exist):
        return False

    wr : wave.Wave_read = wave.open(src_path, 'rb')
    framerate = wr.getframerate()
    nch = wr.getnchannels()
    width = wr.getsampwidth()

    sonic = Sonic(framerate, nch, width)
    sonic.Speed = speed
    sonic.Pitch = pitch

    ww : wave.Wave_write = wave.open(dst_path, 'wb')
    ww.setframerate(framerate)
    ww.setnchannels(nch)
    ww.setsampwidth(width)

    r_available = True 
    while (r_available):
        frames = wr.readframes(2048)
        if(0 == len(frames)):
            sonic.sonicFlushStream()
            r_available = False
        else:
            sonic.writebytes(frames)

        w_available = True
        while(w_available):
            buff = sonic.readbytes(2048)
            if(0 != len(buff)):
                ww.writeframesraw(buff)
            else:
                w_available = False

    wr.close()
    ww.close()

    return True
    
