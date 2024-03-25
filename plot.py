import numpy as np
import matplotlib.pyplot as plt

# Constants provided by the problem
B = 0.21
N = 10
S = 0.50
f = 50
R = 20

# Time array
t = np.linspace(0, 0.04, 1000)
theta = np.linspace(0, 2*np.pi, 1000)
# Angular frequency
omega = 2 * np.pi * f

# Calculate Vmax and Imax
V_max = omega * N * B * S
I_max = V_max / R

# Calculate voltage U(t) and current I(t)
U_t = V_max * np.sin(theta)
I_t = U_t / R

# Calculate power output P_out(t)
P_out = U_t * I_t

# Plotting
fig, ax = plt.subplots(3, 1, figsize=(12, 15))

# Voltage as a function of time
ax[0].plot(theta, U_t, label='Voltage U(theta)')
ax[0].set_xlabel('theta (rad)')
ax[0].set_ylabel('Voltage (V)')
ax[0].set_title('Voltage U(theta) vs. theta')
ax[0].legend()
ax[0].grid(True)

# Current as a function of time
ax[1].plot(theta, I_t, label='Current I(theta)', color='orange')
ax[1].set_xlabel('theta (rad)')
ax[1].set_ylabel('Current (A)')
ax[1].set_title('Current I(theta) vs. theta')
ax[1].legend()
ax[1].grid(True)

# Power output as a function of time
ax[2].plot(theta, P_out, label='Power (theta)', color='green')
ax[2].set_xlabel('theta (rad)')
ax[2].set_ylabel('Power (W)')
ax[2].set_title('Power (theta) vs. theta')
ax[2].legend()
ax[2].grid(True)

# Display the plots
plt.tight_layout()
plt.savefig('result2.png')

# Print average power
#print(f"The average power P_av produced by the generator is: {P_av} Watts")
