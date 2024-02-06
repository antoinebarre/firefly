import numpy as np
import firefly.rocket.flow_rate as flow_rate

a = flow_rate.VariableFlowRate(
    times_flow_rate=np.array([0.0, 10.0, 20.0]), values_flow_rate=np.array([100.0, 50.0, 10.0]))

print(a.get_current(5))
print(a.get_current_used_propellant_mass(5))