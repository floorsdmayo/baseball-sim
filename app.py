import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Baseball Pro", layout="wide")

# going back to CSS because do i have a choice
st.markdown("""
    <style>
    g.updatemenu-button rect {
        fill: #28a745 !important;
        stroke: #1e7e34 !important;
    }
    g.updatemenu-button text {
        fill: white !important;
        font-weight: bold !important;
    }
    .js-plotly-plot {
        height: 500px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚾ Baseball Physics Pro")

st.sidebar.header("Simulation Settings")
v0 = st.sidebar.slider("Initial Velocity (m/s)", 20.0, 100.0, 50.0)
angle = st.sidebar.slider("Launch Angle (degrees)", 0.0, 90.0, 35.0)

m, r, rho, C, g = 0.145, 0.0366, 1.2, 0.5, 9.8
A, dt = np.pi * r**2, 0.05
D = (rho * C * A) / 2

def get_trajectory(v0, angle_deg, drag=True):
    angle_rad = np.radians(angle_deg)
    vx, vy = v0 * np.cos(angle_rad), v0 * np.sin(angle_rad)
    x, y = 0.0, 0.0
    path = [[x, y]]
    while y >= 0:
        v = np.sqrt(vx**2 + vy**2)
        ax = -(D/m) * v * vx if drag else 0
        ay = -g - (D/m) * v * vy if drag else -g
        x += vx * dt
        y += vy * dt
        vx += ax * dt
        vy += ay * dt
        if y >= 0: path.append([x, y])
    return np.array(path)

drag_path = get_trajectory(v0, angle)
ideal_path = get_trajectory(v0, angle, drag=False)

max_len = max(len(drag_path), len(ideal_path))
def pad_path(path, length):
    last_val = path[-1]
    return np.vstack([path, np.tile(last_val, (length - len(path), 1))])

drag_padded = pad_path(drag_path, max_len)
ideal_padded = pad_path(ideal_path, max_len)

fig = go.Figure(
    data=[
        go.Scatter(x=drag_padded[:,0], y=drag_padded[:,1], name="With Drag", line=dict(color="#28a745", width=3)),
        go.Scatter(x=ideal_padded[:,0], y=ideal_padded[:,1], name="No Drag", line=dict(color="#9b59b6", dash="dash")),
        go.Scatter(x=[0], y=[0], name="Ball", mode="markers", marker=dict(color="white", size=14, line=dict(color="red", width=2)))
    ],
    layout=go.Layout(
        xaxis=dict(range=[0, max(ideal_path[:,0]) * 1.1], title="Distance (m)"),
        yaxis=dict(range=[0, max(ideal_path[:,1]) * 1.1], title="Height (m)"),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            x=0.05, y=1.15,
            buttons=[dict(
                label="PLAY BALL",
                method="animate",
                args=[None, {"frame": {"duration": 15, "redraw": False}, "fromcurrent": True, "transition": {"duration": 0}}]
            )]
        )]
    ),
    frames=[go.Frame(data=[
        go.Scatter(x=drag_padded[:k,0], y=drag_padded[:k,1]),
        go.Scatter(x=ideal_padded[:k,0], y=ideal_padded[:k,1]),
        go.Scatter(x=[drag_padded[k,0]], y=[drag_padded[k,1]])
    ]) for k in range(1, max_len, 2)]
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.divider()
col1, col2 = st.columns(2)
col1.metric("Distance", f"{drag_path[-1,0]:.1f} m")
col2.metric("Peak Height", f"{max(drag_path[:,1]):.1f} m")
