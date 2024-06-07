## serial_freq_data_logger.py
## Nicholas Fernandes + Bessam Saleh MEng Team 3 2023-2024
# Writes the received serial data to a file on disk
# PLEASE ENSURE THE CORRECT COM PORT IS USED, OR AN ERROR WILL THROW.

# Works for CSV and txt files with averaging over a second
# Works for plotting a graph at the end
# Works with file naming
# CSV files work in Excel

import serial
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import os

# Get the current date & time for the file name
fileName_time = datetime.now().strftime("%d_%b_%Y_%Hh%Mm%Ss")

data_folder_path = 'serial_received_data'
data_file_path = os.path.join(data_folder_path, 'freq_' + fileName_time + '.csv')

if not os.path.exists(data_folder_path):
    os.mkdir(data_folder_path)

# Change filename to make it easier to integrate for demo
fileName_time = 'serial_received_data.csv'

# Open a csv file and set it up to receive comma delimited input
with open(fileName_time, mode='w', newline='') as f:
    writer = csv.writer(f, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
    # Write column titles in the CSV file
    writer.writerow(["Datetime", "Frequency"])


# Open a txt file
#dataFile = open(f'freq_{fileName_time}.txt', 'w', encoding='UTF-8')

# Open serial terminal - COM port may need to be changed
ser = serial.Serial('COM5', baudrate=115200)
ser.flushInput()

# Initialise global variables
counter = 0
mean_f = 0.0
new_second = 0
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
            current_second = c.strftime('%S')
            # Set new_second for the 1st iteration
            if counter == 0:
                new_second = float(current_second)

            # Check if its during the same second
            if new_second == float(current_second):
                mean_f = mean_f + float(decoded_bytes)
                counter = counter + 1
                old_datetime = c.isoformat(timespec='seconds')
            else:
                # Calculate the mean over the second
                mean_f = mean_f/counter
                mean_f_str = str(mean_f)

                # Write received data to CSV file
                with open(fileName_time, mode='a', newline='') as f:
                    writer = csv.writer(f, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
                    writer.writerow([old_datetime, mean_f_str])

                # Write received data to txt file
                #dataFile.write(old_date)
                #dataFile.write(" ")
                #dataFile.write(old_time)
                #dataFile.write(" frequency = ")
                #dataFile.write(mean_f_str)
                #dataFile.write("\n")

                # Print values for monitoring
                print(old_datetime)
                print(mean_f_str)
                #print(counter)
                #print(mean_f)

                # Start new mean
                counter = 1
                new_second = float(current_second)
                mean_f = freq_float
        else:
            print("not within range")

except KeyboardInterrupt:
    # Close port, CSV file, and txt file to exit
    ser.close()
    #logging.close()
    #dataFile.close()
    print("logging finished")

    # Plot the graph
    #x = []
    #y = []
    #for line in open(f'freq_{fileName_time}.txt', 'r'):
    #    lines = [i for i in line.split()]
    #    x.append(lines[3])
    #    y.append(float(lines[6]))

    #plt.title(f'Frequency Data for "freq_{fileName_time}"')
    #plt.xlabel('Time')
    #plt.ylabel('Frequency')
    #plt.yticks(y)
    #plt.plot(x, y, marker='o', c='g')

    #plt.show()
