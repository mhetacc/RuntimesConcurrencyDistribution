import matplotlib.pyplot as plt
import datetime
#from pathlib import Path


def read_log(file_path):
    timestamps = []
    fps_values = []

    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(";")
            time_part = float(parts[0].split(":")[1])
            fps_part = int(parts[1].split(":")[1])
            
            timestamps.append(datetime.datetime.fromtimestamp(time_part))  # Convert timestamp to datetime
            fps_values.append(fps_part)

    return timestamps, fps_values


# Read data from two log files
timestamps1, fps_values1 = read_log("POCs/performance_eval/logs/baseline_100.log")  # First dataset
timestamps2, fps_values2 = read_log("POCs/performance_eval/logs/baseline_1000.log")  # Second dataset


# Create plot surface
plt.figure(figsize=(10, 5))

# plot datasets, color can be '#FF5733' or a RGB tuple (1, 0, 0)
plt.plot(timestamps1, fps_values1, marker='o', linestyle='-', color='red', label='FPS - Dataset 1')

# Plot the second dataset with a different color
plt.plot(timestamps2, fps_values2, marker='s', linestyle='-', color='blue', label='FPS - Dataset 2')

# Formatting the plot
plt.xlabel('Elapsed Seconds')
plt.ylabel('FPS')
plt.title('FPS Over Time')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

