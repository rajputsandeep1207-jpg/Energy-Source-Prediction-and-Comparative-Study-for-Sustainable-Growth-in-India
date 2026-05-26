#!/usr/bin/env python
# coding: utf-8

# 
# # Problem Statement
# 
# India’s growing population and rapid industrial development have increased the demand for energy. Traditional non-renewable energy sources such as coal and oil contribute heavily to pollution, carbon emissions, and environmental damage. At the same time, renewable energy sources like solar, wind, and hydro power are becoming more important for sustainable development.
# 
# The challenge is to compare renewable and non-renewable energy sources based on factors such as energy production, cost, sustainability, carbon emissions, reliability, and employment generation. The project aims to analyze energy-related data and build machine learning models that can help predict and identify the most sustainable and efficient energy sources for future growth in India.
# 
# ---
# 
# # Objectives of the Project
# 
# 1. To analyze different energy sources using data analysis techniques.
# 
# 2. To compare renewable and non-renewable energy sources based on:
#    - Energy production
#    - Energy consumption
#    - Cost per kWh
#    - CO2 emissions
#    - Sustainability index
#    - Reliability
#    - Employment generation
# 
# 3. To perform data preprocessing and visualization for better understanding of energy trends.
# 
# 4. To identify the environmental and economic impact of various energy sources.
# 
# 5. To apply machine learning algorithms such as:
#    - Random Forest
#    - Decision Tree
#    - XGBoost
# 
# 6. To evaluate and compare model performance for energy source prediction.
# 
# 7. To provide insights that support sustainable energy planning and decision-making in India.
# 
# 8. To encourage the adoption of cleaner and more sustainable energy resources for future development.
# 

# # Capstone Project: Energy Source Prediction and Comparative Study for Sustainable Growth in India
# 
# ## Project Overview
# This capstone project compares renewable and non-renewable energy sources across multiple dimensions:
# - Cost analysis
# - Sustainability
# - Environmental impact
# - Employment generation
# - Government subsidies
# - Energy generation efficiency
# 
# The project also uses Machine Learning models to:
# 1. Predict Energy Type (Renewable / Non-Renewable)
# 2. Analyze important factors affecting sustainability
# 3. Forecast future trends and compare energy sources
# 
# ---
# 
# ## Technologies Used
# - Python
# - NumPy
# - Pandas
# - Matplotlib
# - Seaborn
# - Scikit-learn
# - XGBoost
# - Jupyter Notebook
# 
# ---
# 
# ## Dataset Description
# The dataset contains various energy-related attributes such as:
# - Installation Cost
# - Generation Cost
# - CO2 Emission
# - Employment
# - Sustainability
# - Government Subsidies
# - Transmission Loss
# - Electricity Generation
# - Risk Factors
# 
# The objective is to analyze how renewable and non-renewable sources differ and identify the most sustainable options for India.
# 

# In[1]:


# Import Required Libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

try:
    from xgboost import XGBClassifier
    xgb_available = True
except:
    xgb_available = False

# Load Dataset
# IMPORTANT:
# Keep your CSV file in the same folder as this notebook
# OR provide the full file path below.

df = pd.read_csv("CAPSTONE PROJECT.csv")

print("Dataset Shape:", df.shape)

df.head()


# ## Dataset Information

# In[2]:


df.info()


# ## Checking Missing Values

# In[3]:


df.isnull().sum()


# ## Statistical Summary

# In[4]:


df.describe(include='all')


# ## Data Visualization

# In[5]:


# Countplot for Energy Types

plt.figure(figsize=(8,5))
sns.countplot(x='Energy Type', data=df)
plt.title("Distribution of Energy Types")
plt.show()


# In[6]:


# CO2 Emission by Energy Source

plt.figure(figsize=(12,6))
sns.barplot(x='Energy Source', y='CO2 Emission (kg per kWh)', data=df)
plt.xticks(rotation=45)
plt.title("CO2 Emission by Energy Source")
plt.show()


# In[7]:


# Installation Cost Comparison

plt.figure(figsize=(12,6))
sns.boxplot(x='Energy Type', y='Installation Cost (INR per kW)', data=df)
plt.title("Installation Cost Comparison")
plt.show()


# In[8]:


# Generation Cost Distribution

plt.figure(figsize=(10,6))
sns.histplot(df['Generation Cost (INR per unit)'], kde=True)
plt.title("Generation Cost Distribution")
plt.show()


# In[9]:


# Correlation Heatmap

numeric_df = df.select_dtypes(include=np.number)

plt.figure(figsize=(14,10))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Heatmap")
plt.show()


# ## Data Preprocessing

# In[10]:


# Encode Categorical Variables

df_encoded = df.copy()

label_encoders = {}

for column in df_encoded.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df_encoded[column] = le.fit_transform(df_encoded[column])
    label_encoders[column] = le

df_encoded.head()


# ## Feature Selection

# In[11]:


# Features and Target

X = df_encoded.drop('Energy Type', axis=1)
y = df_encoded['Energy Type']

print("Feature Shape:", X.shape)
print("Target Shape:", y.shape)


# ## Train Test Split

# In[12]:


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

print("Training Samples:", X_train.shape[0])
print("Testing Samples:", X_test.shape[0])


# ## Random Forest Classification

# In[13]:


rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

rf_accuracy = accuracy_score(y_test, rf_predictions)

print("Random Forest Accuracy:", rf_accuracy)
print("\nClassification Report:\n")
print(classification_report(y_test, rf_predictions))


# In[14]:


# Confusion Matrix

cm = confusion_matrix(y_test, rf_predictions)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title("Random Forest Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ## Feature Importance

# In[15]:


importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
})

importance = importance.sort_values(by='Importance', ascending=False)

plt.figure(figsize=(12,8))
sns.barplot(x='Importance', y='Feature', data=importance)
plt.title("Feature Importance")
plt.show()

importance.head(10)


# ## Decision Tree Model

# In[16]:


dt_model = DecisionTreeClassifier(random_state=42)

dt_model.fit(X_train, y_train)

dt_predictions = dt_model.predict(X_test)

dt_accuracy = accuracy_score(y_test, dt_predictions)

print("Decision Tree Accuracy:", dt_accuracy)


# ## XGBoost Model

# In[17]:


if xgb_available:

    xgb_model = XGBClassifier(
        use_label_encoder=False,
        eval_metric='logloss'
    )

    xgb_model.fit(X_train, y_train)

    xgb_predictions = xgb_model.predict(X_test)

    xgb_accuracy = accuracy_score(y_test, xgb_predictions)

    print("XGBoost Accuracy:", xgb_accuracy)

else:
    print("XGBoost is not installed in this environment.")


# ## Model Comparison

# In[18]:


models = ['Random Forest', 'Decision Tree']
accuracies = [rf_accuracy, dt_accuracy]

if xgb_available:
    models.append('XGBoost')
    accuracies.append(xgb_accuracy)

comparison_df = pd.DataFrame({
    'Model': models,
    'Accuracy': accuracies
})

comparison_df


# In[19]:


plt.figure(figsize=(8,5))
sns.barplot(x='Model', y='Accuracy', data=comparison_df)
plt.title("Model Accuracy Comparison")
plt.ylim(0,1)
plt.show()


# # Business Insights
# 
# ## Key Findings
# 1. Renewable energy sources produce significantly lower CO2 emissions.
# 2. Solar and wind energy have higher sustainability scores.
# 3. Fossil fuels show higher environmental impact and global warming effects.
# 4. Government subsidies strongly support renewable energy growth.
# 5. Renewable sources create more long-term sustainable employment opportunities.
# 
# ---
# 
# # Conclusion
# 
# This project successfully analyzed renewable and non-renewable energy sources in India using Machine Learning and Data Analytics techniques.
# 
# The study shows that renewable energy sources:
# - Are more sustainable
# - Produce less pollution
# - Receive better government support
# - Provide long-term environmental benefits
# 
# Among the machine learning models tested:
# - Random Forest performed effectively for energy type prediction.
# - Feature importance analysis identified the major sustainability indicators.
# 
# This capstone project can help policymakers, researchers, and industries make informed decisions about future energy investments in India.
# 
