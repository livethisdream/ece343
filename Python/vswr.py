import numpy as np
import matplotlib.pyplot as plt

# Define the function
def my_function(wt,bz):
    return np.cos(wt-2*np.pi*bz) + 0.75* np.cos(wt+2*np.pi*bz)

# Generate x values from -2 to 0 in increments of 0.25
bz_values = np.arange(-2, 0, 0.005)


wt_values = [0, np.pi/4] # np.arange(0,2*np.pi,2*np.pi/64) #[0,np.pi/2]

for val in wt_values:
    # Calculate corresponding y values
    y_values = my_function(val, bz_values)

    # Plot the function
    plt.plot(bz_values, y_values,color='blue')

plt.title('Plot of cos(wt-bz) + Gamma*cos(wt+bz)')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
# Place the legend outside of the plot area
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True)
plt.show()