# Chest X-Ray Pneumonia Detection
This repository contains a machine learning project for detecting pneumonia from chest X-ray images using Convolutional Neural Networks (CNN), Logistic Regression, and Support Vector Machines (SVM). The repository includes a Jupyter notebook for training the models, pre-trained model files, and a Streamlit web app for predicting pneumonia on uploaded X-ray images.

# Live App

The **Chest X-Ray Pneumonia Detection** app is live on Streamlit Cloud! 🚀  
Click the link below to upload X-ray images and predict if they indicate **Pneumonia** or **Normal**:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pneumonia-vanshajr.streamlit.app)

# Project Overview
The goal of this project is to build a classification system for detecting pneumonia from chest X-ray images. The models in this project include:

- Convolutional Neural Network (CNN): Deep learning-based model for image classification.
- Logistic Regression: A traditional machine learning model for binary classification.
- Support Vector Machine (SVM): Another classification algorithm for binary outcomes.

The repository contains:

- A Jupyter Notebook that trains the models using the chest X-ray pneumonia dataset.
- Pre-trained model files for easy deployment.
- A Streamlit app for easy interaction and prediction on new chest X-ray images.
The dataset used in this project is the Chest X-ray Pneumonia dataset available on Kaggle. It contains pneumonia and normal X-ray images.

## Link to the Dataset:
https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia

Make sure to download the dataset and place it in the appropriate folder if running the notebook locally.

# Project Structure
```bash
├── models/
│   ├── cnn_model.h5               # Trained CNN model
│   ├── logistic_regression_model.pkl # Trained Logistic Regression model
│   ├── pca_transformer.pkl         # Trained PCA model
├── app/
│   ├── app.py                     # Streamlit app for pneumonia detection
├── notebooks/
│   ├── pneumonia_detection.ipynb   # Jupyter notebook with model training and comparisons
├── requirements.txt               # Python dependencies for the project
```

# Installation
1. Clone the Repository
```bash
git clone https://github.com/VanshajR/Pneumonia_Detection.git
cd Pneumonia_Detection
```
2. Install Dependencies
Create a virtual environment and install the necessary dependencies listed in `requirements.txt `:

Create and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
```

Install dependencies
```bash
pip install -r requirements.txt
```

3. Running the Jupyter Notebook
Open the `pneumonia_detection.ipynb` notebook in Jupyter or a compatible environment like Google Colab.
Run all the cells to:
- Load the dataset.
- Train the models (CNN, Logistic Regression, and SVM).
- Save the trained models into the models/ directory.

4. Running the Streamlit App
Once the models are trained and saved, you can use the Streamlit app to upload new X-ray images and get predictions.

i) Navigate to the `app/` folder:
```bash
cd app
```

ii) Run the Streamlit App:
```bash
streamlit run app.py
```

iii) Open your browser and go to `http://localhost:8501` to interact with the app.

5.  Upload an Image to Predict
- Once the app is running, you can upload a chest X-ray image (in .jpg, .png, or .jpeg format).
- The app will show the prediction (Pneumonia or Normal) along with the confidence for each model.
- It will also display relevant metrics (accuracy, confusion matrix, etc.) for each model.

# Model Performance
The models were evaluated based on the following metrics:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC


The CNN model provides the best performance, followed by Logistic Regression. The SVM model was included as an additional benchmark but was not the top performer for this dataset.

# Conclusion
This project demonstrates how to detect pneumonia from chest X-ray images using deep learning and traditional machine learning techniques. The Streamlit app allows users to easily upload X-ray images and get predictions using the trained models.

Feel free to modify the code, train the models on new datasets, or deploy the app for real-world use.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

