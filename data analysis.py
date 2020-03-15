# Import packages and set up parameter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False


# Load the JSON file
df = pd.read_json('book.json', encoding='utf-8')


# Dataset overview

# i. Check column information - 6 categorical columns and 2 numeric columns
# ii. Check NA values - no NA value
# iii. Calculate the discount ratio and add the column Discount
# iv. Add the column Rank

print('')
print('Dataset Overview')
print(df.info())
print('')
print('Find NA values')
print(df.isna().sum())


# Data processing
df['Discount'] = 1 - df['Price_special'] / df['Price_original']
df['Rank'] = list(df.index + 1)


# Categorical analysis - book counts

# i. All the books are in the main category of 中文書 (100)
# ii. Top-3 2nd-level categories are 商業理財 (20), 心理勵志 (19)
#      and 文學小說 (9) / 語言學習 (9)
# iii. Top-3 3rd-level categories are 語言能力檢定測驗 (8), 投資理財 (7)
#       and 人際關係 (5)
# iv. Top-3 4th-level categories are NEWTOEIC新多益 (8),
#       心靈成長 (3) / 散文 (3) / 人脈/處世 (3) ... etc

pivot_count1 = pd.pivot_table(
    data=df, index='Category_1',
    values='Name', aggfunc='count')

pivot_count1.columns = ['Counts']

pivot_count2 = pd.pivot_table(
    data=df, index=['Category_1', 'Category_2'],
    values='Name', aggfunc='count'
    ).sort_values(by='Name', ascending=False)

pivot_count2.columns = ['Counts']

pivot_count3 = pd.pivot_table(
    data=df, index=['Category_1', 'Category_2', 'Category_3'],
    values='Name', aggfunc='count'
    ).sort_values(by='Name', ascending=False)

pivot_count3.columns = ['Counts']

pivot_count4 = pd.pivot_table(
    data=df, index=['Category_1', 'Category_2', 'Category_3', 'Category_4'],
    values='Name', aggfunc='count'
    ).sort_values(by='Name', ascending=False)

pivot_count4.columns = ['Counts']


# Categorical analysis - discount ratio

# i. Top-5% discounted books
#     1. 療癒，從感受情緒開始：傷痛沒有特效藥，勇於面對情緒浪潮，就是最好的處方箋
#     2. 新制多益NEW TOEIC聽力／閱讀題庫解析【博客來獨家套書】（附4 MP3)
#     3. 新制多益 NEW TOEIC 單字大全：2018起多益更新單字資訊完全掌握！
#     4. 全新制20次多益滿分的怪物講師TOEIC多益單字+文法
#     5. 全新制怪物講師教學團隊的TOEIC多益5回全真模擬試題+解析

# ii. 4 of these books are from 語言學習 category
# iii. 1 of these books are from 心理勵志 category

df_discount_top5 = df.sort_values(
    by='Discount', ascending=False
    ).iloc[:5]

print('')
print('Top5 Discounted Books')
print(df_discount_top5[['Name', 'Discount']])

# Plot the top5 2nd-level category distribution
df_discount_top5['Category_2'].value_counts().sort_values(ascending=True).plot(
    kind='barh', figsize=(8, 4))

plt.title(
    'Category distribution for top 5 discounted books',
    size=14, fontweight='bold')

plt.xticks(np.arange(0, 5))
plt.show()

pivot_discount = pd.pivot_table(
    data=df, index='Category_2',
    values='Discount', aggfunc='mean'
    ).sort_values(by='Discount', ascending=False)

# Plot the top100 2nd-level category distribution
pivot_discount.sort_values(by='Discount', ascending=True).plot(
    kind='barh', figsize=(10, 6))

plt.title(
    'Category distribution for top100 bestseller',
    size=18, fontweight='bold')

plt.xlim(0.1, 0.3)
plt.ylabel('Category', size=12, fontweight='bold')
plt.xlabel('Discount ratio', size=12, fontweight='bold')
plt.show()

# Output the categorical information to csv files
pivot_count2.to_csv('category_counts_2level.csv', encoding='utf_8_sig')
pivot_count3.to_csv('category_counts_3level.csv', encoding='utf_8_sig')
pivot_count4.to_csv('category_counts_4level.csv', encoding='utf_8_sig')

df_discount_top5.to_csv('discount_top5.csv', index=False, encoding='utf_8_sig')
