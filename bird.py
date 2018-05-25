# -*- coding: utf-8 -*-
"""
@author: Sxx
"""
import urllib
import numpy
import MySQLdb
import re
from bs4 import BeautifulSoup
import sys

#从网络读取数据
def get_date(path):
	f=urllib.urlopen(path)
	html='"""'+f.read()+'""""'
	soup=BeautifulSoup(html,"html.parser")
	result_rating={}
	result_recording={}
	result_actions={}
	result_audio={}
	result_sound={}

	
	try:
		all_h1=soup.find_all("h1")        #文章标题
		#print all_h1[1].text                     
		all_h2=soup.find_all("h2")     #过滤出所有标签为<h2>的信息

		title=all_h1[1].text       #如果没有该网页，执行此句会报错执行except语句

		for i in range(len(all_h2)):
		#print all_h2[i].string
			pathname_A='/Users/yikisun/Desktop/'#音频的存储路径
			pathname_P='/Users/yikisun/Desktop/'#图片的存储路径

			if all_h2[i].string=='Rating':      ##筛选出等级
				div=soup.find_all("div",attrs={'class':'rating'})
				li=div[0].find_all("li",attrs={'class':'selected'})  #被选中的为等级
				result_rating['Rating']=li[0].text
				insertData("Rating",result_rating,path)#插入数据库


			if all_h2[i].string=='Recording data':
				table=soup.find_all("table",attrs={'class':'key-value'})
				tbody=table[0].find_all("td")
				key=[]
				value=[]

				for tmp in range(len(tbody)):       
					if tmp%2==0:                          #偶数为key值，奇数为key对应的value值，分别存入两个列表
						key.append(tbody[tmp].text)
					else:
						if tbody[tmp].string==None:#如果有超链接，保存链接
							a=tbody[tmp].find_all("a")
							value.append(a[0]['href'])
						else:
							value.append(tbody[tmp].text)					
				for tmp in range(len(tbody)/2):
					result_recording[key[tmp]]=value[tmp]

				insertData("Recording_date",result_recording,path)#插入数据库
			#print result
				

			if all_h2[i].string=="Actions ":      #第一个ul class：simple在头部
				ul=soup.find_all("ul",attrs={'class':'simple'})
				a_A=ul[1].find_all("a")
			#print a_A
				for z in range(len(a_A)):
					result_actions[a_A[z].text]=a_A[z]['href']

				audio_name=a_A[0]['download']#保留音频、图片的命名，名字存在标签的download属性中
				photo_name=a_A[1]['download']

				download('https://www.xeno-canto.org'+result_actions[' Download audio file'],pathname_A+audio_name)      #将音频存入本地
				download('https://www.xeno-canto.org/'+result_actions[' Download full-length sonogram'],pathname_P+photo_name)     #将图片存入本地
				insertData("Actions",result_actions,path)        #result_actions字典插入到Actions表中

			#print result[' Download full-length sonogram']

				#print a_A[z].text,a_A[z]['href']
			#print result
				

			if all_h2[i].string=="Audio file properties":
				table_A=soup.find_all("table",attrs={'class':'key-value'})
				tbody_A=table_A[1].find_all("td")
				key=[]
				value=[]
				for x in range(len(tbody_A)):
					if x%2==0:
						key.append(tbody_A[x].text)
					else:
						value.append(tbody_A[x].text)

				# print tbody_A[x].string
				for x in range(len(tbody_A)/2):
					result_audio[key[x]]=value[x]

				insertData("Audio_file_properties",result_audio,path)#插入数据库
			#print result
			

			if all_h2[i].string=="Sound characteristics":
				table_S=soup.find_all("table",attrs={'class':'key-value'})
				tbody_S=table_S[2].find_all("td")
				key=[]
				value=[]
				for y in range(len(tbody_S)):
					if y%2==0:
						key.append(tbody_S[y].string)
					else:
						value.append(tbody_S[y].string)
				for y in range(len(tbody_S)/2):
					result_sound[key[y]]=value[y]

				#print result_sound
				insertData("Sound_characteristics",result_sound,path)
		

	except Exception as e:
		print "not found page"+path
	
	#print result_rating
	# for key in result.keys():
	# 	result[key.replace(' ','_')]=result.pop(key)       #将key值中的空格符用下划线代替
	# 	#print key
	

def find_all(item,attr,c):
	return item.find_all(attr,attrs={'class':c},limit=1)

def download(_url,name):
	if _url==None:
		print "url faild"

	photo=urllib.urlopen(_url)
	#print photo.getcode()
	if photo.getcode()!=200:
		pass
	else:
		with open(name,"wb") as code:
			code.write(photo.read())
			code.close()

def insertData(TableName,dic,path):
	try:
		conn=MySQLdb.connect(host='10.202.47.135',user='root',passwd='root',db='bird_recording',port=3306,use_unicode=True,charset="utf8")
		cur=conn.cursor()
		
		for key in dic:
			# print "insert into "+TableName+"(k,v) values('"+key+"','"+dic[key]+"')"
			sql = "insert into "+TableName+"(k,v,u) values('"+key+"','"+dic[key]+"','"+path+"')"
			#print sql
			cur.execute(sql)

		conn.commit()
		cur.close()
		conn.close()

	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0],e.args[1])
	
	

def main(path):
	get_date(path)


if __name__ == '__main__':
    #path = 'https://www.xeno-canto.org/1'
    main(sys.argv[1])
