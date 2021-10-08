#! /usr/bin/python3

import sqlite3
conn=sqlite3.connect(":memory:")
c=conn.cursor()
c.execute("create table fail (id text, ip text)")

i=0
import sys 
for item in sys.stdin.readlines():
	#print(line, end='')
	temp_id=(item[0:8]).replace(" ","")
	temp_ip=item[22:37].replace(" ","")
	
	temp_ssh=item[9:18]
	if temp_ssh=="ssh:notty":
		i+=1
		c.execute("insert into fail values ('%s', '%s')" % (temp_id, temp_ip))
	
print("total number : %d" % i)
c.execute("select count(distinct(id)) from fail")
num_id=(c.fetchall())[0][0]

c.execute("select count(distinct(ip)) from fail")
num_ip=(c.fetchall())[0][0]
print("%d distinct usernames and %d distinct IP adrs" % (num_id, num_ip))


c.execute("select id, count(id) from fail group by id order by count(id) desc limit 20")
results=c.fetchall()
print("-"*25)
print("id\t| count\t| percent")
print("-"*25)

for item in results:
	if len(item[0])<8:
		print("%s\t| %d\t| %.1f %%" % (item[0], item[1], item[1]/i*100.0))
	else:
		print("%s| %d\t| %.1f %%" % (item[0], item[1], item[1]/i*100.0))	

c.execute("select ip, count(ip) from fail group by ip order by count(ip) desc limit 20")
results=c.fetchall()
print("-"*35)
print("ip\t\t| count\t| percent")
print("-"*35)
for item in results:
	#print(item[0],"\t|\t",item[1])
	print("%s\t| %d\t| %.1f %%" % (item[0], item[1], item[1]/i*100.0))

conn.close()

