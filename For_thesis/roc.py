import matplotlib.pyplot as plt

# Data for Accuracy and ROC AUC
models = ['ZeroR', 'OneR','Logistic Regression', 'J48 DT', 'RepTree DT', 'MLP', 'Naïve Bayes', 'Bayesian Network', 'Random Forest']


# ROC AUC values for different feature selection methods
auc_no_fs = [0.50, 0.50, 0.61, 0.59, 0.62, 0.58, 0.60, 0.60, 0.62]
auc_cfs = [0.50, 0.50, 0.59, 0.57, 0.57, 0.58, 0.59, 0.59, 0.59]
auc_infogain = [0.50, 0.50, 0.60, 0.59, 0.60, 0.57, 0.60, 0.60, 0.61]
auc_manual = [0.50, 0.50, 0.59, 0.57, 0.58, 0.57, 0.59, 0.59, 0.60]


# Plot for ROC AUC
plt.figure(figsize=(10, 6))
plt.plot(models, auc_no_fs, marker='o', label='No FS')
plt.plot(models, auc_cfs, marker='o', label='CFS')
plt.plot(models, auc_infogain, marker='o', label='Information Gain')
plt.plot(models, auc_manual, marker='o', label='Manual')
plt.title('AUC-ROC comparison of ML models trained on imbalanced data and using different FS methods')
plt.xlabel('Models')
plt.ylabel('AUC-ROC')
plt.xticks(rotation=45)
# plt.yticks(range(0.45, 0.65, 0.5))  # Sets the y-axis ticks with a step of 2
plt.yticks([0.50, 0.55, 0.60, 0.65])


plt.grid(True)
plt.legend()
plt.tight_layout()

# Show ROC AUC Plot
plt.show()
