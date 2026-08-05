![Figure1](<back.jpg>)


# Cars_prediction


## #1 Problem Statement

In this project We are taking/getting Kia: Rio car prices and making Sense of that data, in the future we are putting Machine learning pipelines.







## #2 Data Source

### folder in use: `Data`
  - in `Links` folder:
1. Run `get_all_links.py` script
2. after we got the links, we run `Duplicated_links_check.py` to ensure we have unique links


*go back to `Data` folder*


3. run 'Scrape_one_page.py' script
4. after we got the output.csv, go to `csv_modification.py` to make the data into one cohesive dataframe


## #3 EDA

1. We found in My data that price (targer feature) is not
in a good place (distribution wise) so I may need to get more data
or limit and max out prices.

2. we have 7 missing values in insurance column
3. some outliers with `price` column -- think about how can you handle them
4. Most important features for `price` column, is `date` & `mileage`

5. Walk Through the EDA step again and I found out some data are Not even in Kia Rio brand And they are in here, so I deleted those and they were mostly a outlier, Now I expect that my model perform better than before.



## #4 Data Preprocessing

#### Important Note

*Data Leakage Prevention*


- We first should Train_test_split our data and get the median (mean) of the X_train and apply it to the X_test to prevent from data leakage.

- build a column transform pipleline to handle numerical columns with standardScaler and categorical columns with OneHotEncoder

- We've Decided that because at this moment we have near 50 data points I should have less categorical data because when I OneHotEncode I get lots of features and cause Overfitting.



- I turned color values to just two category Light and Dark, Now I noticed Regarding the original colors I have misjudged the color and Now I should go back to a version that have the original colors

  learned I should Always keep the original column in place when modifing and create a new column based on the original column

## #5 Baseline Model

**When I run a Linear Regression to this data my R2_score for training was like 0.7176106632234047, but when it came to test I GOT NEGATIVE R2_score suggesting that I for sure Overfitted my model**



- one silly thing That I was doing, I was misplacing in r2_score the y_pred and y_true placement.

  
*first y_true then y_pred*


Now the problem is **Underfitting**, my training r2_score is less than my test r2_score so I should try with better models and gather more data points for my model.


## #6 Model Selection

- between, Ridge Regression, Support Vector Machine, Gradient boosting Regression and Random Forest Regressor, the Choice based on R2_score is **Ridge Regression**.

- now that I got more data, the simple model of LinearRegression worked marvelously and model R2 come to near 70 percent in both train and test, that shows there is not problem of overfitting.



## #7 HyperParameter Tuning
I am gonna HyperParameter Tune Ridge Regression Parameters to get the best Result.

I choose for Now the support vector machine regressor because it have lower MSE than Ridge Regression.


there is no real need for HyperParameter tuning the linear regression, I tested Ridge regression too but the chosen alpha was 0 meaning the simple linear regression was chosen even then.


## #8 Training The best Model

the best model for now is A SVR model.


**now the best model is LinearRegression**



## #9 Model Evaluation

In Model Evaluations when you put your target variable to np.log function, then after you train the model your should np.exp to get the real world result, We know that already, One trick is to use TransformedTargetRegressor to do that automatically with PipeLine like this:

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


## #10 Deployment
I deployed my Model using Streamlit you can find it in here 👇


[App Link](https://4gm9gphzgdzfv7vgd4tda6.streamlit.app/)



### @ Mehdi

- [x]  چک کردن درست بودن دیتا ها با توجه به لینکهایی که در هر سطر قرار داره
- [x]  ذخیره و تهیه لینک های مربوط به ماشین `کیا ریو`
- [x]  بررسی داده های گمشده با توجه به لینک های هر سطر
- [x]  تغییر سال های شمسی به میلادی و یک دست کردن سالهای تولید
