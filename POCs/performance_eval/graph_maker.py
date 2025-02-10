import matplotlib.pyplot as plt
import datetime
#from pathlib import Path


def read_log(file_path):
    timestamps = []
    fps_values = []

    with open(file_path, "r") as file:
        elapsed_seconds = 1
        for line in file:
            parts = line.strip().split(";")
            #time_part = float(parts[0].split(":")[1])
            fps_part = int(parts[1].split(":")[1])
            
            timestamps.append(elapsed_seconds)  # Convert timestamp to datetime
            fps_values.append(fps_part)
            elapsed_seconds += 1

    return timestamps, fps_values


# Read data from logs
seconds_baseline_100, fps_baseline_100 = read_log("POCs/performance_eval/logs/baseline_100.log") 
seconds_baseline_1000, fps_baseline_1000 = read_log("POCs/performance_eval/logs/baseline_1000.log")  

seconds_threading_100, fps_threading_100 = read_log("POCs/performance_eval/logs/threading_100.log") 
seconds_threading_1000, fps_threading_1000 = read_log("POCs/performance_eval/logs/threading_1000.log") 

seconds_multiprocess_100, fps_multiprocess_100 = read_log("POCs/performance_eval/logs/multiprocess_100.log") 
seconds_multiprocess_1000, fps_multiprocess_1000 = read_log("POCs/performance_eval/logs/multiprocess_1000.log") 




# Create plot surface
plt.figure(figsize=(10, 5))

# plot datasets, color can be '#FF5733' or a RGB tuple (1, 0, 0)
# baselines (shades of red)
plt.plot(seconds_baseline_100, fps_baseline_100, marker=None, linestyle='-', color='#FF0000', linewidth = 2, label='Baseline - 100 dots')
plt.plot(seconds_baseline_1000, fps_baseline_1000, marker=None, linestyle='-', color='#A42A04', linewidth = 2, label='Baseline - 1000 dots')

# threading (shades of blue)
plt.plot(seconds_threading_100, fps_threading_100, marker=None, linestyle='-', color='#0096FF', linewidth = 2, label='Threading - 100 dots')
plt.plot(seconds_threading_1000, fps_threading_1000, marker=None, linestyle='-', color='#0047AB', linewidth = 2, label='Threading - 1000 dots')

# multiprocessing (shades of green)
plt.plot(seconds_multiprocess_100, fps_multiprocess_100, marker=None, linestyle='-', color='#32CD32', linewidth = 2, label='Multiprocessing - 100 dots')
plt.plot(seconds_multiprocess_1000, fps_multiprocess_1000, marker=None, linestyle='-', color='#808000', linewidth = 2, label='Multiprocessing - 1000 dots')

# Formatting the plot
plt.xlabel('Elapsed Seconds')
plt.ylabel('FPS')
plt.title('FPS Over Time')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

