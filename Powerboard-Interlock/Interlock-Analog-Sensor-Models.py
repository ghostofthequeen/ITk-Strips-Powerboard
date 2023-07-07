import numpy as np
import matplotlib.pyplot as plt
## For the NTC, we use the formula R = R_0 exp(B(1/T - 1/T_0))
## We can extract values for B, T_0, and R_0 from the data sheet

x_NTC = np.linspace(-40,40,1000)
B = 3984 ## K
actB = 3665.546
R0 = 10000 ## Ohm
actR0 = 9356.944
T0 = 298.15 ## K, 25 C
V_supply_NTC = 12 ## V
R_NTC = R0*np.exp(B*(1/(x_NTC+273.15) - 1/T0))
NTC = V_supply_NTC*R_NTC/(50000 + R_NTC)
ax = plt.axes()
ax.set_facecolor("pink")
plt.plot(x_NTC,NTC,'c',label="NTC")
plt.xlabel('Temperature (C)')
plt.ylabel('Threshold Voltage (V)')
plt.title('Threshold Voltage vs. Temperature')
plt.legend()

def temp(resistance):
    return 1/(np.log(resistance/R0)/B + 1/T0) - 273.15

def resistance(voltage):
    return 50000*(voltage/V_supply_NTC)/(1 - (voltage/V_supply_NTC))

## For the humidity, we use the formula V_out = V_supply * (0.0062 * RH_s + 0.16)

x_HUM = np.linspace(0,100,1000)
V_supply = 5 ## Vdc, pulled from table specifications
## T = 25 C per table specifications
HUM = V_supply*(0.0062*(x_HUM) + 0.16)
ax = plt.axes()
ax.set_facecolor("pink")
plt.plot(x_HUM,HUM,'c',label="HUM")
plt.xlabel('Relative Humidity (%)')
plt.ylabel('Output Voltage (V)')
plt.title('Output Voltage vs. Relative Humidity')
plt.legend()

def hum(voltage):
    return (voltage/V_supply - 0.16)/0.0062


## For the air flow, we use the formula  V = V_supply((Flow + 10)/212.5 + 0.1) from the datasheet

x_FLOW = np.linspace(0,4,1000)
V_supply = 5 ## Vdd, pulled from table specifications
FLOW = V_supply*((28.3168*x_FLOW + 10)/212.5 + 0.1)
ax = plt.axes()
ax.set_facecolor("pink")
plt.plot(x_FLOW,FLOW,'c',label="FLOW")
plt.xlabel('Air Flow (Cubic Feet Per Minute (CFM))')
plt.ylabel('Output Voltage (V)')
plt.title('Output Voltage vs. Air Flow')
plt.legend()

def flow(voltage):
    return 212.5*(voltage/V_supply - 0.1) - 10
