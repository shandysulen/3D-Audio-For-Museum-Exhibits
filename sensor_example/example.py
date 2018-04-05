from marvelmind import MarvelmindHedge
from time import sleep
import sys


def main():
    hedge = MarvelmindHedge(tty="/dev/tty.usbmodem1421")  # create MarvelmindHedge thread
    hedge.start()  # start thread
    iterations = 100  # print location info for 100 iterations
    while iterations > 0:
        """
        valuesUltrasoundPosition - buffer of US position measures
        valuesImuRawData - buffer of IMU raw measures (accelerometer, gyroscope, compass)
        valuesImuData - buffer of IMU and US based measures 
        (position, angular position (quaternion), velocities, accelerations) [x, y, z, qw, qx, qy, qz, vx, vy, vz, ax, ay, az, timestamp]
        
        valuesImuData is not working currently, maybe the packet has not been supported yet. But you do can get the gyro data 
        through valuesImuRawData, and the position data from print_position method. Go through to marvelmind module,
        you will find the valuesUltrasoundPosition list holds the position. e.g. p[0] for beacon id, p[1] for x, p[2] for y, p[3] for z. You should play with them and try to get more location information. 
        """
        try:
            sleep(1)
            print(hedge.valuesImuRawData)  # print gyro data
            hedge.print_position()
            # I will show you the detail information inside the print_position() method
            # you can get the x, y, z location here
            # you should handle the errors, the following example may having errors since it reads the raw information
            # print("Hedge {:d}: X: {:d} m, Y: {:d} m, Z: {:d} m at time T: {:.2f}"
            #       .format(hedge.valuesUltrasoundPosition[0],
            #               hedge.valuesUltrasoundPosition[1],
            #               hedge.valuesUltrasoundPosition[2],
            #               hedge.valuesUltrasoundPosition[3]))
            # print(hedge.valuesImuData) # not working currently
        except KeyboardInterrupt:
            hedge.stop()  # stop and close serial port
            sys.exit()

        iterations -= 1


main()
