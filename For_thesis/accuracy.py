import matplotlib.pyplot as plt

# Data from the table
models = [
    "ZeroR", "OneR", "Logistic Regression", "J48 DT",
    "RepTree DT", "MLP", "Naïve Bayes", "Bayesian Network", 
    "Random Forest"
]

no_fs_acc = [78.91, 78.91, 78.99, 79.42, 79.39, 78.91, 78.98, 78.98, 79.15]
cfs_acc = [78.91, 78.91, 78.96, 78.98, 78.98, 78.91, 78.96, 78.96, 78.98]
info_gain_acc = [78.91, 78.91, 78.97, 79.31, 79.31, 78.91, 78.93, 78.93, 79.31]
manual_acc = [78.91, 78.91, 78.92, 79.21, 79.21, 78.91, 78.90, 78.90, 79.21]

# Create the plot
plt.figure(figsize=(10, 6))

plt.plot(models, no_fs_acc, label="No FS", marker='o')
plt.plot(models, cfs_acc, label="CFS", marker='o')
plt.plot(models, info_gain_acc, label="Information Gain", marker='o')
plt.plot(models, manual_acc, label="Manual", marker='o')

plt.title('Accuracy comparison of ML models trained on balanced data and using different FS methods')
plt.xlabel('Models')
plt.ylabel('Accuracy (%)')
plt.xticks(rotation=45, ha='right')
plt.yticks(range(76, 84, 2))  # Sets the y-axis ticks with a step of 2
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
