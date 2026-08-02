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



## #4 Data Preprocessing

#### Important Note

*Data Leakage Prevention*


- We first should Train_test_split our data and get the median (mean) of the X_train and apply it to the X_test to prevent from data leakage.

- build a column transform pipleline to handle numerical columns with standardScaler and categorical columns with OneHotEncoder

- We've Decided that because at this moment we have near 50 data points I should have less categorical data because when I OneHotEncode I get lots of features and cause Overfitting.

## #5 Baseline Model

**When I run a Linear Regression to this data my R2_score for training was like 0.7176106632234047, but when it came to test I GOT NEGATIVE R2_score suggesting that I for sure Overfitted my model**



- one silly thing That I was doing, I was misplacing in r2_score the y_pred and y_true placement.

  
*first y_true then y_pred*


Now the problem is **Underfitting**, my training r2_score is less than my test r2_score so I should try with better models and gather more data points for my model.


## #6 Model Selection
## #7 HyperParameter Tuning
## #8 Training The best Model
## #9 Model Evaluation


### @ Mehdi

- [x]  چک کردن درست بودن دیتا ها با توجه به لینکهایی که در هر سطر قرار داره
- [ ]  ذخیره و تهیه لینک های مربوط به ماشین `کیا ریو`
- [x]  بررسی داده های گمشده با توجه به لینک های هر سطر
- [x]  تغییر سال های شمسی به میلادی و یک دست کردن سالهای تولید
