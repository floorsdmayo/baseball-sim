import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Baseball Physics Simulator")
st.write("Comparing motion both with and without air resistance. This one's for you, Sir Joni.")

st.sidebar.header("Simulation Settings")
v0 = st.sidebar.slider("Initial Velocity (m/s)", 20.0, 100.0, 50.0)
angle = st.sidebar.slider("Launch Angle (degrees)", 0.0, 90.0, 35.0)

m, r, rho, C, g = 0.145, 0.0366, 1.2, 0.5, 9.8
A = np.pi * r**2
D = (rho * C * A) / 2
dt = 0.01

angle_rad = np.radians(angle)
vx, vy = v0 * np.cos(angle_rad), v0 * np.sin(angle_rad)
x, y = 0.0, 0.0
x_list, y_list = [x], [y]

while y >= 0:
    v = np.sqrt(vx**2 + vy**2)
    ax = -(D/m) * v * vx
    ay = -g - (D/m) * v * vy
    x += vx * dt + 0.5 * ax * dt**2
    y += vy * dt + 0.5 * ay * dt**2
    vx += ax * dt
    vy += ay * dt
    x_list.append(x)
    y_list.append(y)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x_list, y_list, color='green', label='With Air Drag')

# Ideal trajectory
t_ideal = np.linspace(0, (2 * v0 * np.sin(angle_rad)) / g, 100)
x_ideal = v0 * np.cos(angle_rad) * t_ideal
y_ideal = v0 * np.sin(angle_rad) * t_ideal - 0.5 * g * t_ideal**2
ax.plot(x_ideal[y_ideal >= 0], y_ideal[y_ideal >= 0], 
         color='purple', linestyle='--', label='No Air Drag')

ax.set_title('Baseball Trajectory')
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')
ax.legend()
ax.grid(True)

st.pyplot(fig)
