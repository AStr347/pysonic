from pysonic import SonicReSpeedFiles
import time

def main():
    print("sonic talking.wav -> talking_speed18.wav")
    # read part of wave file like stream
    before = time.time_ns()
    SonicReSpeedFiles('talking.wav', 'talking_speed30_08.wav', 3.0, 0.8)
    after = time.time_ns()
    dif = after - before
    print(f'sec: {dif/1000000000}\tns: {dif}')
    

if '__main__' == __name__:
    main()


