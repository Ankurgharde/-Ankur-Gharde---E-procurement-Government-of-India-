import pandas as pd
import numpy as np
import seaborn as sns 
import matplotlib.pyplot as plt


df1=pd.read_csv('tenders.csv')


print(df1.head())


df1.insert(0,'Sr.No',range(1,len(df1)+1))


# removing the irrelevent digit from tender title column
def fun(str1):
    s=str1[2:].strip()
    return s


df1['Tender Title']=df1['Tender Title'].apply(lambda x:fun(x))


print(df1)


print(df1.info())

#Observation: All columns have 10 non-null values, indicating that there are no missing values in the DataFrame.


df1['Tender Title'].value_counts().plot(kind='barh')


def fun1(str1):
    return str1.lower()


for i in df1.columns:
    if df1[i].dtypes==object:
        df1[i]=df1[i].apply(lambda x:fun1(x))

print(df1)

num_tenders = len(df1)
print("Number of tenders:", num_tenders)

earliest_closing_date = df1['Closing Date'].min()
tender_with_earliest_closing = df1[df1['Closing Date'] == earliest_closing_date]['Tender Title'].values[0]
print("Tender with earliest closing date:", tender_with_earliest_closing)

closing_dates_count = df1['Closing Date'].str.split().str[0].value_counts()
print("Tenders closing on each date:")
print(closing_dates_count)
most_common_reference = df1['Reference No'].mode().values[0]
print("Most common reference number:", most_common_reference)

df1['Closing Date'] = pd.to_datetime(df1['Closing Date'], format="%d-%b-%Y %I:%M %p")
df1['Bid Opening Date'] = pd.to_datetime(df1['Bid Opening Date'], format="%d-%b-%Y %I:%M %p")
time_diff = df1['Bid Opening Date'] - df1['Closing Date']
average_time_diff = time_diff.mean()
print("Average time between closing and bid opening:", average_time_diff)






