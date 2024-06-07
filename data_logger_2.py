# Testing data_logger_4 with milliseconds

import serial
from datetime import datetime
import csv

# Get the current date & time for the file name
fileName_time = datetime.now().strftime("%d_%b_%Y_%Hh%Mm%Ss")

# Open a csv file and set it up to receive comma delimited input
logging = open(f'freq_{fileName_time}.csv', mode='w', newline='')
writer = csv.writer(logging, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)

# Write column titles in the CSV file
writer.writerow(["Date", "Time", "Frequency"])

# Open serial terminal
ser = serial.Serial('COM3', baudrate=115200)
ser.flushInput()

# Initialise global variables
old_time = "old time"
old_date = "old date"

try:
    while True:
        # Read in data from Serial and convert to string
        ser_bytes = ser.readline()
        decoded_bytes = (ser_bytes[0:len(ser_bytes) - 1].decode("UTF-8"))

        # Check if within the range
        freq_float = float(decoded_bytes)
        if (freq_float > 10) & (freq_float < 100):

            # Get current date & time
            c = datetime.now()
            old_time = c.strftime('%H:%M:%S:%f')[:-4]
            old_date = c.strftime('%d %b %Y')
            mean_f_str = str(round(freq_float, 3))

            # Write received data to CSV file
            writer.writerow([old_date, old_time, mean_f_str])

            # Print values for monitoring
            print(old_date)
            print(old_time)
            print(mean_f_str)

        else:
            print("not within range")

except KeyboardInterrupt:
    # Close port, CSV file, and txt file to exit
    ser.close()
    logging.close()
    print("logging finished")
