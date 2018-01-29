import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Import flattened CSV census data into dataframe
df = pd.read_csv('../output/flattened_census_data.csv')

#Create new helpful features
def cat_target(row):
    if row['over_50k'] == 0:
        return 'False'
    elif row['over_50k'] == 1:
        return 'True' 
    else:
        return np.NaN

df['over_50_bool'] = df.apply(cat_target, axis=1)

#Sort out numeric and categorical fields for processing
exclude_vars = ['over_50k','respondent_id']
numeric_vars = list(df._get_numeric_data().columns)
numeric_vars = [field for field in numeric_vars if field not in exclude_vars]
cat_vars = [col for col in df.columns if col not in numeric_vars and col != 'respondent_id']

print("Numeric Vars:  ")
print(numeric_vars)
print("\n")
print("Categorical Vars:  ")
print(cat_vars)

#Create Data Exploration Charts
rows,cols = df.shape
sns.set_style("whitegrid")

#Create one-way frequencies for categorical vars
for cat_var in cat_vars:
	f, ax = plt.subplots(figsize=(12,12))
	plt.title(cat_var+' frequencies')
	sns.countplot(y=cat_var, data=df, color="c")
	plt.savefig('../output/figs/freqs/'+cat_var+'_freqs.png', bbox_inches='tight')
	plt.close()

#Display by category the likelihood of a respondent earning over 50k
for cat_var in cat_vars:
	f, ax = plt.subplots(figsize=(12,12))
	plt.title(cat_var+' frequencies')
	sns.countplot(x=cat_var, hue="over_50_bool", data=df)
	plt.savefig('../output/figs/by_over50k/'+cat_var+'_by_over50k.png', bbox_inches='tight')
	plt.close()
  
#Create histograms for numeric vars
for numeric_var in numeric_vars:
	f, ax = plt.subplots(figsize=(12,12),nrows=2)
	over50=df[df.over_50_bool == 'True']
	under50=df[df.over_50_bool == 'False']
	ax[0].title.set_text('Over 50K: ' + numeric_var+' histogram')
	sns.distplot(over50[numeric_var],norm_hist=True,ax=ax[0])
	ax[1].title.set_text('Under 50K: ' + numeric_var+' histogram')
	sns.distplot(under50[numeric_var],norm_hist=True,ax=ax[1])
	plt.savefig('../output/figs/histograms/'+numeric_var+'_hist.png', bbox_inches='tight')
	plt.close()