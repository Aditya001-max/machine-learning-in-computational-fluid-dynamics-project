#!/usr/bin/env python3

import os
import io
import time
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from smartredis import Client
from smartsim import Experiment

from matplotlib import rcParams
rcParams["figure.dpi"] = 200
from smartsim.error.errors import SmartSimError

# Define MLP model
class MLP(nn.Module):
    def __init__(self, num_layers, layer_width, input_size, output_size, activation_fn):
        super(MLP, self).__init__()
        layers = [nn.Linear(input_size, layer_width), activation_fn]
        for _ in range(num_layers - 2):
            layers += [nn.Linear(layer_width, layer_width), activation_fn]
        layers.append(nn.Linear(layer_width, output_size))
        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        return self.layers(x)

# Sort helper
def sort_tensors_by_names(tensors, tensor_names):
    pairs = sorted(zip(tensor_names, tensors))
    tensor_names_sorted, tensors_sorted = zip(*pairs)
    return list(tensors_sorted), list(tensor_names_sorted)

def main():
    exp = Experiment("mesh-motion", launcher="local")

    # ✅ You are manually starting Redis from another terminal (Terminal 1)
    redis_address = "127.0.0.1:8010"
    print("🔁 Connecting to Redis at", redis_address)

    # ✅ Connect to the Redis orchestrator that’s already running
    client = Client(address=redis_address, cluster=False) 
    num_mpi_ranks = 4

    of_rs = exp.create_run_settings(exe="moveDynamicMesh", exe_args="-case spinningDisk -parallel",
                                    run_command="mpirun", run_args={"np": f"{num_mpi_ranks}"})
    of_model = exp.create_model(name="of_model", run_settings=of_rs)

    try:
        exp.start(of_model, block=False)

        torch.set_default_dtype(torch.float64)
        model = MLP(num_layers=3, layer_width=50, input_size=2, output_size=2, activation_fn=nn.Sigmoid())

        local_time_index = 1
        while True:
            print(f"Time step {local_time_index}")
            if not client.poll_list_length("meshDatasetList", num_mpi_ranks, 10, 1000):
                raise ValueError("Mesh dataset list not updated.")

            datasets = client.get_datasets_from_list("meshDatasetList")
            points, displacements = [], []

            for ds in datasets:
                pt_name = next(n for n in ds.get_tensor_names() if "points" in n)
                dp_name = next(n for n in ds.get_tensor_names() if "displacements" in n)
                points.append(ds.get_tensor(pt_name))
                displacements.append(ds.get_tensor(dp_name))

            points = torch.from_numpy(np.vstack(points))[:, :2]
            displacements = torch.from_numpy(np.vstack(displacements))[:, :2]

            points_train, points_val, displ_train, displ_val = train_test_split(points, displacements, test_size=0.2, random_state=42)

            optimizer = optim.Adam(model.parameters(), lr=1e-4)
            loss_func = nn.MSELoss()
            epochs = 10000
            validation_rmse = []

            model.train()
            for epoch in range(epochs):
                optimizer.zero_grad()
                displ_pred = model(points_train)
                loss_train = loss_func(displ_pred, displ_train)
                loss_train.backward()
                optimizer.step()

                with torch.no_grad():
                    displ_pred_val = model(points_val)
                    mse_loss_val = loss_func(displ_pred_val, displ_val)
                    validation_rmse.append(torch.sqrt(mse_loss_val))

            # Save validation loss plot
            plt.figure()
            plt.loglog()
            plt.title("Validation loss RMSE")
            plt.xlabel("Epochs")
            plt.plot(validation_rmse)
            plt.savefig(f"validation_loss_t{local_time_index}.png")
            plt.close()

            # Plot actual vs predicted displacements
            points_np = points.detach().numpy()
            displ_np = displacements.detach().numpy()
            displ_pred_np = model.forward(points).detach().numpy()

            plt.figure()
            plt.axis('equal')
            plt.title(f"Actual Displacements at t={local_time_index}")
            plt.scatter(points_np[:, 0], points_np[:, 1], color='blue', s=5)
            plt.quiver(points_np[:, 0], points_np[:, 1], displ_np[:, 0], displ_np[:, 1], color='green')
            plt.savefig(f"actual_displacements_t{local_time_index}.png")
            plt.close()

            plt.figure()
            plt.axis('equal')
            plt.title(f"Predicted Displacements at t={local_time_index}")
            plt.quiver(points_np[:, 0], points_np[:, 1], displ_pred_np[:, 0], displ_pred_np[:, 1], color='red', width=0.002)
            plt.savefig(f"predicted_displacements_t{local_time_index}.png")
            plt.close()

            # Save model to Redis
            model.eval()
            model_script = torch.jit.trace(model, torch.rand(1, 2, dtype=torch.float64))
            model_buffer = io.BytesIO()
            torch.jit.save(model_script, model_buffer)
            client.set_model("MLP", model_buffer.getvalue(), "TORCH", "CPU")

            client.put_tensor("model_updated", np.array([0.]))
            client.delete_list("meshDatasetList")

            local_time_index += 1

            if client.poll_key("end_time_index", 10, 10):
                print("End time reached.")
                break

    except Exception as e:
        print("❌ Exception:", str(e))

    finally:
        exp.stop(db)

if __name__ == "__main__":
    main()

