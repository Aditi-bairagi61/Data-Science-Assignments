# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 22:42:20 2023

@author: Dnyaneshwari...
"""
#Problem Statement:
'''
2.	Perform clustering for the crime data and identify the number of clusters            
formed and draw inferences. Refer to crime_data.csv dataset.
'''

###################################################################
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

################################################

df=pd.read_csv("C:/Datasets/Crime_data.csv")
df
df.describe()
df.columns


#################################################################

#1.Business objectives
#To perform clustering and KMeans for Crime_data .
#To draw the inference.

#2.Business Constraints


##################################################################

#2. Work on each feature of the dataset to create a data dictionary 
#as displayed in the below image:

df.columns
dic={   'Feature_Name':['ID#', 'Murder', 'Qual_miles', 'cc1_miles', 'cc2_miles', 'cc3_miles',
       'Bonus_miles', 'Bonus_trans', 'Flight_miles_12mo', 'Flight_trans_12',
       'Assault', 'Award?'],
         'Description':'Columns',
         'Type':['Quantitative','Nominal'],
         'Relevence':'Irrelevent'
     }
new_df=pd.DataFrame(dic)
#all array must be of same length
new_df
###################################################################

#3. Data Pre-processing 
#Data Cleaning, Feature Engineering, etc.

df.head()
#2 FINDING DUPLICATES
#drop 
duplicates=df.duplicated()
duplicates
#output is a single column it present true otherwise false.
sum(duplicates)#0
# so no duplicates are present

#3. OUTLIERS ANALYSIS
sns.boxplot(df.Murder)
sns.boxplot(df.Flight_trans_12)
IQR=df.Murder.quantile(0.75)-df.Murder.quantile(0.25)
IQR
#73876.5

lower_limit=df.Murder.quantile(0.75) - 1.5*IQR
lower_limit
#-18410.75
upper_limit=df.Murder.quantile(0.75) + 1.5*IQR
upper_limit
#203218.75

######################################################


#OUTLIER TREATMENT
#TRIMMING

outliers_df=np.where(df.Murder > upper_limit,True, np.where(df.Murder<lower_limit,True,False)) 
outliers_df
df_trimmed=df.loc[~ outliers_df]
df_trimmed
df.shape
#(3999, 12)
df_trimmed.shape
#(3733, 12)
#therefore there are 266 outliers that is trimmed

#REPLACEMENT TECHQUIES

df_replaced=pd.DataFrame(np.where(df.Murder > upper_limit , upper_limit,np.where(df.Murder < lower_limit , lower_limit,df.Murder)))
#if values are greter than upper limit mapped to the upper limit
#if values are lower than lower limit mapped to the lower limit

sns.boxplot(df_replaced[0])

#Winsorizer
from feature_engine.outliers import Winsorizer

winsor=Winsorizer(capping_method='iqr',
                  tail='both',
                  fold=1.5,
                  variables=['Murder'])

df_t=winsor.fit_transform(df[{'Murder'}])
sns.boxplot(df['Murder'])
sns.boxplot(df_t['Murder'])


###################################################################


#4. Exploratory Data Analysis (EDA):
#4.1. Summary.
#4.2. Univariate analysis.
#4.3. Bivariate analysis.


df.columns
df.shape
#(3999, 12)

df["Murder"].value_counts()
df["Assault"].value_counts()

# the given dataset is a imMurderd dataset

###################################################################
#scatter plot
df.plot(kind='scatter', x='Bonus_miles', y='Murder') ;
plt.show()
#2D scatter plot
sns.set_style("whitegrid");
sns.FacetGrid(df, hue="ID#").map(plt.scatter, "Assault", "Murder").add_legend();
plt.show();
#pair plot
sns.pairplot(df, hue="Murder");

#########################################################

#Mean, Variance, Std-deviation,  
print("Means:")
print(np.mean(df["Murder"]))
#Mean with an outlier.
print(np.mean(np.append(df["Murder"],50)));
print(np.mean(df["Murder"]))
print(np.mean(df["Murder"]))

print("\nStd-dev:")
print(np.std(df["Murder"]))
print(np.std(df["Murder"]))
print(np.std(df["Murder"]))

print("\nMedians:")
print(np.median(df["Murder"]))

#####################################################################
'''
5. Model Building 
5.1 Build the model on the scaled data (try multiple options).
5.2 Perform the hierarchical clustering and visualize the 
clusters using dendrogram.
5.3 Validate the clusters (try with different number of 
clusters) – label the clusters and derive insights 
(compare the results from multiple approaches).

'''

from scipy.cluster.hierarchy import linkage 
import scipy.cluster.hierarchy as sch 
from sklearn.cluster import AgglomerativeClustering 


z=linkage(df, method='complete',metric='euclidean') 
plt.figure(figsize=(15,8))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Index')
plt.ylabel('Distance')

#ref help of dendrogram 
#sch.dendrogram(z)
sch.dendrogram(z,leaf_rotation=0,leaf_font_size=10)
plt.show()

#dendrogram()
#applying agglomerative clustering choosing 3 as clusters 
#from dendrogram 
#whatever has been displayed in dendrogram is not clustering 
#It is just showing number of possible clusters 
h_complete = AgglomerativeClustering(n_clusters=3,linkage='complete',affinity='euclidean').fit(df)

#apply labels to the clusters 
h_complete.labels_
cluster_labels = pd.Series(h_complete.labels_)
df['Murder'] = cluster_labels 
#we want to relocate the column 7 to 0th position 
df = df.iloc[:,[7,1,2,3,4,5,6]]
#now check the Univ1 datafraame 
df.iloc[:,2:].groupby(df.Murder).mean()

#########################################################################################

'''
6.MODEL BULDING
6.1 Build the model on the scaled data (try multiple options).
6.2 Perform K- means clustering and obtain optimum number of 
clusters using scree plot.
6.3 Validate the clusters (try with different number of clusters) 
– label the clusters and derive insights (compare the results 
from multiple approaches).


'''
#KMeans 

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

univ1=pd.read_csv("C:/Datasets/Crime_data.csv")
univ1
univ1.describe()
univ1.columns
univ=univ1.drop({'Assault'},axis=1)


def norm_fun(i):
    x=(i-i.min()) / (i.max()-i.min())
    return x

df_norm=norm_fun(univ.iloc[:,1:])
#what will be the cluster number,will it be 1,2,3,4....

TWSS=[]
k=list(range(2,8))
for i in k:
    kmeans=KMeans(n_clusters=1)
    kmeans.fit(df_norm)
    
    TWSS.append(kmeans.inertia_)
    
    
'''
kmeans inertia is also known as sum of squares errors or SSE,
calculates the sum of distances of all points within  a cluster
from the centroid of the point. it is  the diffrence between 
the observed value and the predicted value.

'''

TWSS
''' TWSS Values
[9.192835254328504,
 9.192835254328504,
 9.192835254328504,
 9.192835254328504,
 9.192835254328504,
 9.192835254328504]
'''
plt.plot(k,TWSS,'bo-');
plt.xlabel("No of Clusters(K)");
plt.ylabel("Total_within_SS(TWSS)")

'''
How to select value of k from elbow curve
when k changes from 2,3 then decrease
in TWSS is higher
when k changes from 3,4
then TWSS is decreasing slowly and from
4,5 is conseiderablely less hence take k=3
'''

model=KMeans(n_clusters=3)
model.fit(df_norm)
model.labels_
mb=pd.Series(model.labels_)
univ['Assault']=mb
univ.head()
univ=univ.iloc[:,[7,0,1,2,3,4,5,6]]
univ
univ.iloc[:,2:8].groupby(univ.Assault).mean()
univ.to_csv("C:/Datasets/Crime_data.csv",encoding='utf-8')

################################################################


#7. Write about the benefits/impact of the solution - 
#in what way does the business (client) benefit from the solution provided?