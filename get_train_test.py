import pandas as pd
from sklearn.model_selection import train_test_split

IN_FILE = 'clean_data/no_FS_full.csv'
# IN_FILE = 'clean_data/no_FS_truncated.csv'

OUT_PATH = 'TrainTestData/'

TARGET_VAR = 'repres30days'

def generate_csv(dataframe, filepath):
	print("Generating csv file: " + filepath + "\n")
	dataframe.to_csv(filepath, index=False)

def main():
    # Load dataset
    df = pd.read_csv(IN_FILE)
    # df = df.head(5000)

    X = df.drop(columns=TARGET_VAR)
    y = df[TARGET_VAR]

    # Perform a stratified 80-20 split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2,  # 20% for test set
        stratify=y,     # Maintain the class distribution
        random_state=42 # Seed for reproducibility
    )

    X_train[TARGET_VAR] = y_train.values
    X_test[TARGET_VAR] = y_test.values

    # Print the sizes of the splits
    print(f"Training set size: {X_train.shape}\n")
    print(f"Testing set size: {X_test.shape}")

    generate_csv(X_train, OUT_PATH + 'NO_FS/train.csv')
    generate_csv(X_test, OUT_PATH + 'NO_FS/test.csv')
   

if __name__ == "__main__":
    main()