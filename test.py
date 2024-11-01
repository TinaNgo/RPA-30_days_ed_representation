import numpy as np

def final_diagnosis_subcode_to_nominal(code: float) -> str:
    return int(np.floor(code))


code = 'L50.9'
print(final_diagnosis_subcode_to_nominal(code))