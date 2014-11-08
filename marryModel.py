#-*-encoding:utf-8 -*-
from time import time
import numpy as np
import pandas as pd
from pdTransform import loadData,saveData
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale



def kmeansModel(data,filters):
	def bench_k_means(estimator,data,filters):
		estimator.fit(data)
		return estimator.labels_

	new_data=data.drop(labels=filters,axis=1)
	new_data=new_data.fillna(0).astype(float)
	new_data=scale(new_data.values)
	n_digits=5
	pca=PCA(n_components=n_digits).fit(new_data)
	results=bench_k_means(KMeans(init=pca.components_,n_clusters=n_digits,n_init=1),new_data,filters)
	data['class']=results
	return data



	



header='id|gender|age|height|edu|salary|nation|car|house|body|face|hair|\
smoke|drink|child|parent|bmi|where2|where0|where1|\
marriage0|marriage1|look0|look1'.split('|')
data=pd.read_csv('/home/idanan/jiayuan/code/pd_female1.txt',names=header,sep='|')
data=kmeansModel(data,['id','gender'])
saveData(data,'/home/idanan/jiayuan/code/cluster_female.txt')


