import os

def generate_config(argument1, argument2, argument3):
    # Create the config content
    config_content = f"""[meta]
; PATH FOR RUNNING LOCALLY
; train_data_path = /Volumes/TINA_UNI/RPA_repres/TrainTestData/{argument1}/{argument2}.arff
; test_data_path = /Volumes/TINA_UNI/RPA_repres/TrainTestData/{argument1}/test.arff

; PATH FOR RUNNING ON ARTEMIS
train_data_path = /project/START2/Tina-repres30days/TrainTestData/{argument1}/{argument2}.arff
test_data_path = /project/START2/Tina-repres30days/TrainTestData/{argument1}/test.arff

[Logistic_Regression]
classname = weka.classifiers.functions.Logistic
"""

    # Directory path where the config file will be saved
    directory = f"Evaluation/{argument3}/{argument1}/LogisticRegression/"

    # Ensure that the directory exists
    os.makedirs(directory, exist_ok=True)

    # Full path to the config file
    config_file_path = os.path.join(directory, "config.ini")

    # Write the config content to the file
    with open(config_file_path, 'w') as f:
        f.write(config_content)

    print(f"Config file generated and saved as {config_file_path}")


def main():
    # Define the argument lists
    argument1_list = ['NO_FS', 'CFS', 'InfoGain', 'Manual_FS']
    
    # Only allow matching pairs for argument2 and argument3
    pairings = [
        ('train', 'NOT_RESAMPLED'),
        ('train_resampled', 'RESAMPLED')
    ]

    # Iterate through all combinations of argument1 and valid argument2, argument3 pairs
    for argument1 in argument1_list:
        for argument2, argument3 in pairings:
            # Generate the config file for the current combination
            generate_config(argument1, argument2, argument3)
    
main()
