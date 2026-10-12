import numpy as np
import matplotlib.pyplot as plt
import cmath

# Function to calculate the complex expression
def complex_function(L):
    num = 50*((25 + 25j) + 50j * np.tan(2 * np.pi * L))
    denom = 50 + (25j - 25) * np.tan(2 * np.pi * L)
    return num / denom

# Values for L ranging from 0 to 0.45
L_values = np.linspace(0, 0.45, 1000)

# Calculate the complex function for each L
result_values = [complex_function(L) for L in L_values]

# Extract real and imaginary parts for plotting
real_part = np.real(result_values)
imag_part = np.imag(result_values)

# Find indices where imag_part values transition from positive to negative or vice versa
transitions_indices = np.where(np.diff(np.sign(imag_part)) != 0)[0]

# Plotting on the complex plane
plt.figure(figsize=(8, 6))
plt.plot(real_part, imag_part, label='Input Impedance')
plt.scatter(real_part[transitions_indices], imag_part[transitions_indices], color='red', marker='x', label='Sign Transitions')
for i, txt in enumerate(transitions_indices):
    plt.annotate(f'L={L_values[txt]:.3f}', (real_part[txt], imag_part[txt]), textcoords="offset points", xytext=(0,10), ha='center')

plt.title('Complex Plane Plot')
plt.xlabel('Real Part')
plt.ylabel('Imaginary Part')
plt.legend()
plt.grid(True)
plt.show()

# Output the indices where imag_part values transition from positive to negative or vice versa
#print("Indices where imag_part transitions occur:", transitions_indices)

# Print values of L at the transition indices
print("Values of L at transition indices:", L_values[transitions_indices])
