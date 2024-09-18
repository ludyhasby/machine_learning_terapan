# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xzgOgqq9r8wfy9utAB2-tbWo-zTprMll

# Predictive Analysis Solar Pannel Performance From Capacity

this analysis has goals to help company to achieve higher efficiency levels and reduce uncertainty in solar power production. And this analysis will supporting sustainability goals and reducing the dependenceies on fossil energy sorces.

The dataset used in this predictive modeling consists of 3 datasets, namely the main dataset (consisting of timestamp and %Baseline), solar irradiance dataset (primary key timestamp), and weather dataset (primary key timestamp). The data source can be accessed at [the following link](https://www.kaggle.com/competitions/preliminary-round-dac-prs-2024/data)

## Introduction
- Introduction of importance of renewable energy while massive use of electricity and energy in this current decade
- Fixed Cost of Renewable energy is relative high, so people has tendencies to use traditional or fossil energy sources
- To reach more speed on break even poin, the optimilization of solar power production must to achieve. Installing a solar system can be a big investment, so most homeowners are always looking for ways to maximize their ROI by making their installation as efficient as possible.
- The importance tools that will help is Machine Learning that want to learning based on historical solar power optimalization production, help by data of weather and solar irradiance, also time series method.

## Theoritical Framework

[Factors that effect performance of solar system](https://www.hoymiles.com/resources/blog/7-factors-that-affect-the-performance-of-your-solar-system/)
- Enviromental Factors
    - Irradiance (radiasi), amount of sunlight that hits solar panels at any given time -> positive correlation
    - Temperature, higher temperature lower the output of solar panels (based on scientifict, when solar panel heats up, voltage of semiconducting material in the panel drops, thats make reduce pannels output).
        peak efficiency betwee 15 - 35 degree celcius
    The both seems counterintutive, but the solution suggestion as below
        - give the gap between panels and roof so the air can easily circulate
        - using microinvertes, to improce overall efficiency and reliabilty of solar system, the microinvertes will installed at underneath of the pannel that means ther're always in shade.
        - using light colored roofing that reflect sunlight aroung panel
- Equipment
    - Solar penel degradations (overall, can expect panenls to degrade at rate of 8-14% during first 25 years after installed.)
    - solar panel orientation and tilt
        the keys are calculating azimuth angle (compass direction from which the sun is hinning, placing pannels at tilt that keeps perpendicualr to the sun)
        - if on north equator, pannels shoud be facing south
        ![Pannel Orientation Suggestion](equipment_orientation.jpg)
    - shading and soliling (if can, dont shading lah, shade of thing from sun, dirt, or dust). Solution about temperature is using microinverter
    - Inverter Efficiency
        - conversion efficiency
        - MPPT efficiency

## Data Understanding
Heres are data that provided
- %Baseline : percentage of energy generated in one hour based on the energy storage capacity (Respons Variables)
- Timestamp (year, month, date, and hour)

### Solar_Irradiance
- DHI (Diffuse Horizontal Irradiance): Quantity of solar radiation received pwe unit area by a horizontal surface from all directions except the sun which has been scattered by molecules and particles in the atmosphere (Watt per Square Metre).
- DNI (Direct Normal Irradiance): Quantity of solar radiation received per unit area by surface amintained perpendicular to rays that come in straight line from sun current position in sky.
- GHI (Global Horizontal Irradiance): Combination of DHI and DNI that follow this bellow formula:
    GHI = DHI + DNI * Cos(θz) | θz stand for solar zenith angle.
- Clearsky DHI: DHI radiation under clear sky condition
- Clearsky DNI: DNI radiation under clear sky condition
- Clearsky GHI: GHI radiation under clear sky conditions. (Watt per square metre)
- Cloud Type: Classification of cloud types at the time of measurement: Clear
- Dew Point (titik embun): The temperature at which the air becomes saturated with moisture and water vapor begins to condense. (Celcius)
- Solar Zenith Angle: The angle between the sun’s rays and the vertical direction other than the solar elevation angle. (Degree)
- Surface Albedo : Index of shortwave radiation reflected from the ground or surface.
- Wind Speed: Wind speed at the time of measurement. (Metre per second)
- Relative Humidity: The amount of moisture in the air compared to what the air can hold at its current temperature. (Percentage)
- Temperature: Air temperature at the time of measurement. (Celsius)
- Pressure: Atmospheric pressure at the time of measurement. (Millibar)

### Weather
- maxtempC: Maximum temperature point of a region during a specific period. (Celsius)
- mintempC: Minimum temperature point of a region during a specific period. (Celsius)
- totalSnow_cm: Total accumulated snow height. (Centimetres)
- sunHour: Estimated total hours of sunlight.
- uvIndex: UV light index generated by the sun.
- moon_illumination: Moon illumination percentage (percentage of the moon's surface exposed to sunlight).
- moonrise: Moonrise time.
- moonset: Moonset time.
- sunrise: Sunrise time.
- DewPointC: The temperature at which the air gets saturated with moisture and water vapor starts to condense. (Celsius)
- FeelsLikeC: Perceived temperature by considering factors such as air temperature
- HeatIndexC: The perceived heat index that is hotter than the actual air temperature due to the humidity factor. (Celsius)
- WindChillC: The perceived wind chill index that is colder than the actual air temperature due to wind factors. (Celsius)
- WindGustKmph: Maximum wind gust speed. (Kilometre per hour)
- cloudcover: Percentage of cloud coverage.
- humidity: Percentage of air humidity.
- precipMM: Total precipitation (in one square metre of flat area with collected rainwater to a certain height in millimetre)
- pressure: Air pressure. (Millibar)
- tempC: Air temperature at the time of measurement. (Celsius)
- visibility: Range of vision. (Kilometre)
- winddirDegree: Wind direction. (Degree)
- windspeedKmph: Average wind speed. (Kilometre per hour)

## Library Loading
"""

STATE = 123
import pandas as pd # dataframe handling
import matplotlib.pyplot as plt # visualisasi
import seaborn as sns # also visualization, more style
import numpy as np # math handling
from sklearn.preprocessing import  OneHotEncoder # buat data preprocessing one hot encoding
from sklearn.decomposition import PCA # handling Principle Component Analysis
from sklearn.model_selection import (train_test_split, KFold, cross_val_score as cvs,
    cross_val_predict as cvp,
) # cross val, scoring, KFold
from sklearn.preprocessing import StandardScaler # standardization
from sklearn import ensemble, linear_model # for ensemble learning, ridge as linear
import xgboost as xgb # xgb
import lightgbm as lgbm # Light Gradient Boosting Machine
import catboost as cb # Cat boost
from sklearn.metrics import mean_squared_error as mse # handling evaluation metric (bridging to RMSE)
import time # handling time
from sklearn.preprocessing import PolynomialFeatures # making polynomials
import optuna # hypertunning
from sklearn.svm import NuSVR # NUSVR model

"""## Data Wrangling

### Sample Submission
"""

# read submission format
sample_submission = pd.read_csv(r"dataset\sample_submission.csv")

# count submission
len(sample_submission)

"""### Train"""

# read train data
train = pd.read_csv(r"dataset\train.csv")

# Train Data top 5 by index
train.head()

# Overview data that will be train
banyakTrain = len(train)
firstDateTrain = train.iloc[0, 0]
lastDateTrain = train.iloc[-1, 0]
print(f"Banyak data pada train {banyakTrain}, \nTanggal pada data pertama {firstDateTrain}\nTanggal pada data terakhir {lastDateTrain}")

train.dtypes # type of each columns of train

# So that can be Integrate Later
train["Timestamp"] = pd.to_datetime(train["Timestamp"]) # after some trials it can be without format

"""### Test"""

# read test set that will be submit
test = pd.read_csv(r"dataset/test.csv")

# overview of testing set
banyakTest = len(test)
firstDateTest = test.iloc[0, 0]
lastDateTest = test.iloc[-1, 0]
print(f"Banyak data pada train {banyakTest}, \nTanggal pada data pertama {firstDateTest}\nTanggal pada data terakhir {lastDateTest}")

"""Here, we can see data that will test is data of forecasting of train data, not data based on random date."""

# So that can be Integrate Later
test["Timestamp"] = pd.to_datetime(test["Timestamp"]) # after some trials and checks it can be without format

"""### Weather"""

# read weather data
weather = pd.read_csv(r"dataset\Weather.csv")

# top 5 weather data by index
weather.head()

# check types of each columns of weather data
weather.dtypes

# change date_time types to datetime without format, because it can learn the format
weather["date_time"] = pd.to_datetime(weather["date_time"])

"""### Solar Irradiance"""

# read data solar irradiance each year (2014-2017)
si_2014 = pd.read_csv(r"dataset\solar-irradiance\Solar_Irradiance_2014.csv")
si_2015 = pd.read_csv(r"dataset\solar-irradiance\Solar_Irradiance_2015.csv")
si_2016 = pd.read_csv(r"dataset\solar-irradiance\Solar_Irradiance_2016.csv")
si_2017 = pd.read_csv(r"dataset\solar-irradiance\Solar_Irradiance_2017.csv")

# check number data of each year
m = 2014
for i in [si_2014, si_2015, si_2016, si_2017]:
    print(f"Number data and columns Solar Irradiance {m}: {len(i)}, {len(i.columns)}")
    m += 1

"""we will merge data, as the data same between columns as notes 2016 has more on data, because it is cabisat year (so plus 1 day or 24 hour) then surplus for 24 data."""

# merge into one data
solar_irradiance = pd.concat([si_2014, si_2015, si_2016, si_2017])

# Number SI total data
len(solar_irradiance)

# top 5 data solar irradiance by index
solar_irradiance.head()

# check data type of each columns
solar_irradiance.dtypes

# check wheather data that has minutes more than 0
solar_irradiance[solar_irradiance["Minute"]>0]
## it is safe

# new column call as next_datetime to integrate some features in order to concatenate with other data in next chapter
solar_irradiance["next_datetime"] = solar_irradiance["Year"].astype(str) + "/" + solar_irradiance["Month"].astype(str) + "/"+ solar_irradiance["Day"].astype(str) + "/"+ solar_irradiance["Hour"].astype(str) + "/"+ solar_irradiance["Minute"].astype(str)

# check next_datetime column
solar_irradiance["next_datetime"][-10:]

# convert next_datetime to datetime with the format
solar_irradiance["date_time"] = pd.to_datetime(solar_irradiance["next_datetime"], format="%Y/%m/%d/%H/%M")

# drop some unnecassary or bridging columns
solar_irradiance = solar_irradiance.drop(["next_datetime", "Minute"], axis=1)

"""### Final Data (Integrate 2 Data)

After do trials and checking in order to better interpolate, it would be integrate data weather and train, testing. Meanwhile Solar Irradiance would be treatment as missing value first then integrate with other data.

#### Train
"""

# Show amount of data from train
len(train)

# merge with weather
train = train.merge(weather, left_on='Timestamp', right_on='date_time', how='inner')
# drop double columns
train = train.drop(["date_time"], axis=1)

# Recheck again
len(train)

"""#### Test"""

# Show amount of data from test
len(test)

# merge with weather
test = test.merge(weather, left_on='Timestamp', right_on='date_time', how='inner')
# drop double columns
test = test.drop(["date_time"], axis=1)

# check again
len(test)

"""## Exploratory Data Analysis

### Acessing Data

#### Train
"""

# checking data type of each columns
train.dtypes

# descriptive analysis of numerical columns
train.describe()

# check whether data that baseline more than 1
train[train["% Baseline"]>1]

"""- % Baseline: There are some value that out of 1, maybe it is seems not make sense because outside of range (0-1), but if we look at number of data only 3 and it maybe can outside of energy capacity.

#### Test
"""

# descriptive analysis of numerical columns
test.describe()

"""### Handling Missing Value"""

# Checking Missing Value of train set
train.isnull().sum()

# Checking Missing Value of testing set
test.isnull().sum()

# Checking Missing Value of solar irradiance set
solar_irradiance.isnull().sum()

# check whether the null value in same data or not in columns that null (Cloud Type as base columns)
solar_irradiance[solar_irradiance["DHI"].isnull() & solar_irradiance["DNI"].isnull() & solar_irradiance["GHI"].isnull() & solar_irradiance["Clearsky DHI"].isnull() & solar_irradiance["Clearsky DNI"].isnull() & solar_irradiance["Clearsky GHI"].isnull() & solar_irradiance["Cloud Type"].isnull()][["date_time", "Cloud Type"]]

"""from that we conclude that 977 data null at same data point"""

# Intepolate Numeric columns as average between previous and next data
solar_irradiance[['DHI', 'DNI', 'GHI', 'Clearsky DHI', 'Clearsky DNI', 'Clearsky GHI']] = solar_irradiance[['DHI', 'DNI', 'GHI', 'Clearsky DHI', 'Clearsky DNI', 'Clearsky GHI']].interpolate(limit_direction='both')

# data type supecious
solar_irradiance[solar_irradiance["Cloud Type"]=='Unknown']

# change unknown as Null
solar_irradiance["Cloud Type"].replace('Unknown', None, inplace=True)

# take index for each null data of cloud type
tes_indeks = solar_irradiance[solar_irradiance["Cloud Type"].isnull()].index

# Count how many data that potentially interpolate both size, the idea of the privous cloud type and the next data is same
counter = 0
for i in tes_indeks:
    if pd.isna(solar_irradiance.iloc[i, 10]) & pd.notna(solar_irradiance.iloc[i-1, 10]) & pd.notna(solar_irradiance.iloc[i+1, 10]) & (solar_irradiance.iloc[i-1, 10]==solar_irradiance.iloc[i+1, 10]):
        counter += 1
print(counter)

# Interpolasi kolom kelas dengan nilai sebelumnya (because its same if we fill the privious reseach first, then interpolate the others)
solar_irradiance["Cloud Type"] = solar_irradiance["Cloud Type"].interpolate(method='pad', limit_direction="forward")

# Recheck the null each columns
solar_irradiance.isnull().sum()

# merge with Solar Irradiance
train = train.merge(solar_irradiance, left_on='Timestamp', right_on='date_time', how='inner')
train = train.drop(["date_time"], axis=1)

# Recheck data
len(train)

"""#### Terapkan pada data testing"""

# merge with Solar Irradiance
test = test.merge(solar_irradiance, left_on='Timestamp', right_on='date_time', how='inner')
test = test.drop(["date_time"], axis=1)

# Recheck data
len(test)

"""### Univariate Analysis"""

# look the columns name
train.columns

# information of training set
train.info()

# columns that data types as object
object_columns = ['moonrise', 'moonset', 'sunrise', 'sunset', 'Cloud Type']

# columns that not belongs as object
numerical_columns = []
for i in train.columns:
    if (i not in object_columns) & (i != "Timestamp"):
        numerical_columns.append(i)

"""#### Cloud Type"""

# Amount of data each cloud type
jumlah_tipe = train["Cloud Type"].value_counts()
persentase_tipe = 100*train["Cloud Type"].value_counts(normalize=True)
df_ct = pd.DataFrame({'jumlah sampel': jumlah_tipe, 'persentase(%)': persentase_tipe})
print(df_ct)
jumlah_tipe.plot(kind='bar', title="Amount of Data by Cloud Type")

# Distribution of each columns
train.hist(bins=50, figsize=(20,15))
plt.show()

"""From these histogram we can conclude some notes:
- % Baseline : Data has tendencies in below, that means so many pannel less optimal, the data distribution is right skew that will implicate to the model

### Multivariate Analysis
show relationship two or more variables.

#### Object Columns: Cloud Type
mean of % Baseline each cloud type, want to know which one has tendencies on more % baseline and which one less.
"""

# % Baseline each Cloud type
mean_baseline = train.groupby('Cloud Type')['% Baseline'].mean().sort_values(ascending=False).reset_index()
# Plot the sorted bar chart
sns.catplot(x='Cloud Type', y='% Baseline', data=mean_baseline, kind='bar',
            dodge=False, height=4, aspect=3, palette="Set3")
plt.title("Mean of % Baseline relative to Cloud Type")

"""#### Numerical Features"""

# name of each features to recheck
train.columns

# make three columns to handling amplitude
train['wind_speed_cos_angle'] = train['Wind Speed'] * np.cos(np.deg2rad(train['winddirDegree']))
train['wind_speed_sin_angle'] = train['Wind Speed'] * np.sin(np.deg2rad(train['winddirDegree']))
train['wind_speed_solar_interaction'] = train['Wind Speed'] * (90 - train['Solar Zenith Angle'])
train['angle_diff'] = np.abs(train['winddirDegree'] - train['Solar Zenith Angle'])

# working on the testing set
test['wind_speed_cos_angle'] = test['Wind Speed'] * np.cos(np.deg2rad(test['winddirDegree']))
test['wind_speed_sin_angle'] = test['Wind Speed'] * np.sin(np.deg2rad(test['winddirDegree']))
test['wind_speed_solar_interaction'] = test['Wind Speed'] * (90 - test['Solar Zenith Angle'])
test['angle_diff'] = np.abs(test['winddirDegree'] - test['Solar Zenith Angle'])

# adding the additional features into list of numerical_columns
numerical_columns.extend(["wind_speed_cos_angle", "wind_speed_sin_angle", "wind_speed_solar_interaction", "angle_diff"])

correlation = train[numerical_columns].corr()['% Baseline'].sort_values(ascending=False)
correlation = correlation.drop(["% Baseline"])
plt.figure(figsize=(15, 6))
sns.barplot(x=correlation.index, y=correlation.values, palette='coolwarm')
plt.xlabel('Correlation')
plt.ylabel('Features')
plt.xticks(rotation=45, ha='right')
plt.title('Correlation of Numerical Features with % Baseline')
plt.show()

# heatmap of numerical columns
plt.figure(figsize=(20, 20))
corr_matrix = train[numerical_columns].corr().round(2)
# untuk print nilai dalam kotak
sns.heatmap(data=corr_matrix, annot=True, cmap='coolwarm',linewidths=0.5,)
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

"""Drop of less correlation would be skip first, because who know it will use to reveal non linear relation like in decision tree.

## Data Preprocessing

### Feature Engineering

#### Season
"""

plt.plot(train["Timestamp"], train["% Baseline"])
plt.title("Distribution of % Baseline with Timestamp")
plt.xticks(rotation=90, ha='right')

train["Timestamp"].describe()

test["Timestamp"].describe()

coba = train.copy()
coba['period'] = pd.to_datetime((train["Timestamp"].dt.year).astype(str) +"-" + train["Timestamp"].dt.month.astype(str) + "-"+"01")

train['Season'] = np.where(
    (train["Timestamp"].dt.month > 11) | (train["Timestamp"].dt.month < 3), "winter",  # Musim Dingin (Desember - Februari)
    np.where(
        train["Timestamp"].dt.month < 6, "spring",  # Musim Semi (Maret - Mei)
        np.where(
            train["Timestamp"].dt.month < 9, "summer",  # Musim Panas (Juni - Agustus)
            "autumn" # Musim Gugur (September - November)
        )
    )
)

tes = train.groupby(['Season'])['% Baseline'].mean().reset_index()

plt.figure(figsize=(2, 3))
plt.bar(tes["Season"], tes["% Baseline"])
plt.title("Mean of % Baseline relative to Season")
plt.xticks(rotation=60)

# Working on testing set
test['Season'] = np.where(
    (test["Timestamp"].dt.month > 11) | (test["Timestamp"].dt.month < 3), "winter",  # Musim Dingin (Desember - Februari)
    np.where(
        test["Timestamp"].dt.month < 6, "spring",  # Musim Semi (Maret - Mei)
        np.where(
            test["Timestamp"].dt.month < 9, "summer",  # Musim Panas (Juni - Agustus)
            "autumn" # Musim Gugur (September - November)
        )
    )
)

train.drop('Season', axis=1, inplace=True)
test.drop('Season', axis=1, inplace=True)

"""#### sun_hour and moon_hour"""

# look at selected columns
train[["Timestamp", 'moonrise', 'moonset', 'sunrise', 'sunset']]

# change sunrise features into datetime format
train["sunrise"] = pd.to_datetime(train["Timestamp"].dt.date.astype(str) + " " + train["sunrise"], format="%Y-%m-%d %I:%M %p")
train["sunset"] = pd.to_datetime(train["Timestamp"].dt.date.astype(str) + " " + train["sunset"], format="%Y-%m-%d %I:%M %p")

# Working on testing set
test["sunrise"] = pd.to_datetime(test["Timestamp"].dt.date.astype(str) + " " + test["sunrise"], format="%Y-%m-%d %I:%M %p")
test["sunset"] = pd.to_datetime(test["Timestamp"].dt.date.astype(str) + " " + test["sunset"], format="%Y-%m-%d %I:%M %p")

# After checking, we decide to manipulate with change "no moonrise" into moonset (vice versa)
train.loc[train['moonrise'] == 'No moonrise', 'moonrise'] = train.loc[train['moonrise'] == 'No moonrise', 'moonset']
train.loc[train['moonset'] == 'No moonset', 'moonset'] = train.loc[train['moonset'] == 'No moonset', 'moonrise']

# Working on testing set
test.loc[test['moonrise'] == 'No moonrise', 'moonrise'] = test.loc[test['moonrise'] == 'No moonrise', 'moonset']
test.loc[test['moonset'] == 'No moonset', 'moonset'] = test.loc[test['moonset'] == 'No moonset', 'moonrise']

# change moonrise & moonset features into datetime format
train["moonset"] = pd.to_datetime(train["Timestamp"].dt.date.astype(str) + " " + train["moonset"], format="%Y-%m-%d %I:%M %p")
train["moonrise"] = pd.to_datetime(train["Timestamp"].dt.date.astype(str) + " " + train["moonrise"], format="%Y-%m-%d %I:%M %p")

# Working on testing set
test["moonset"] = pd.to_datetime(test["Timestamp"].dt.date.astype(str) + " " + test["moonset"], format="%Y-%m-%d %I:%M %p")
test["moonrise"] = pd.to_datetime(test["Timestamp"].dt.date.astype(str) + " " + test["moonrise"], format="%Y-%m-%d %I:%M %p")

# recheck the columns after manipulate
train[["Timestamp", 'moonrise', 'moonset', 'sunrise', 'sunset']].head()

# sun_hour di train set
train["sun_hour"] = np.where((train["Timestamp"] > train["sunrise"]) & (train["Timestamp"] < train["sunset"]), 1, 0)
# sun_hour di test set
test["sun_hour"] = np.where((test["Timestamp"] > test["sunrise"]) & (test["Timestamp"] < test["sunset"]), 1, 0)

# moon hour di train set
train["moon_hour"] = np.where((train["Timestamp"] > train["moonrise"]) & (train["Timestamp"] < train["moonset"]), 1, 0)
# sun_hour di test set
test["moon_hour"] = np.where((test["Timestamp"] > test["moonrise"]) & (test["Timestamp"] < test["moonset"]), 1, 0)

"""#### Long Day (Panjang Hari Relatif dengan Matahari)"""

# making new features into training set
train["long_day_minutes"] = (train["sunset"] - train["sunrise"]).dt.total_seconds()/60

# making new features into testing set
test["long_day_minutes"] = (test["sunset"] - test["sunrise"]).dt.total_seconds()/60

"""#### Morning, Noon, Afternoon"""

# making new features, the idea is about the day divide into 4 parts (evening, morning, noon, and afternoon)
train["intense_sunrise"] = np.where(train["sun_hour"]==0, "evening",
                                   np.where(
                                       train["Timestamp"].dt.hour < train["sunrise"].dt.hour+(train["sunset"].dt.hour - train["sunrise"].dt.hour)/3, "morning",
                                       np.where(
                                           train["Timestamp"].dt.hour <= train["sunrise"].dt.hour+(train["sunset"].dt.hour - train["sunrise"].dt.hour)*2/3, "noon", "afternoon"
                                       )
                                   )
                                   )

intense_sunrise = train.groupby("intense_sunrise")["% Baseline"].mean().reset_index()
sns.catplot(x='intense_sunrise', y='% Baseline', data=intense_sunrise, kind='bar',
            dodge=False, height=4, aspect=3, palette="Set3")
plt.title("Mean of % Baseline relative to Day Division")

# working on testing set
test["intense_sunrise"] = np.where(test["sun_hour"]==0, "evening",
                                   np.where(
                                       test["Timestamp"].dt.hour < test["sunrise"].dt.hour+(test["sunset"].dt.hour - test["sunrise"].dt.hour)/3, "morning",
                                       np.where(
                                           test["Timestamp"].dt.hour <= test["sunrise"].dt.hour+(test["sunset"].dt.hour - test["sunrise"].dt.hour)*2/3, "noon", "afternoon"
                                       )
                                   )
                                   )

# One hot encoding
train = pd.concat([train, pd.get_dummies(train['intense_sunrise'], prefix='intense_sunrise')], axis=1)
test = pd.concat([test, pd.get_dummies(test['intense_sunrise'], prefix='intense_sunrise')], axis=1)

# Dropping bridging column
train = train.drop(['intense_sunrise', 'moonrise', 'moonset', 'sunrise', 'sunset'], axis=1)
test = test.drop(['intense_sunrise', 'moonrise', 'moonset', 'sunrise', 'sunset'], axis=1)

"""#### Encoding Cloud Type"""

# One hot encoding Cloud Type
train = pd.concat([train, pd.get_dummies(train['Cloud Type'], prefix='Cloud Type')], axis=1)
test = pd.concat([test, pd.get_dummies(test['Cloud Type'], prefix='Cloud Type')], axis=1)

# Working One Hot into testing set
train.drop(["Cloud Type"], axis=1, inplace=True)
test.drop(["Cloud Type"], axis=1, inplace=True)

"""#### Time Features Extraction"""

# features of jumlah_jam is number of hours in the time after the first data
train["jumlah_jam"] = ((train["Year"] - 2014)*365.25 + (train["Month"] - 1)*30 + (train["Day"]-1))*24 + train["Hour"]

# features of jumlah_jam is number of hours in the time after the first data
test["jumlah_jam"] = ((test["Year"] - 2014)*365.25 + (test["Month"] - 1)*30 + (test["Day"]-1))*24 + test["Hour"]

# making cyclical variables make sense if patterns occur 24/7/31
def time_features(_df: pd.DataFrame, data_type:str='train') -> pd.DataFrame:
    df = _df.copy()
    hour = df["Hour"]
    dm = df["Day"]
    dw = train["Timestamp"].dt.dayofweek + 1
    month = df["Month"]
    for time, col in zip([hour, dm, dw, month], ['hour', 'dm', 'dw', 'month']):
        time_range = {
            'hour':24,
            'dm': 31,
            'dw': 7,
            'month':12,
        }
        df[f'{col}_sin'] = np.sin(time*(2*np.pi/time_range[col]))
        df[f'{col}_cos'] = np.cos(time*(2*np.pi/time_range[col]))
    return df

train = train[train["month"]>=10]

# cyclical working on training set
train_preprocess = time_features(train)

# cyclical working on testing set
test_preprocess = time_features(test)

# drop Timestamp
train_preprocess.drop(['Timestamp'], axis=1, inplace=True)
test_preprocess.drop(['Timestamp'], axis=1, inplace=True)

"""### Train Test Split"""

# make X and y division
X = train_preprocess.drop(["% Baseline"], axis=1)
y = train_preprocess["% Baseline"]

# X for testing
X_test = test_preprocess.drop(["% Baseline"], axis=1)

# splitting for train and validation and sequentials (not random)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=STATE)

# check number of data each set of data
print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in test dataset: {len(X_val)}')

"""### Standardization
It will help machine learning algorithm performance better, reaching more on convergence for numerical features
"""

# check columns that not belong into numerical_columns
for i in X_train.columns:
    if i not in numerical_columns:
        print(i)

# Adding to standardization
for i in ['Year', 'Month', 'Day', 'Hour', 'jumlah_jam', 'long_day_minutes', "local_solar_time", "hour_angle"]:
    numerical_columns.append(i)
# remove unnecassary columns
for i in ["% Baseline"]:
    numerical_columns.remove(i)

# standardization define
scaler = StandardScaler()

# fiting standardization
scaler.fit(X_train[numerical_columns])

# transform numerical columns
X_train[numerical_columns] = scaler.transform(X_train.loc[:, numerical_columns])
X_val[numerical_columns] = scaler.transform(X_val.loc[:, numerical_columns])
X_test[numerical_columns] = scaler.transform(X_test.loc[:, numerical_columns])

# checking top 5 training standardization by index
X_train[numerical_columns].head()

"""## Modelling

### Model Selection
"""

# here are models that we selected to compare them, then selected best of them, boosting with hypertunning
models = {
    'ridge': linear_model.RidgeCV(),
    'rf': ensemble.RandomForestRegressor(n_jobs=-1, random_state=STATE),
    'xgboost': xgb.XGBRegressor(n_estimators=200, random_state=STATE),
    'catboost': cb.CatBoostRegressor(verbose=0, random_state=STATE),
    'lightgbm': lgbm.LGBMRegressor(n_estimators=1000, random_state=STATE)
}

# dict for amount of error
oof_predictions = dict()

# Root Mean Square Error with Cross Validation
def get_rmse(y_pred: np.array, y_true: np.array, folds:int=5)-> np.array:
    scores=np.zeros(folds)
    dpf = int(np.ceil(len(y_pred)/folds))
    for i in range(folds):
        start = i*dpf
        end = min((i+1)*dpf, len(y_pred))
        scores[i] = mse(y_pred[start:end], y_true[start:end], squared=False)
    return scores

# Compare each model
for model_name, model in models.items():
    start = time.perf_counter()
    oof_predictions[model_name] = cvp(model, X_train, y_train)
    end = time.perf_counter()
    scores=get_rmse(oof_predictions[model_name], y_train)

    print(f"""{model_name}'s Performance in RMSE
          time: {end-start:.3f} secs
          mean: {np.mean(scores):.3f}
          std: {np.std(scores):.3f}
          max: {np.max(scores):.3f}
          min: {np.min(scores):.3f}
""")

# feature imporance of LGBM
selected_model = models['lightgbm']
selected_model.fit(X_train, y_train)

# What is Features that achieve best gain
lgbm.plot_importance(selected_model, importance_type="gain", figsize=(10, 20), title="LightGBM Feature Importance (Gain)")
plt.show()

# What is Features that often used to split the data
lgbm.plot_importance(selected_model, importance_type="split", figsize=(10, 20), title="LightGBM Feature Importance (Split)")
plt.show()

# validation of base model
y_val_pred = selected_model.predict(X_val)
# means of cross val
np.mean(get_rmse(y_val_pred, y_val))

# value of baseline under 0
sum(y_val_pred < 0)

# count value of baseline over 1
sum(y_val_pred > 1)

# change value to be 0 if under 0
for i in range(len(y_val_pred)):
    if y_val_pred[i] < 0:
        y_val_pred[i] = 0.00
# change value to be 1 if over 1
for i in range(len(y_val_pred)):
    if y_val_pred[i] > 1:
        y_val_pred[i] = 1
# checking again
sum(y_val_pred < 0)

# check again cross val of validation base model
np.mean(get_rmse(y_val_pred, y_val))

# how about train
y_pred = selected_model.predict(X_train)
for i in range(len(y_pred)):
    if y_pred[i] < 0:
        y_pred[i] = 0.00
np.mean(get_rmse(y_pred, y_train))

# How about CatBoost (as references)
selected_model = models['catboost']
selected_model.fit(X_train, y_train)

feature_importances = selected_model.get_feature_importance()
feature_names = train.columns

sorted_idx = np.argsort(feature_importances)[::]

# Plot feature importance of catboost
plt.figure(figsize=(10, 16))
plt.barh(range(len(feature_importances)), feature_importances[sorted_idx], align='center')
plt.yticks(range(len(feature_importances)), np.array(X_train.columns)[sorted_idx])
plt.title('Feature Importance')
plt.ylabel('Feature')
plt.xlabel('Importance')
plt.tight_layout() # Adjust layout to fit feature names
plt.show()

# what went wrong ? based on oof
fig, ax = plt.subplots(1, 1, figsize=(20, 5))

sns.lineplot(
    x=train["Timestamp"],
    y=y_train - oof_predictions['catboost'],
)

"""### Hypertuning
we use Optuna, smart technique called Bayesian Optimization to find best hyperparameter
"""

def objective(trial):
    params = {
        "objective": "regression",
        "metric": "rmse",
        "n_estimators":1000,
        "verbosity": -1,
        "bagging_freq":1,
        "learning_rate":trial.suggest_float("learning_rate", 1e-3, 0.1, log=True),
        "num_leaves": trial.suggest_int("num_leaves", 2, 2**10),
        "subsample":trial.suggest_float("subsample", 0.05, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.05, 1.0),
        "min_data_in_leaf": trial.suggest_int("min_data_in_leaf", 1, 100),
    }
    model = lgbm.LGBMRegressor(**params)
    model.fit(X_train, y_train)
    prediction = model.predict(X_val)
    rmse = mse(y_val, prediction, squared=False)
    return rmse

# learning based on combination parameter with objective minimize RMSE on validation
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=200)

# take best params
best_params = study.best_params

# combine inital params with best
params = {
        "objective": "regression",
        "metric": "rmse",
        "n_estimators":1000,
        "verbosity": -1,
        "bagging_freq":1 }
for i in best_params:
    params[i] = best_params[i]

# show parameters that would be used
params

# not working twice (Full Data)
params_full = {'objective': 'regression',
 'metric': 'rmse',
 'n_estimators': 1000,
 'verbosity': -1,
 'bagging_freq': 1,
 'learning_rate': 0.028466902638673276,
 'num_leaves': 233,
 'subsample': 0.42065594946727325,
 'colsample_bytree': 0.7140859781300104,
 'min_data_in_leaf': 14}

# learning by parameters given
lgbm_final = lgbm.LGBMRegressor(**params_full)
lgbm_final.fit(X_train, y_train)

# validation set
y_val_pred_lgbm = lgbm_final.predict(X_val)
get_rmse(y_val_pred_lgbm, y_val)

# mean of cross val
np.mean(get_rmse(y_val_pred_lgbm, y_val))

# sum of under 0
sum(y_val_pred_lgbm < 0)

# set to be 0 like above
for i in range(len(y_val_pred_lgbm)):
    if y_val_pred_lgbm[i] < 0:
        y_val_pred_lgbm[i] = 0.00

# updating score
np.mean(get_rmse(y_val_pred_lgbm, y_val))