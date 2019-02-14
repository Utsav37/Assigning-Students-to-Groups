#!/usr/bin/env python3
# to run this file do : ./assign.py testfile.txt 102 20 1 

# I had to do : 

# dos2unix assign.py
# chmod u+x assign.py
# ./assign.py testfile.txt 102 2 1 
# NOTE:          ".txt" after filename is necessary. 
# ~csb551/a1/test-format.py ./assign.py testcase1.txt 60 30 20 . This worked perfect and said congratulations
#########################################################################################################################################
# ASSUMPTION: We know that grading an assignment can take much longer than as compared to reading email or doing small meeting . 
# Here I have assumed that our k value is significantly greater than the values of n and m. So my code give best solution by grouping 3 students in single group.
# So what my program does is, it will create groups of 3 students first and then we will find optimum solution by swapping students across groups to see if they 
# have reduced costs or not.
# Moreover it sometimes gives optimum solution even with nearly same values of k and m and n if the number of students are significantly larger. 
##########################################################################################################################################
# FAILED STRATEGIES: 1. First strategy used by me was to create all possible states that are possible, but unfortunately after 4 days I had to give up because 
# some states were missing in my code and it was going too complex. The strategy used here was first generate all possible states, find cost of each state and then 
# select the optimal one. 

# 2.Second strategy was using monte carlo local search. I tried to apply it but it never was convincing and the way to apply was always obscure. As there was 
# much less mentioned about implementation of this strategy on internet, we didnt have much example to observe the way it works. So had to give up
# that strategy too.
# #########################################################################################################################################
#code for reading file and storing each students data into a list of dictionary which contains userid, prefergroupsize, prefer, nonprefer.
import sys
inputdata=[]
allstudentidlist=[]
with open(sys.argv[1], 'r') as file:
	for line in file:
		line=line.replace("\n"," ")
		# print("inintially line was this : ",line)

		linedetail=line.split(" ")
		# print("after splitting line became this : ", linedetail)
		preferlist=[]
		nonpreferlist=[]
		if(linedetail[2]!="_"):
			allprefer=linedetail[2].split(",")
			for name in allprefer:
				preferlist.append(name)

		if(linedetail[3]!="_"):
			nonprefer=linedetail[3].split(",")
			for name in nonprefer:
				nonpreferlist.append(name)

		studentdata={
		'userid':linedetail[0],
		'prefergroupsize':linedetail[1],
		'prefer':preferlist,
		'nonprefer':nonpreferlist
		}

		allstudentidlist.append(linedetail[0])
# input data is list and it will consist of many dictionaries and each dictionary will consist of userid,prefergroupsize,prefer,nonprefer
		inputdata.append(studentdata)
# print(inputdata)
noofstudents=len(inputdata)

# core logic of ptogram goes here 

# I have taken kval instead of k because it conflicted with k parameter used in later part of code. so no issues with this.
kval=int(sys.argv[2])
m=int(sys.argv[3])
n=int(sys.argv[4])
# m is for meeting and n for email , kval for per assignment time 

if(len(allstudentidlist)%3)==0:
	len_finallist=int(len(allstudentidlist)/3)
else:
	len_finallist=int(len(allstudentidlist)/3)+1
# here if there are 15 students, then it will make 5 groups of 3 each and if there are 17 students, it will make total 6 groups(17/3 +1 = 5 +1 =6)
personconflictlist=[]
nonpreferedconflictlist=[]
finallist=[]
finallist = [allstudentidlist[x:x+3] for x in range(0, len(allstudentidlist), 3)]
# print("finallist is ",finallist)


def compute_cost(finallist):
	allloopcost=0
	for list1 in finallist:
		for person in list1:
			gc=int(check_group_conflict(person,list1))
			# print("gc is : ",gc)
			# print(type(gc))
			pc=int(check_person_conflict(person,list1))
			npc=int(check_nonprefered_conflict(person,list1))
			allloopcost=allloopcost+int(gc)*1+pc*n+npc*m 
		allloopcost=allloopcost+kval
	# print(" $$$$$$$$$$$  :",allloopcost)
	return allloopcost

def check_group_conflict(person,list1):
	index=allstudentidlist.index(person)
	prefergrpsize=int(inputdata[index]['prefergroupsize'])
	gotgrpsize=len(list1)
	if(prefergrpsize==0):
		return 0
	if(prefergrpsize!=gotgrpsize):
		return 1
	else:
		return 0

def check_person_conflict(person,list1):
	l=0
	index=allstudentidlist.index(person)
	# print("person is :",person)
	# print("got list is :",list1)
	personconflictlist=inputdata[index]['prefer'].copy()
	personconflictlist.append(person)
	# print("prefer list is :",personconflictlist)
	for x in personconflictlist:
		if(x not in list1):
			l=l+1

	# l=len(list1)-len(list(set(personconflictlist).intersection(list1)))
	# print(l)
	return l

def check_nonprefered_conflict(person,list1):
	l=0
	index=allstudentidlist.index(person)
	nonpreferedconflictlist=inputdata[index]['nonprefer']
	# print("person is ",person)
	# print("got list is :",list1)
	# print("non preferred group is  :",nonpreferedconflictlist)
	for x in list1:
		if x in nonpreferedconflictlist:
			l=l+1

	# l=len(list(set(personconflictlist).intersection(list1)))
	# print("cost " ,l)
	return l
def printfunction(finallist):
	for list11 in finallist:
		# print("list 11 is : ",list11)
		print( " ".join([x for x in list11]))
	print(originalcost)

# i will be row index that will be compared to all below rows under it 
# j will be all rows below ith row and we will compare all elements of ith row with all elements of jth row and jth row will be ranging from row under ith row to second last row
# for example: if i = 1, then j = 2,3,4..16   if i= 7,j=8,9,10...16 if there are 17 rows in total
# I had to split this into  two parts it : (if rows=17) first for all above 15 rows and second for below 2 rows because of list index out of range errors
originalcost=compute_cost(finallist)
for i in range(len_finallist-1):
	for j in range(i+1,len_finallist-1):
		for k in range(0,3):
			temp1=finallist[i][k]
			temp2=finallist[j][k]
			finallist[j][k]=temp1
			finallist[i][k]=temp2
			newcost=compute_cost(finallist)
			if(newcost>originalcost):
				temp1=finallist[i][k]
				temp2=finallist[j][k]
				finallist[j][k]=temp1
				finallist[i][k]=temp2
			else:
				originalcost=newcost

# here i have implemented logic for last two columns as there are not fixed number of columns in the last column. 
# Thus rows will change from i=0 to len_finallist and column will change from 0 to len(finallist[endindex])
# print("####################",finallist[len_finallist])
for i in range(0,len_finallist):
	for k in range(0,len(finallist[len_finallist-1])):
		temp1=finallist[i][k]
		temp2=finallist[len_finallist-1][k]
		finallist[len_finallist-1][k]=temp1
		finallist[i][k]=temp2
		newcost=compute_cost(finallist)
		if(newcost>originalcost):
			temp1=finallist[i][k]
			temp2=finallist[len_finallist-1][k]
			finallist[len_finallist-1][k]=temp1
			finallist[i][k]=temp2
		else:
			originalcost=newcost

printfunction(finallist)