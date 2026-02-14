import sys
import os
import pandas as pd
import numpy as np


# -------------------------------
# Input Validation Function
# -------------------------------
def validate_inputs(df, weights_str, impacts_str):
    
    # Check minimum columns
    if df.shape[1] < 3:
        raise ValueError("Input file must contain at least 3 columns.")

    # Check numeric columns (from 2nd column onwards)
    for col in df.columns[1:]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError("All columns from 2nd to last must be numeric.")

    # Parse weights and impacts
    weights = weights_str.split(',')
    impacts = impacts_str.split(',')

    # Check if separated by comma
    if len(weights) == 1:
        raise ValueError("Weights must be separated by comma ','.")

    if len(impacts) == 1:
        raise ValueError("Impacts must be separated by comma ','.")

    # Length match check
    if len(weights) != len(impacts) or len(weights) != (df.shape[1] - 1):
        raise ValueError("Number of weights, impacts and criteria columns must be same.")

    # Convert weights to float
    try:
        weights = np.array(weights, dtype=float)
    except:
        raise ValueError("Weights must be numeric values.")

    # Validate impacts symbols
    if not all(i in ['+', '-'] for i in impacts):
        raise ValueError("Impacts must be either '+' or '-'.")

    return weights, impacts


# -------------------------------
# TOPSIS Calculation Function
# -------------------------------
def calculate_topsis(df, weights, impacts):

    decision_matrix = df.iloc[:, 1:].values.astype(float)

    # Step 1: Normalize decision matrix
    norm_matrix = decision_matrix / np.sqrt((decision_matrix ** 2).sum(axis=0))

    # Step 2: Apply weights
    weighted_matrix = norm_matrix * weights

    # Step 3: Determine ideal best and worst
    ideal_best = np.array([
        weighted_matrix[:, i].max() if impacts[i] == '+'
        else weighted_matrix[:, i].min()
        for i in range(len(impacts))
    ])

    ideal_worst = np.array([
        weighted_matrix[:, i].min() if impacts[i] == '+'
        else weighted_matrix[:, i].max()
        for i in range(len(impacts))
    ])

    # Step 4: Calculate distances
    distance_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    # Step 5: Calculate Topsis Score
    score = distance_worst / (distance_best + distance_worst)

    return score

# -------------------------------
# Reusable Function (For Web App)
# -------------------------------
def run_topsis(input_file, weights_str, impacts_str, output_file):

    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File '{input_file}' not found.")

    df = pd.read_csv(input_file)

    weights, impacts = validate_inputs(df, weights_str, impacts_str)

    score = calculate_topsis(df, weights, impacts)

    df['Topsis Score'] = score
    df['Rank'] = df['Topsis Score'].rank(ascending=False, method='max').astype(int)

    df.to_csv(output_file, index=False)

# -------------------------------
# Main Function (CLI Entry)
# -------------------------------
def main():

    # Check number of parameters
    if len(sys.argv) != 5:
        print("Usage: python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>")
        sys.exit(1)

    input_file = sys.argv[1]
    weights_str = sys.argv[2]
    impacts_str = sys.argv[3]
    output_file = sys.argv[4]

    # Check file existence
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    try:
        # Read input file
        df = pd.read_csv(input_file)

        # Validate inputs
        weights, impacts = validate_inputs(df, weights_str, impacts_str)

        # Calculate TOPSIS
        score = calculate_topsis(df, weights, impacts)

        # Add results
        df['Topsis Score'] = score
        df['Rank'] = df['Topsis Score'].rank(ascending=False, method='max').astype(int)

        # Save output
        df.to_csv(output_file, index=False)

        print("TOPSIS calculation completed successfully.")
        print(f"Output saved to '{output_file}'")

    except Exception as e:
        print("Error:", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
