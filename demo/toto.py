# change Python Path
from pathlib import Path
from typing import Any, Callable, Dict
pkg_dir = Path().resolve().parents[0]
import sys
sys.path.insert(0,str(pkg_dir.absolute()))

import matplotlib.pyplot as plt
import pandas as pd


from firefly.geography.gravity import gravity
from firefly.geography.position import Position
import numpy as np

list_data =[
    "time",
    "X_ECEF",
    "Y_ECEF",
    "Z_ECEF",
    "Vx_ECEF",
    "Vy_ECEF",
    "Vz_ECEF",
]

earth_model = "SPHERICAL"

# support functions
def gravity4X(
        t:float,
        X: list[float]) -> list[float]:
    return gravity(Position(*X[0:3]),earth_model=earth_model)
    


def pfd(
        t:float,
        X:list[float]) -> list[float]:

    [x,y,z,vx,vy,vz] = X

    velocity = [vx, vy, vz]

    # Position Equation
    dx_dt = velocity
    

    dv_dt = gravity4X(t,X)

    return dx_dt + dv_dt # concat vector

def hit_ground(t, X): 

    [x,y,z,_,_,_] = X

    [_,_,alt] = Position(x,y,z).as_LLA(earth_model=earth_model)
    
    return alt


# initi value
pos0 = Position.from_LLA(0.,0.,1000000.)

X0 = [pos0.x,pos0.y,pos0.z,0.,0.,0.]

tend = 40000
time = np.linspace(0,tend,10000)
tspan = (0, tend)

from scipy.integrate import solve_ivp, RK45
hit_ground.terminal = True
Y = solve_ivp(pfd,tspan,X0,events=[hit_ground],max_step=0.1,
              dense_output=True)

if Y.status == 1:
    print('Success, termination event occured.')
if Y.status == 0:
    print('Success, t end reached.')



df = pd.DataFrame(
    np.concatenate((Y.t[:, np.newaxis], Y.y.T), axis= 1),columns=list_data)

# print(df.shape)

# print(df.tail())


# Add informations to dataframe

def calculate_position(t,X):
    lat_n, long_n, alt_n = Position(*X[0:3]).as_LLA()
    
    return {'lat': lat_n,
            'long': long_n,
            'alt': alt_n}

def calculate_position2(t,X):
    lat_n, long_n, alt_n = Position(*X[0:3]).as_LLA()
    
    return {'lat2': lat_n,
            'long2': long_n,
            'alt2': alt_n}

def add_parameters(
        df:pd.DataFrame,
        funs:list[Callable[[float, list[float]], Dict[str, Any]]]
        ) -> pd.DataFrame:
    
    tt = []
    
    for index, row in df.iterrows():

        # initiate dict
        new_row_as_dict = {}

        #create X
        X = row[list_data[1:]]

        # create t
        t = row["time"]
        for fun in funs:

            dict_to_add = fun(t,X)
            if dict_to_add.keys() & new_row_as_dict.keys() == set():
                new_row_as_dict.update(dict_to_add)
            else:
                common_keys = list(dict_to_add.keys() & new_row_as_dict.keys())
                msg = [
                    f"The following keys are used at least twice: {common_keys}"
                ]
                raise KeyError(msg)
        
        tt.append(new_row_as_dict)

    new_df = pd.DataFrame.from_dict(tt) # type: ignore
    return pd.concat([df,new_df],axis=1)


df2 = add_parameters(df,funs=[calculate_position,calculate_position2]) 

# print(df2.tail())

# print(Y)



