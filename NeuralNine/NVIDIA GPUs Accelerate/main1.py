#Code work only under Linux

import pandas as pd
import cudf 
import os
import time
import numpy as np
import kagglehub

module_dir = os.path.dirname(__file__)
os.chdir(module_dir)


# Download latest version
path = kagglehub.dataset_download("mexwell/taxi-trips-2023")
print("Path to dataset files:", path)

df = pd.read_csv("taxi-trips-2023\versions\1\Taxi_Trips_-_2023.csv")
gdf = cudf.DataFrame.from_pandas(df)

df.head()

def basic_operation(df):

    df = df.dropna()

    df =  df[df]['Trip Miles'] > 2

    result = df.groupby('Payment Type').agg({
        'Trip Miles': 'mean',
        'Trip Total': 'sum'
    })

    result =  result.sort_values(by='Trip Miles', accending=False)

    return result

basic_operation(df)

start_time =  time.time()
cpu_result =  basic_operation(df)
cpu_time = time.time() - start_time

start_time =  time.time()
gpu_result =  basic_operation(gdf)
gpu_time = time.time() - start_time

print(f"CPU time : {cpu_time:.4f} secondes")
print(f"GPU time : {gpu_time:.4f} secondes")
print(f"Speed Up : {cpu_time / gpu_time:.4f}x")
print(f"Speed Up : {(cpu_time - gpu_time) / gpu_time * 100:.2f}%")

cpu_trip_distance = cpu_result['Trip Miles'].to_numpy()
gpu_trip_distance = gpu_result['Trip Miles'].to_numpy()

cpu_total_amount = cpu_result['Trip Total'].to_numpy()
gpu_total_amount = gpu_result['Trip Total'].to_numpy()

assert np.allclose(cpu_trip_distance, gpu_trip_distance, atol=1e-5), "Trip distance do not match"
assert np.allclose(cpu_total_amount, gpu_total_amount, atol=1e-5), "Trip distance do not match"
