![Figure1](<back.jpg>)

# Kia Rio Price Prediction
A regression project that scrapes, cleans, and analyzes Kia Rio listing data to predict resale price — with a deployed Streamlit app for interactive predictions.

## Summary
- Goal: Predict Kia Rio resale price from listing data (mileage, date, color, insurance time, etc.)
- Best model: Linear Regression
- Result: R² ≈ 0.70 on both train and test sets, with no meaningful overfitting
- Key drivers: mileage and date were the most important predictors of price



## Project Structure:
```
├── Data/            # Scraping scripts and raw/cleaned CSVs
├── EDA/              # Exploratory data analysis notebooks
├── PreProcessing/     # Data cleaning and pipeline construction
├── Model/             # Model training, selection, and evaluation
├── Deployment/        # Streamlit app code
├── requirements.txt
└── README.md
```


## How to Run:

### 1. clone the repo and install dependencies: 
```
   git clone https://github.com/pouniq/CarPred.git
   cd CarPred
   pip install -r requirements.txt
```

### 2. Scrape fresh data

```
   cd Data
   python scraped_one_page.py   # provide listing URLs as input
   python csv_modification.py   # produces a cleaned CSV
```
### 3. running the deployed app

```
   cd Deployment
   streamlit run app.py

```

## Methodology
### Data

Listing data was scraped for Kia Rio cars and consolidated into a single cleaned CSV.

#### Exploratory Data Analysis
- The target variable (price) had a skewed distribution, which motivated a log transform later in the pipeline.
- ~30 missing values were found in the insurance column.
- Outliers were identified in price, including several listings that turned out not to be Kia Rios at all — these were removed after further inspection.
- date and mileage emerged as the strongest predictors of price.


#### Preprocessing

- Applied train_test_split before computing any statistics (medians/means) to prevent data leakage — training-set statistics are reused on the test set, never recomputed on it.
- Built a ColumnTransformer pipeline: StandardScaler for numerical features, OneHotEncoder for categorical features.
- With only ~200 data points, categorical cardinality was kept low to avoid overfitting from one-hot encoding — e.g., color was engineered into a binary Light/Dark feature, while the original color column was preserved alongside it for reference.


#### Modeling
- Baseline: Linear Regression, which performed well out of the box.
- Compared: Ridge Regression, SVM, Gradient Boosting, and Random Forest — Linear Regression had the lowest RMSE.

Hyperparameter tuning: Tested Ridge regularization strengths; the optimal alpha converged to 0, confirming plain Linear Regression as the best choice.


Target transform: Used TransformedTargetRegressor to apply np.log/np.exp automatically within the pipeline:

```python
  pipe_svr = Pipeline([
      ('process', processor),
      ('model', SVR())
  ])

  model_log = TransformedTargetRegressor(
      regressor=pipe_svr,
      func=np.log,
      inverse_func=np.exp
  )
```
## Results

Final Linear Regression model achieved R² ≈ 0.70 on both train and test sets, indicating a reasonable fit without overfitting given the dataset size.

## Deployment

The final model is deployed as an interactive Streamlit app: 

[STREAMLIT APP](carpred2.streamlit.app)

## Notes

Data verification and collection tasks were tracked collaboratively (link validation, listing accuracy checks, Persian-to-Gregorian year conversion for consistent production years).

