# NanoRise

NanoRise focuses on empowering nano-entrepreneurs such as vegetable vendors, small grocery store owners, and laundry service providers by utilizing AI-driven credit scoring systems. It leverages alternative data sources like UPI transactions, social feedback, and business performance metrics to assess creditworthiness.

---

## Video Demo

[![Watch the Video Demo](https://via.placeholder.com/150)](your-video-demo-link)

---

## Project Presentation

[NanoRise Presentation](https://www.canva.com/design/DAGXErtOwNo/6VFu6QZjQojSZ-PosC2ZRg/edit?ui=eyJEIjp7IlAiOnsiQiI6ZmFsc2V9fX0)

---

## Deployed Application

[https://nano-rise.vercel.app/](https://nano-rise.vercel.app/)

---

## Technologies Used

- **Frontend**: React.js, Vite
- **Backend**: Node.js, Express.js
- **Machine Learning**: Python, scikit-learn, TensorFlow
- **Database**: PostGres
- **Deployment**: Vercel
- **APIs**: Google Maps API (for address verification), Gemini API (AI Financial Advices)

---

## Project Process

1. **Data Collection**:
   - Aggregated alternative data sources such as UPI transactions, shop images, and customer feedback.
   - Utilized APIs like Google Maps API for geolocation and address validation.

2. **Data Preprocessing**:
   - Cleaned transaction data by handling missing values, outliers, and formatting inconsistencies.
   - Preprocessed shop and street view images using TensorFlow-based models for resizing, normalization, and feature extraction.
   - Applied Natural Language Processing (NLP) techniques to analyze qualitative feedback for sentiment analysis.

3. **Model Development**:
   - Designed an ensemble model using scikit-learn's `RandomForestClassifier` and TensorFlow-based neural networks.
   - Divided features into subsets to ensure diversity in predictions and reduce overfitting.
   - Combined predictions from multiple models to achieve high accuracy and robust credit scoring.

4. **Backend Development**:
   - Created RESTful APIs with Node.js and Express.js to handle data input, storage, and interaction with the ML models.
   - Integrated PostGres for scalable and efficient storage of transactional, feedback, and geolocation data.
   - Implemented real-time updates using webhooks for feedback form submissions.

5. **Frontend Development**:
   - Built a responsive user interface with React.js and Vite to allow entrepreneurs to input data and view their credit scores.
   - Designed interactive dashboards to visualize UPI transaction trends, feedback analysis, and address verification results.

6. **Deployment**:
   - Deployed the application on Vercel for seamless access and scalability.
   - Configured continuous integration/continuous deployment (CI/CD) pipelines to automate updates.
