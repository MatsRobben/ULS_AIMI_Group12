import os
import matplotlib.pyplot as plt

def plot_histograms(df, columns_to_plot, save_dir, split_column='Dice', threshold=0):
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
        ax_low.hist(df_low[column], bins=20, color='red', edgecolor='black', alpha=0.5)
        ax_low.set_title(f'{column} (<= {threshold})')
        ax_low.set_xlabel('Value')
        ax_low.set_ylabel('Frequency')

        # Plot for the high group
        ax_high = axes[i, 1]
        ax_high.hist(df_high[column], bins=20, color='blue', edgecolor='black', alpha=0.5)
        ax_high.set_title(f'{column} (> {threshold})')
        ax_high.set_xlabel('Value')
        ax_high.set_ylabel('Frequency')

    # Save the subplot as an image file
    file_path = os.path.join(save_dir, 'grouped_column_histogram.png')
    fig.savefig(file_path)
    
    # Close the plot to free memory
    plt.close(fig)

def plot_scatterplots(df, scatterplot_tuples, save_dir, split_column='Dice', threshold=0):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Split the dataframe based on the threshold
    df_low = df[df[split_column] <= threshold]
    df_high = df[df[split_column] > threshold]

    # Create subplots for scatterplots
    num_plots = len(scatterplot_tuples)
    num_rows = (num_plots + 1) // 2  # Round up for odd numbers of plots
    fig, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(12, num_rows * 6))

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

# Example usage
# Define the directory to save the images
save_directory = 'images'

# Define the scatterplot tuples
scatterplot_tuples = [('Dice', 'predicted_lesion_size'), 
                      ('Dice', 'true_num_components')]