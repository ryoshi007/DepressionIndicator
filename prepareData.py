import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os

data = pd.read_csv('data.csv', delimiter='\t')
data.drop(['Q1A', 'Q2A', 'Q4A', 'Q6A', 'Q7A', 'Q8A', 'Q9A', 'Q11A', 'Q12A', 'Q14A', 'Q15A', 'Q18A', 'Q19A', 'Q20A',
           'Q22A', 'Q23A', 'Q25A', 'Q27A', 'Q28A', 'Q29A', 'Q30A', 'Q32A', 'Q33A', 'Q35A', 'Q36A', 'Q39A', 'Q40A',
           'Q41A',
           'Q1I', 'Q1E', 'Q2I', 'Q2E', 'Q3I', 'Q3E', 'Q4I', 'Q4E', 'Q5I', 'Q5E', 'Q6I', 'Q6E', 'Q7I', 'Q7E', 'Q8I',
           'Q8E', 'Q9I', 'Q9E', 'Q10I', 'Q10E',
           'Q11I', 'Q11E', 'Q12I', 'Q12E', 'Q13I', 'Q13E', 'Q14I', 'Q14E', 'Q15I', 'Q15E', 'Q16I', 'Q16E', 'Q17I',
           'Q17E', 'Q18I', 'Q18E', 'Q19I', 'Q19E', 'Q20I', 'Q20E',
           'Q21I', 'Q21E', 'Q22I', 'Q22E', 'Q23I', 'Q23E', 'Q24I', 'Q24E', 'Q25I', 'Q25E', 'Q26I', 'Q26E', 'Q27I',
           'Q27E', 'Q28I', 'Q28E', 'Q29I', 'Q29E', 'Q30I', 'Q30E',
           'Q31I', 'Q31E', 'Q32I', 'Q32E', 'Q33I', 'Q33E', 'Q34I', 'Q34E', 'Q35I', 'Q35E', 'Q36I', 'Q36E', 'Q37I',
           'Q37E', 'Q38I', 'Q38E', 'Q39I', 'Q39E', 'Q40I', 'Q40E',
           'Q41I', 'Q41E', 'Q42I', 'Q42E', 'country', 'source', 'introelapse', 'testelapse', 'surveyelapse', 'TIPI1',
           'TIPI2', 'TIPI3', 'TIPI4', 'TIPI5', 'TIPI6', 'TIPI7',
           'TIPI8', 'TIPI9', 'TIPI10', 'VCL1', 'VCL2', 'VCL3', 'VCL4', 'VCL5', 'VCL6', 'VCL7', 'VCL8', 'VCL9', 'VCL10',
           'VCL11', 'VCL12', 'VCL13', 'VCL14', 'VCL15', 'VCL16',
           'education', 'urban', 'engnat', 'hand', 'religion', 'orientation', 'race', 'voted', 'familysize', 'major',
           'screensize', 'uniquenetworklocation'], axis=1, inplace=True)

data_1 = data.copy()
data_1['gender'] = data_1['gender'].replace(to_replace=0, value=3)
data_1['married'] = data_1['married'].replace(to_replace=0, value=3)


def condition(x):
    if x <= 10:
        return 'Under 10'
    if 10 <= x <= 16:
        return ' Primary Children'
    if 17 <= x <= 21:
        return 'Secondary Children'
    if 21 <= x <= 35:
        return 'Adults'
    if 36 <= x <= 48:
        return 'Elder Adults'
    if x >= 49:
        return 'Older People'


data_1['Age_Groups'] = data_1['age'].apply(condition)

new_data = data_1.iloc[:, 14:]
data_2 = data_1.filter(regex='Q\d{1,2}A')


def sub(data_2):
    return data_2.subtract(1, axis=1)


data_2 = sub(data_2)
Dep_keys = {'Depression': [3, 5, 10, 13, 16, 17, 21, 24, 26, 31, 34, 37, 38, 42]}
Dep = []
for i in Dep_keys["Depression"]:
    Dep.append('Q' + str(i) + 'A')
depression = data_2.filter(Dep)


def scores(source):
    col = list(source)
    source['Total_Count'] = source[col].sum(axis=1)
    return source


depression = scores(depression)

# Depression Set
Depression = pd.merge(depression, new_data, how='left', left_index=True, right_index=True)


def condition(x):
    if x <= 9:
        return 'Normal'
    if 10 <= x <= 13:
        return 'Mild'
    if 14 <= x <= 20:
        return 'Moderate'
    if 21 <= x <= 27:
        return 'Severe'
    if x > 27:
        return 'Extremely Severe'


Depression['Condition'] = Depression['Total_Count'].apply(condition)

# Rename columns
Depression = Depression.rename(columns={'Q3A': 'Optimistic', 'Q5A': 'Motivation', 'Q10A': 'Looking-Forward',
                                        'Q13A': 'Sadness', 'Q16A': 'Interest', 'Q17A': 'Existential-Crisis',
                                        'Q21A': 'Importance', 'Q24A': 'Enjoyment', 'Q26A': 'Down-hearted',
                                        'Q31A': 'Enthusiasm', 'Q34A': 'Worthiness','Q37A': 'Hopefulness',
                                        'Q38A': 'Meaningless', 'Q42A': 'Tiredness', })

# print(Depression)

plt.figure(figsize=(10, 6))
sns.countplot(Depression.sort_values('Condition').Condition, palette='GnBu')
plt.title('People Condition of Depression Level', fontsize=15)
# plt.show()

Depr = Depression.copy()


def condition(x):
    if x <= 9:
        return 0
    if 10 <= x <= 13:
        return 1
    if 14 <= x <= 20:
        return 2
    if 21 <= x <= 27:
        return 3
    if x > 27:
        return 4


def cond(x):
    if x <= 10:
        return 0
    if 10 <= x <= 16:
        return 1
    if 17 <= x <= 21:
        return 2
    if 22 <= x <= 35:
        return 3
    if 36 <= x <= 48:
        return 4
    if x > 48:
        return 5


Depr['Condition'] = Depr['Total_Count'].apply(condition)
Depr['Age_Groups'] = Depr['age'].apply(cond)
Depr = Depr.drop(columns=['age', 'Total_Count'])
print(Depr)

Depression.to_csv('clean_data.csv', index=False)

plt.figure(figsize=(20, 20))
sns.heatmap(Depr.corr(), vmin=-1, vmax=1, cmap=sns.diverging_palette(20, 220, n=200))
# plt.show()


# Comparing different answers given for situations like gender, marriage,age etc and comparing with their Depression
# Conditions GENDER 1=Male, 2=Female, 3=Other print('Count of People participated as of Gender\n', Depression[
# 'gender'].value_counts())
plt.figure(figsize=(10, 6))
sns.countplot(Depression.sort_values('gender').gender, hue=Depression['Condition'], palette='Pastel1')
plt.title('Depression Condition of Different Gender', fontsize=15)

# MARRIAGE
# 1=Never married, 2=Currently married, 3=Previously married
# print(Depression['married'].value_counts())
plt.figure(figsize=(10, 6))
sns.countplot(Depression.sort_values('married').married, hue=Depression['Condition'], palette='GnBu_r')
plt.title('Depression Condition of People as of Married or Not', fontsize=15)
# Never Married - Mostly had extremely severe conditions for Depression and Anxiety.
# Married - Mostly were normal
# Divorced - As per the people participated Most people were in Extreme Severe for depressive state

# AGE GROUPS
# Under 10
# Primary(10-16)
# Secondary(17-21)
# Adults(21-35)
# Elder Adults(36-48)
# Older people(49+)
# print('Counts of answered recorded as per age groups\n', Depression['Age_Groups'].value_counts())
plt.figure(figsize=(10, 6))
sns.countplot(Depression.sort_values('Age_Groups').Age_Groups, hue=Depression['Condition'], palette='RdYlBu')
plt.title('Depression Condition as per different Age Groups', fontsize=15)

# plt.show()
