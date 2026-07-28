import readme_renderer
import pandas as pd

df = pd.read_csv("cars_scraped.csv")
df

# first extract the date of production from the `car` column
# and for cars that do not have them look for that manually
date = [1390,1389,1394,1390,1394,1390,1387,1390,None,None,1396,1392,1385,None,None,1387,1390,1389,None,1389,1387,1390,1384]
