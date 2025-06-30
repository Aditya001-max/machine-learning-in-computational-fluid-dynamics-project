#!/usr/bin/env python3

import numpy as np
from smartredis import Client
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
        # Paths
        points_path = "constant/polyMesh/points"
        if not os.path.exists(points_path):
            raise FileNotFoundError(f"{points_path} not found")

        timesteps = sorted([d for d in os.listdir(".") if d.replace(".", "", 1).isdigit()], key=float)
        if not timesteps:
            raise RuntimeError("No timestep directories found.")

        latest_time = timesteps[-1]
        displacement_path = os.path.join(latest_time, "pointDisplacement")

        if not os.path.exists(displacement_path):
            raise FileNotFoundError(f"{displacement_path} not found")

        # Load data
        points = load_points(points_path)
        displacements = load_points(displacement_path)

        # Connect to Redis
        client = Client(address="127.0.0.1:8000", cluster=False)

        # Number of MPI ranks expected by ML script
        num_chunks = 4

        # Split data into chunks
        points_chunks = np.array_split(points, num_chunks)
        displ_chunks = np.array_split(displacements, num_chunks)

        # Push chunks to Redis and register in lists
        for i in range(num_chunks):
            pt_key = f"points_tensor_{i}"
            dp_key = f"displacements_tensor_{i}"
            client.put_tensor(pt_key, points_chunks[i])
            client.put_tensor(dp_key, displ_chunks[i])
            client.append_to_list("pointsDatasetList", pt_key)
            client.append_to_list("displacementsDatasetList", dp_key)

        print("✅ All mesh data chunks sent to Redis")

    except Exception as e:
        print("❌ Error sending to Redis:")
        traceback.print_exc()

if __name__ == "__main__":
    main()

