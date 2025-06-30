#!/usr/bin/env python3

import numpy as np
from smartredis import Client, Dataset
import os
import traceback

def load_points(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Find the first line that contains only "(" and the last line with only ")"
    start = next(i for i, line in enumerate(lines) if line.strip() == '(') + 1
    end = next(i for i, line in enumerate(lines) if line.strip() == ')')

    data = [list(map(float, line.strip("()\n ").split())) for line in lines[start:end]]
    return np.array(data)

def main():
    try:
        # File paths
        points_path = "constant/polyMesh/points"
        timesteps = sorted([d for d in os.listdir(".") if d.replace(".", "", 1).isdigit()], key=float)
        latest_time = timesteps[-1]
        displacement_path = os.path.join(latest_time, "pointDisplacement")

        # Load mesh data
        points = load_points(points_path)
        displacements = load_points(displacement_path)

        # Connect to Redis
        client = Client(address="127.0.0.1:8010", cluster=False)

        # Split into chunks for parallel processing
        num_chunks = 4
        points_chunks = np.array_split(points, num_chunks)
        displ_chunks = np.array_split(displacements, num_chunks)

        for i in range(num_chunks):
            ds = Dataset(f"mesh_data_{i}")
            ds.add_tensor(f"points_tensor_{i}", points_chunks[i])
            ds.add_tensor(f"displacements_tensor_{i}", displ_chunks[i])
            client.put_dataset(ds)
            client.append_to_list("meshDatasetList", ds)

        print("✅ All mesh data chunks sent to Redis")

    except Exception as e:
        print("❌ Error sending to Redis:")
        traceback.print_exc()

if __name__ == "__main__":
    main()

