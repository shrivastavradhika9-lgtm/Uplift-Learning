import pandas as pd


def load_data(path="data/learners.csv"):
    """Load learner intervention data from CSV."""
    df = pd.read_csv(path)
    return df


if __name__ == "__main__":
    df = load_data()

    print("Dataset loaded successfully!")
    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())