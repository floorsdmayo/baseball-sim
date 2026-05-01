import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Baseball Pro", layout="wide")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #28a745 !important;
        color: white !important;
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        font-weight: bold;
        border: none;
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

def draw_plot(frame_idx):
    fig = go.Figure(
        data=[
            go.Scatter(x=drag_path[:,0], y=drag_path[:,1], name="With Drag", line=dict(color="#28a745", width=3)),
            go.Scatter(x=ideal_path[:,0], y=ideal_path[:,1], name="No Drag", line=dict(color="#9b59b6", dash="dash")),
            go.Scatter(x=[drag_path[frame_idx,0]], y=[drag_path[frame_idx,1]], 
                       mode="markers", 
                       marker=dict(color="white", size=15, line=dict(color="red", width=2)),
                       showlegend=False)
        ],
        layout=go.Layout(
            xaxis=dict(range=[0, max(ideal_path[:,0]) * 1.1], title="Distance (m)"),
            yaxis=dict(range=[0, max(ideal_path[:,1]) * 1.1], title="Height (m)"),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x=1)
        )
    )
    return fig

placeholder = st.empty() # This creates a spot for the graph to live

if st.button("PLAY BALL"):
    for i in range(0, len(drag_path), 2):
        with placeholder:
            st.plotly_chart(draw_plot(i), use_container_width=True, config={'displayModeBar': False}, key=f"anim_{i}")
        time.sleep(0.01)
else:
    with placeholder:
        st.plotly_chart(draw_plot(0), use_container_width=True, config={'displayModeBar': False}, key="static_start")

st.divider()
c1, c2 = st.columns(2)
c1.metric("Distance", f"{drag_path[-1,0]:.1f} m")
c2.metric("Peak Height", f"{max(drag_path[:,1]):.1f} m")
