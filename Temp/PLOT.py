import numpy as np
import matplotlib.pyplot as plt

# Initialize figure and axis
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
x = np.arange(512)  # x-axis values (assuming index represents time)
line, = ax.plot(x, np.zeros(512))  # Initialize line plot

# Set plot labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Real-Time Data Plot')

# Initialize buffer
buffer = np.zeros(512)


# Function to update plot
def update_plot():
    global buffer
    line.set_ydata(buffer)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()
    fig.canvas.flush_events()


# Simulate real-time updating of buffer
import time

while True:
    # Update buffer with new data (random values for demonstration)
    new_data = np.random.rand(512)  # Generate random data
    buffer = np.roll(buffer, -len(new_data))  # Shift buffer
    buffer[-len(new_data):] = new_data  # Update buffer with new data

    # Update plot
    update_plot()

    # Pause for 0.05 seconds (adjust as needed)
    time.sleep(0.05)
