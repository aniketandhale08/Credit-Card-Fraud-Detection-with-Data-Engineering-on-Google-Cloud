# Credit Card Fraud Detection with Data Engineering on Google Cloud

This project aims to develop a comprehensive credit card fraud detection system for Transpe Limited, a global transaction company responsible for handling transactions across multiple banks worldwide. The system utilizes historical financial and demographic data to train a machine learning model, deploys it on Vertex AI Endpoint for real-time transaction analysis, and incorporates various components to process, classify, and handle fraudulent transactions. Additionally, Looker Dashboards are created to provide detailed insights into both fraud and non-fraud transactions, enabling effective monitoring and analysis.

## Toolbox 🧰
![tools](https://github.com/user-attachments/assets/9786c138-9d54-494b-bc37-553ac0c09116)

## Overview of Tools and Their Roles

**1. BigQuery ML:** Enables advanced machine learning model training directly on large datasets stored in BigQuery and simplifies data preparation and feature engineering with SQL-based workflows.

**2. Vertex AI:** Serves as the platform for deploying the trained fraud detection model and offers a REST API endpoint for real-time predictions.

**3. Pub/Sub:** Acts as the backbone for real-time messaging, facilitating seamless data ingestion from on-prem systems to the cloud and triggering downstream processes.

**4. Dataflow:** Processes incoming transactional data in real-time, enabling transformation, enrichment, and preparation of data for further analysis.

**5. Firestore:** Provides a NoSQL document database for efficient storage and retrieval of processed transaction data, particularly for real-time applications.

**6. Looker Studio:** Creates interactive dashboards and reports to visualize transaction trends, fraud patterns, and key metrics.

**7. Cloud Functions:** Automates critical workflows, such as sending email notifications and triggering alerts based on fraud predictions.

**8. Secret Manager:** Ensures secure storage and access to sensitive credentials, such as API keys and email configuration details.

**9. Python:** Powers custom scripts for data ingestion, processing, and model interactions, providing flexibility and control over the system logic.

## Architecture Diagram
![Architecture Diagram](https://github.com/user-attachments/assets/1299b117-6b7f-4f8b-aa80-feda1aea8fc4)

## **Workflow of the Project**
![Blank diagram (1)](https://github.com/user-attachments/assets/f4fa109f-55fe-45f3-85f2-4893451c4943)

### **1. Data Preparation**
- **Data Collection**:  
  Historical and demographic transaction data stored in BigQuery is used to train the fraud detection model.
  
- **Feature Engineering**:  
  Key features include transaction type, transaction amount, balance changes, and origin/destination accounts. Features like `type`, `amount`, `oldbalanceOrig`, `newbalanceOrig`, `oldbalanceDest`, and `newbalanceDest` play a vital role in model training.
  
- **Preprocessing**:  
  - Data is cleaned to handle missing values, remove anomalies, and normalize numeric features.  
  - The data is highly imbalanced; BigQuery handles smoothing and applies one-hot encoding in the background.

### **2. Model Training**
- **BigQuery ML**:  
  - Used to train classification models such as `KMEANS`, `LOGISTIC_REGRESSION`, and `BOOSTED_TREE_CLASSIFIER`.  
  - The model learns patterns of fraudulent behavior based on labeled data in the `isFraud` column.

- **Evaluation Metrics**:  
  Metrics like **precision**, **recall**, and **F1-score** ensure the model is optimized for fraud detection accuracy.  
  Below are the metrics for the **BOOSTED_TREE_CLASSIFIER** after training.
  
![BOOSTED_TREE_CLASSIFIER metrics](https://github.com/user-attachments/assets/2a11cf20-7179-450e-a32d-59dea7298b43)

### **3. Model Deployment**
- **Vertex AI**:  
  - The trained model is deployed on Vertex AI, creating an API endpoint for real-time scoring.  
  - Vertex AI offers scalability and ensures low-latency predictions.  
  - Each transaction is scored in real time, generating a fraud probability.

### **4. Real-Time Data Pipeline**
- **Data Ingestion**:  
  Transactional data from on-prem systems is streamed into a Pub/Sub topic in real time. Data is converted to JSON format for processing.

- **Firestore**:  
  Recent transaction data is stored in Firestore for efficient monitoring and retrieval.

- **Dataflow Pipeline**:  
  A Dataflow pipeline processes the Pub/Sub messages, applies transformations, and routes the data for storage and prediction.  
  Each transaction is scored by the Vertex AI model, and predictions are appended to the data.

### **5. Fraud Detection and Alerts**
- Transactions identified as fraudulent are published to another Pub/Sub topic.
- **Cloud Function**:  
  - Listens to this topic and takes automated actions:
    - Sends email notifications to customers and banks.
    - Logs the fraud incident in an internal system for further analysis.
  - Sensitive credentials like email SMTP configurations are securely fetched from Secret Manager.

### **6. Data Storage**
- Transactions are categorized based on predictions and stored in two BigQuery tables:
  - **Fraudulent Transactions Table**: Used for further investigation, analytics, and notification purposes.
  - **Non-Fraudulent Transactions Table**: Used for general analysis and reporting.

### **7. Dashboards and Visualization**
- **Looker Studio Dashboards**:  
  Provide comprehensive insights into transaction data:
  - Trends in fraudulent transactions over time.
  - Real-time monitoring, fraud trends, and actionable intelligence.
  - Region-wise distribution of fraud cases.
  -  [Dashboard Link](https://lookerstudio.google.com/reporting/b326b751-5eb0-46b3-a998-d7e858a2f034)

![Dashboard](https://github.com/user-attachments/assets/d1d95f7e-cbf6-4270-8721-d8ee5fb3116a)

## Email to Bank
![bank mail](https://github.com/user-attachments/assets/e61c91f7-338f-48da-bb4f-24f248f6c589)

## Email to Customer
![customer mail](https://github.com/user-attachments/assets/68eadc97-94e3-43a8-9ab0-04439bb060a3)

## **Code Structure**
```plaintext
├── Home Directory  
|   ├── Transaction_Pipeline.py
|   ├── Transaction_Pubsub.py
|   ├── fraud_data.csv
├── setup.py  
```

## **Conclusion**

Working on this project has been an incredible learning experience. I gained valuable insights into real-time data processing, machine learning, and cloud-based technologies. Using tools like BigQuery ML, Vertex AI, Dataflow, Pub/Sub, and Firestore has enhanced my technical skills and understanding of end-to-end data engineering workflows.

I am confident that the knowledge and experience I’ve gained from this project will help me excel in future roles as a Data Engineer. This project has not only strengthened my problem-solving skills but also fueled my passion for leveraging technology to solve real-world challenges. I look forward to applying these skills and continuing to grow in this exciting field.

## Project Video
I encourage you all to watch the project video for better understanding.
- [Project Video Link](https://youtu.be/NmyJocN2kxU)


## Connect with Me
Feel free to reach out if you have any questions or want to discuss data analytics:
- [LinkedIn](https://www.linkedin.com/in/aniketandhale08/)
