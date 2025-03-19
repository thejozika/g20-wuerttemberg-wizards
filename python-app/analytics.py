import os
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from data_loader import load_all_datasets  # adjust the import as needed


def dataset_summary(datasets: dict) -> dict:
    """
    Create a summary dictionary for each dataset.
    For each layer, store the number of features and, if available,
    basic stats (min, max, mean) on the 'value' attribute.
    """
    summary = {}
    for dataset_name, layers in datasets.items():
        summary[dataset_name] = {}
        for layer_name, gdf in layers.items():
            num_features = len(gdf)
            stats = {}
            if "value" in gdf.columns and not gdf["value"].empty:
                stats = {
                    "min": gdf["value"].min(),
                    "max": gdf["value"].max(),
                    "mean": gdf["value"].mean()
                }
            summary[dataset_name][layer_name] = {
                "features": num_features,
                "value_stats": stats
            }
    return summary


def print_summary(summary: dict):
    """
    Print a neat summary of each dataset and its layers.
    """
    for dataset, layers in summary.items():
        print("=" * 50)
        print(f"Dataset: {dataset}")
        for layer, stats in layers.items():
            print(f"  Layer: {layer} - {stats['features']} features")
            if stats["value_stats"]:
                print(f"    Value stats: {stats['value_stats']}")
        print("\n")


def plot_feature_counts(summary: dict):
    """
    Plot bar charts for each dataset showing feature counts per layer.
    """
    for dataset, layers in summary.items():
        layer_names = list(layers.keys())
        feature_counts = [layers[layer]["features"] for layer in layer_names]

        plt.figure()
        plt.bar(layer_names, feature_counts)
        plt.title(f"Feature Counts for {dataset}")
        plt.xlabel("Layer")
        plt.ylabel("Number of Features")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # Adjust the base_dir path as needed.
    base_dir = "../datasets"
    if os.path.exists(base_dir):
        datasets = load_all_datasets(base_dir)
        summary = dataset_summary(datasets)
        print_summary(summary)
        plot_feature_counts(summary)
    else:
        print(f"Dataset directory {base_dir} does not exist.")
