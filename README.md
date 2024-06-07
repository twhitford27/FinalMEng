3 Programs are needed for the Live Frequency Logging:

 1.  The C program on the microcontroller to estimate the grid frequency and send it to a connected PC through serial communications. 

 2.   serial_freq_data_logger.py - Stores the data received from the serial communications port to the PC’s local storage as a CSV file. Two columns are in the output: Datetime and Frequency. 

 3.   grid_freq_live_graph_animation.py - Reads the CSV data and plots it to a Matplotlib graph, which automatically updates with any new data. Also pulls frequency data from the Elexon BMRS API and plots this on the same graph.

 Ensure the data logger is loaded and set to the correct COM port in order to produce data for the graph animation program.
