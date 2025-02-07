import matplotlib.pyplot as plt
import os

# Function to read and normalize log data from a file
def read_log(file_path, global_start_time):
    timestamps = []
    fps_values = []

    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(";")
            time_part = float(parts[0].split(":")[1])
            fps_part = int(parts[1].split(":")[1])

            normalized_time = int(time_part - global_start_time)  # Normalize time using global start
            timestamps.append(normalized_time)
            fps_values.append(fps_part)

    return timestamps, fps_values

# Paths to log files (relative paths)
log1_path = "POCs/performance_eval/logs/baseline_100.log"
log2_path = "POCs/performance_eval/logs/baseline_1000.log"

# Check if files exist
if not os.path.exists(log1_path) or not os.path.exists(log2_path):
    print("Error: One or both log files are missing.")
else:
    # Find the earliest timestamp from both logs
    with open(log1_path, "r") as file1, open(log2_path, "r") as file2:
        first_time1 = float(file1.readline().split(";")[0].split(":")[1])
        first_time2 = float(file2.readline().split(";")[0].split(":")[1])
        global_start_time = min(first_time1, first_time2)  # Take the earliest time

    # Read and normalize log data
    timestamps1, fps_values1 = read_log(log1_path, global_start_time)
    timestamps2, fps_values2 = read_log(log2_path, global_start_time)

    # Define custom colors
    color1 = "#FF5733"  # Orange-Red for Log 1
    color2 = "#33FF57"  # Green for Log 2

    # Plot the first dataset
    plt.figure(figsize=(10, 5))
    plt.plot(timestamps1, fps_values1, marker='o', linestyle='-', color=color1, label='FPS - Log 1')

    # Plot the second dataset
    plt.plot(timestamps2, fps_values2, marker='s', linestyle='-', color=color2, label='FPS - Log 2')

    # Formatting the plot
    plt.xlabel('Time (seconds)')
    plt.ylabel('FPS')
    plt.title('FPS Over Time (Normalized)')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()
