import streamlit as st
from CoolProp.CoolProp import PropsSI

st.title("Refrigerant Heat Load Calculator (R134a & R407C)")

# User Inputs
fluid = st.sidebar.selectbox("Select Refrigerant", ["R134a", "R407C"])
P_cond_bar = st.sidebar.number_input("Condensing Pressure (bar abs)", value=23.52, min_value=1.0, max_value=35.0, step=0.1)
T_superheat = st.sidebar.number_input("Inlet Superheated Temp (°C)", value=95.0)
T_subcool = st.sidebar.number_input("Outlet Subcooled Liquid Temp (°C)", value=52.7)
m_dot = st.sidebar.number_input("Mass Flow Rate (kg/s)", value=0.599)

# Convert to SI units
P_cond = P_cond_bar * 1e5  # Pa
T1 = T_superheat + 273.15  # K
T3 = T_subcool + 273.15    # K

try:
    # Get saturation temperature at condensing pressure
    T_sat = PropsSI("T", "P", P_cond, "Q", 0, fluid)

    # h1: superheated vapor or saturated vapor
    if T1 > T_sat:
        h1 = PropsSI("H", "P", P_cond, "T", T1, fluid)
    else:
        h1 = PropsSI("H", "P", P_cond, "Q", 1, fluid)

    # h2: saturated vapor
    h2 = PropsSI("H", "P", P_cond, "Q", 1, fluid)

    # h3: saturated liquid
    h3 = PropsSI("H", "P", P_cond, "Q", 0, fluid)

    # h4: subcooled liquid or saturated liquid
    if T3 < T_sat:
        h4 = PropsSI("H", "P", P_cond, "T", T3, fluid)
    else:
        h4 = h3

    # Calculate heat duties
    q_sensible = h1 - h2
    q_latent = h2 - h3
    q_subcool = h3 - h4

    Q_sensible = m_dot * q_sensible / 1000
    Q_latent = m_dot * q_latent / 1000
    Q_subcool = m_dot * q_subcool / 1000
    Q_total = Q_sensible + Q_latent + Q_subcool

    # Display results
    st.subheader("Heat Load Results")
    st.write(f"**Sensible Cooling:** {Q_sensible:.2f} kW")
    st.write(f"**Latent Condensation:** {Q_latent:.2f} kW")
    st.write(f"**Subcooling:** {Q_subcool:.2f} kW")
    st.write(f"**Total Heat Removed:** {Q_total:.2f} kW")

except Exception as e:
    st.error(f"Calculation error: {e}")
