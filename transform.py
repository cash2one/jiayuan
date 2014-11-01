#-*-encoding:utf-8-*-
import numpy as np
import pandas as pd

FILTERS=[5]
def loadData(path):
	infos=[]
	with open(path) as f:
		for line in f:
			info=line.strip().split(' |')
			infos.append(info)
	return infos

def mapping(x):
	if x in mappy.keys():
		return mappy[x]
	else:
		return x

def departInfo(info,filters):
	info1=[info[i] for i in filters]
	info2=[info[i] for i  in range(23) if i not in FILTERS]
	return [info1,info2]

def transform(data):
	new_data=[]
	for info in data:
		info1,info2=departInfo(info,FILTERS)
		new_info=info2+map(mapping,info1)
		new_data.append(new_info)
	return new_data


def saveData(data,path):
	with open(path,'w') as f:
		for line in data:
			s=[str(i) for i in line]
			f.write(' |'.join(s)+'\n')


def quantile(array,quantiles):
	for p,v in enumerate(array):
		rate=0
		for i in quantiles:
			if v>i:
				rate+=1
			else:
				break
		array[p]=rate

	return array

def calQuantile(array,num):
	length=len(array)
	array=sorted(map(lambda x:int(x),array))
	p=int(length*num)
	return array[p]

def fourQuant(array):
	quants=[]
	for num in [0.25,0.5,0.75]:
		quants.append(calQuantile(array,num))
	return quants

def convertQuants(array):
	quants=fourQuant(array)
	array=quantile(array,quants)
	return array

def calBMI(array):
	for p,v in enumerate(array):
		if v<18 or 24<v<28:
			array[p]=0
		if 18<=v<=24:
			array[p]=1
		if v>=28:
			array[p]=-1
	return array	



def main():
	data=pd.ExcelFile('/home/idanan/jiayuan/female_data.xls').parse('sheet1')
	data['height']=convertQuants(data['height'])
	data['weight']=convertQuants(data['weight'])
	data['bmi']=pd.Series(calBMI(np.array(data['bmi']).astype(int)))
	data.to_excel('/home/idanan/jiayuan/female_data1.xls',index=False)

main()
