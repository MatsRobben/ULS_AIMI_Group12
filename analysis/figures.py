import os
import matplotlib.pyplot as plt
import numpy as np

def plot_histograms_two_groups(df, columns_to_plot, save_dir, split_column='Dice', threshold=0):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Split the dataframe based on the threshold
    df_low = df[df[split_column] <= threshold]
    df_high = df[df[split_column] > threshold]

    # Define the number of rows and columns for the subplots
    num_columns = 2
    num_rows = len(columns_to_plot)

    # Create subplots
    fig, axes = plt.subplots(nrows=num_rows, ncols=num_columns, figsize=(12, num_rows * 4))
    fig.tight_layout(pad=3.0)  # Adjust the spacing between subplots

    # Plot histograms for each column for each group
    for i, column in enumerate(columns_to_plot):
        # Plot for the low group
        ax_low = axes[i, 0]
        ax_low.hist(df_low[column], bins=50, color='red', edgecolor='black', alpha=0.5)
        ax_low.set_title(f'{column} (<= {threshold})')
        ax_low.set_xlabel('Value')
        ax_low.set_ylabel('Frequency')

        # Plot for the high group
        ax_high = axes[i, 1]
        ax_high.hist(df_high[column], bins=50, color='blue', edgecolor='black', alpha=0.5)
        ax_high.set_title(f'{column} (> {threshold})')
        ax_high.set_xlabel('Value')
        ax_high.set_ylabel('Frequency')

    # Save the subplot as an image file
    file_path = os.path.join(save_dir, 'grouped_column_histogram.png')
    fig.savefig(file_path)
    
    # Close the plot to free memory
    plt.close(fig)


def plot_histograms(df, columns_to_plot, save_dir):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Create subplots for histograms
    fig_hist, axes_hist = plt.subplots(nrows=len(columns_to_plot) // 2, ncols=2, figsize=(12, 12))
    fig_hist.tight_layout(pad=3.0)  # Adjust the spacing between subplots

    # Flatten the axes array for easy iteration
    axes_hist = axes_hist.flatten()

    # Plot histograms for each column
    for i, column in enumerate(columns_to_plot):
        ax = axes_hist[i]
        ax.hist(df[column], bins=50, color='skyblue', edgecolor='black')
        ax.set_title(column)
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')

    # Hide any unused subplots
    for j in range(len(columns_to_plot), len(axes_hist)):
        axes_hist[j].axis('off')

    # Save the histograms
    file_path = os.path.join(save_dir, f'column_histogram.png')
    fig_hist.savefig(file_path)

    # Close the histogram plot to free memory
    plt.close(fig_hist)

def plot_scatterplots(df, scatterplot_tuples, save_dir, split_column='Dice', threshold=0):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Split the dataframe based on the threshold
    df_low = df[df[split_column] <= threshold]
    df_high = df[df[split_column] > threshold]

    # Create subplots for scatterplots
    num_plots = len(scatterplot_tuples)
    if num_plots == 1:
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 6))
        axes = np.array([axes])  # Make it iterable
    else:
        num_rows = (num_plots + 1) // 2  # Round up for odd numbers of plots
        fig, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(12, num_rows * 6))
        axes = axes.flatten()  # Flatten the axes array for easy iteration

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Plot scatterplots
    for i, scatterplot_tuple in enumerate(scatterplot_tuples):
        column_x, column_y = scatterplot_tuple
        ax = axes[i]
        ax.scatter(df_high[column_x], df_high[column_y], color='blue', label=f'{split_column} > {threshold}')
        ax.scatter(df_low[column_x], df_low[column_y], color='red', label=f'{split_column} <= {threshold}')
        ax.set_title(f'{column_x} vs {column_y}')
        ax.set_xlabel(column_x)
        ax.set_ylabel(column_y)
        ax.legend()

    # Hide any unused subplots
    for j in range(num_plots, len(axes)):
        axes[j].axis('off')

    # Save the subplot as an image file
    scatterplots_filename = '_'.join([f'{column_x}_vs_{column_y}' for (column_x, column_y) in scatterplot_tuples])
    file_path = os.path.join(save_dir, f'{scatterplots_filename}.png')
    fig.savefig(file_path)

    # Close the plot to free memory
    plt.close(fig)