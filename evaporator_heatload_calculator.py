import streamlit as st
from CoolProp.CoolProp import PropsSI

st.title("Evaporator Refrigerant Heat Load Calculator (R134a & R407C)")

# User Inputs
fluid = st.sidebar.selectbox("Select Refrigerant", ["R134a", "R407C"])
P_evap_bar = st.sidebar.number_input("evaporating Pressure (bar abs)", value=10.00, min_value=1.0, max_value=35.0, step=0.1)
T_superheat = st.sidebar.number_input("Outlet Superheated Temp (°C)", value=11)
T_subcool = st.sidebar.number_input("Inlet Subcooled Liquid Temp (°C)", value=5.0)
m_dot = st.sidebar.number_input("Mass Flow Rate (kg/s)", value=0.599)

# Convert to SI units
P_evap = P_evap_bar * 1e5  # Pa
T1 = T_superheat + 273.15  # K
T3 = T_subcool + 273.15    # K

try:
    # Get saturation temperature at condensing pressure
    T_sat = PropsSI("T", "P", P_evap, "Q", 1, fluid)

    # h1: superheated vapor or saturated vapor
    if T1 < T_sat:
        h1 = PropsSI("H", "P", P_evap, "T", T1, fluid)
    else:
        h1 = PropsSI("H", "P", P_evap, "Q", 1, fluid)

    # h2: saturated vapor
    h2 = PropsSI("H", "P", P_evap, "Q", 0, fluid)

    # h3: saturated vapour
    h3 = PropsSI("H", "P", P_evap, "Q", 0, fluid)

    # h4: subcooled liquid or saturated liquid
    if T3 > T_sat:
        h4 = PropsSI("H", "P", P_evap, "T", T3, fluid)
    else:
        h4 = h3

    # Calculate heat duties
    q_sensible = h2 - h1
    q_latent = h3 - h2
    q_superheat = h4 - h3

    Q_sensible = m_dot * q_sensible / 1000
    Q_latent = m_dot * q_latent / 1000
    Q_superheat = m_dot * q_superheat / 1000
    Q_total = Q_sensible + Q_latent + Q_superheat

    # Display results
    st.subheader("Heat Load Results")
    st.write(f"**Sensible heating:** {Q_sensible:.2f} kW")
    st.write(f"**Latent evaporation:** {Q_latent:.2f} kW")
    st.write(f"**Superheating:** {Q_superheat:.2f} kW")
    st.write(f"**Total Heat added:** {Q_total:.2f} kW")

except Exception as e:
    st.error(f"Calculation error: {e}")
