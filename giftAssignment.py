import random
import smtplib
import boto3
import csv

def getFamilyInfo():
    family = []
    inputFile = csv.DictReader(open("familyInfo.csv"))
    for row in inputFile:
        family.append(row)
    return family

def getPrivateInfo():
    inputFile = csv.DictReader(open("privateInfo.csv"))
    for row in inputFile:
        privateInfo = row
    return privateInfo

def assignGifts(family):
	options = []
	for person in family:
		options.append(person['name'])
	for person in family:
		otherName = person['name']
		while otherName == person['name']:
			i = random.randint(0,len(options)-1)
			otherName = options[i]
		options.remove(otherName)
		person['giftFor'] = otherName

def parseTexts(family):
	for person in family:
		person['emailText'] = "Subject: Christmas Gift Draw\nHello " + person['name'] + ",\nFor this year's gift, you have: " + person['giftFor'] + ".\nMerry Christmas!"
		person['smsText'] = "For this year's gift, you have: " + person['giftFor'] + ". Merry Christmas!"

def sendEmail(family, privateInfo):
	testEmail = privateInfo['testEmail']
	emailKey = privateInfo['email_key']
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
	smtpObj.starttls()
	smtpObj.login(testEmail, emailKey)
	for person in family:
		print(person['emailText'])
		# smtpObj.sendmail(testEmail, person['email'], person['emailText'])
	smtpObj.quit()

def sendTexts(family, privateInfo):
	client = boto3.client(
	    "sns",
	    aws_access_key_id=privateInfo['access_key_id'],
	    aws_secret_access_key=privateInfo['secret_access_key'],
	    region_name=privateInfo['region']
	)

	for person in family:
		print(person['phone'] + " : " + person['smsText'])
		# client.publish(
		#     PhoneNumber=person['phone'],
		#     Message=person['smsText']
		# )

# Get all the info from my local csv files.
family = getFamilyInfo()
privateInfo = getPrivateInfo()

assignGifts(family)
parseTexts(family)
sendEmail(family, privateInfo)
sendTexts(family, privateInfo)
