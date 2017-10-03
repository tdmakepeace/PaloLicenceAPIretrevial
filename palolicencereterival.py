import urllib2
import urllib
import sys
import json


try:
    from config import *
except ImportError:
    for arg in sys.argv: 1
# use the command line to call the function from a single script.
    if arg == "setup":
        print ""
    else:
        print ("Run palolicencereterival.py setup")
        sys.exit(0)

def setup(): 	
    
# This section just registers the LicenceAPI key for future use, it should be a one of process and not repeated.
# however if a customer regenerates the key for any reason, they would need to rerun. 

    api = raw_input("What is the licenseing API key for your account:")
    key = "api = '%s'" %api
##    if the customer wanted to register the authcode to be used that is a option. 
##    auth = raw_input("What is the licenseing API key for your account:")
##    authcode = "authcode = '%s'" %auth


    f = open('config.py', 'w')
    print >> f, key # or f.write('...\n')
##    print >> f, authcode # or f.write('...\n')
    f.close()
        
def serialretrieve(): 
    
# this section is to be able to retrieve the licence files for off line installations after the registration is 
# completed either via the API or the portal directly.
# the process generates the licence key files that can be imported. 
    
    serial = raw_input("What is the Serial number of the licence you wish to retrieve:")
    data = "serialNumber="+serial
    
#   debug
#   print data

    url = 'https://api.paloaltonetworks.com/api/license/activate'
    headers = { 'apikey':api , 'Content-Type':'application/x-www-form-urlencoded' }
    req = urllib2.Request(url, data , headers)
    resp_str = urllib2.urlopen(req)

    for x in resp_str:
# Count the number of licences in the file.
        c = x.count('partidField')
        resp = json.loads(x)
        
# for every licence create a file with the output.
# use the serial number and the licence type. 
#
        i=0
        while i < c:
            fName = serial+"-"+resp[i]['partidField']+".key"
#Uncomment for debug
#            print fName
#            print (resp[i]['keyField'])

            file = open(fName,"w") 
            file.write(resp[i]['keyField'])
            file.close() 
            i+=1
        
    resp_str.close()
	

    

def serialregister():
# this section is to be able to register a device based on the authcode and the CPUID and UUID
# It will retrieve the licence files for off line installations 

    
    cpuid = raw_input("What is the cpuid of the device you wish to register:")
    uuid = raw_input("What is the uuid of the device you wish to register:")
    authcode = raw_input("What is the authcode of the device you wish to register:")
    
    forms =  { "cpuid" : cpuid , "uuid" : uuid ,"authCode" : authcode }
    data = urllib.urlencode(forms)
    print data

    url = 'https://api.paloaltonetworks.com/api/license/activate'
    headers = { 'apikey':api , 'Content-Type':'application/x-www-form-urlencoded' }
    req = urllib2.Request(url, data , headers)
    resp_str = urllib2.urlopen(req)

    for x in resp_str:
# Count the number of licences in the file.
        lic = x.count('partidField')
        print  "you have '%s' licences" %lic
 
    resp_str.close()

# map the authcode into the data field.
    data = "authcode=%s" %authcode
    url = 'https://api.paloaltonetworks.com/api/license/get'
    headers = { 'apikey':api , 'Content-Type':'application/x-www-form-urlencoded' }
    req = urllib2.Request(url, data , headers)
    resp_str1 = urllib2.urlopen(req)

    for a in resp_str1:

        resp = json.loads(a)   


#        d = resp['UsedCount']
#        print  "the number of devices  = '%s'" %d
#
#        print(resp)
#
#        cpuid = raw_input("What is the cpuid of the device you wish to register:")


        ## for every licence create a file with the output.
        ## use the serial number and the licence type. 
        ##
        x=0
        while x < d:
            print (resp['UsedDeviceDetails'][x]['SerialNumber'])+","+(resp['UsedDeviceDetails'][x]['CPUID'])+","+(resp['UsedDeviceDetails'][x]['UUID'])
            if cpuid == (resp['UsedDeviceDetails'][x]['CPUID']):
                serial = (resp['UsedDeviceDetails'][x]['SerialNumber'])
                data = "serialNumber="+serial

            #   debug
            #   print data

                url = 'https://api.paloaltonetworks.com/api/license/activate'
                headers = { 'apikey':api , 'Content-Type':'application/x-www-form-urlencoded' }
                req = urllib2.Request(url, data , headers)
                resp_str2 = urllib2.urlopen(req)

                for y in resp_str2:
            # Count the number of licences in the file.
                    c = y.count('partidField')
                    resp = json.loads(y)

            # for every licence create a file with the output.
            # use the serial number and the licence type. 
            #
                    i=0
                    while i < c:
                        fName = serial+"-"+resp[i]['partidField']+".key"
            #Uncomment for debug
            #            print fName
            #            print (resp[i]['keyField'])

                        file = open(fName,"w") 
                        file.write(resp[i]['keyField'])
                        file.close() 
                        i+=1

                resp_str2.close()

            else:
                print "nothing found"

            x=x+1    

        print "Finished"
    resp_str1.close()


    
def registeruser():
# not working as i need a CSSP account to work with.

    
    SERIAL = raw_input("The following details as required to be registered against a device \nWhat is the Serial number of the device you wish to register details against \n:")
    CustomerAccountId = raw_input("Unique Reference number, used for billing tracking:")
    CompanyName = raw_input("End User Company name:")
    Address = raw_input("First Line of the address:")
    Country = raw_input("Country code - Currently only US supported :")
    Region = raw_input("Region (optional):")
    City = raw_input("City:")
    State = raw_input("State - Currently on CA supported :")
    PostalCode = raw_input("Postal Code:")
    EndUserContactEmail = raw_input("The End User Email address:")
    Admin = raw_input("What is the ID of the Admin submitting the request:")
    
    
    forms =  { 
    "serialNumbers" : SERIAL , 
    "CustomerAccountId" : CustomerAccountId ,
    "CompanyName" : CompanyName , 
    "Address" : Address ,
    "Country" : Country ,
    "Region" : Region ,
    "City" : City ,
    "State" : State ,
    "PostalCode" : PostalCode ,
    "EndUserContactEmail" : EndUserContactEmail ,
    "CreatedBy" : Admin 
    }
    
    data = urllib.urlencode(forms)
    print data



    url = 'https://api.paloaltonetworks.com/api/license/ReportEndUserInfo'
    headers = { 'apikey':api , 'Content-Type':'application/json' }
    req = urllib2.Request(url, data , headers)
    resp_str = urllib2.urlopen(req)

    result = resp_str.read()
    print result


def authcode():
# retrieves all the serial number against the authcode.
# gives you the option to create the licence files for the serial number and authcode.
#
    
    authcode = raw_input("What is the authcode you wish to validate:")
    data = "authcode=%s" %authcode

    url = 'https://api.paloaltonetworks.com/api/license/get'
    headers = { 'apikey':api , 'Content-Type':'application/x-www-form-urlencoded' }
    req = urllib2.Request(url, data , headers)
    resp_str1 = urllib2.urlopen(req)

    for a in resp_str1:

        resp = json.loads(a)   

        d = resp['UsedCount']
        print  "the number of registered devices  = '%s'" %d

#        print(resp)


        x=0
        while x < d:
            print (resp['UsedDeviceDetails'][x]['SerialNumber'])+","+(resp['UsedDeviceDetails'][x]['CPUID'])+","+(resp['UsedDeviceDetails'][x]['UUID'])
            licence = raw_input("Do you need me to generate licences, y or n :")
    
            if licence == 'y':
                serial = (resp['UsedDeviceDetails'][x]['SerialNumber'])
                data = "serialNumber="+serial

            #   debug
            #   print data

                url = 'https://api.paloaltonetworks.com/api/license/activate'
                headers = { 'apikey':api , 'Content-Type':'application/x-www-form-urlencoded' }
                req = urllib2.Request(url, data , headers)
                resp_str2 = urllib2.urlopen(req)

                for y in resp_str2:
            # Count the number of licences in the file.
                    c = y.count('partidField')
                    resp = json.loads(y)

            # for every licence create a file with the output.
            # use the serial number and the licence type. 
            #
                    i=0
                    while i < c:
                        fName = serial+"-"+resp[i]['partidField']+".key"
            #Uncomment for debug
            #            print fName
            #            print (resp[i]['keyField'])

                        file = open(fName,"w") 
                        file.write(resp[i]['keyField'])
                        file.close() 
                        i+=1

                resp_str2.close()

            else:
                print " "

            x=x+1    

        print "Finished"
    resp_str1.close()
       
def help(): 	
    print "help menu"  
    print " still to be written post testing"
    print " need to provide fall automation examples"
    
if __name__ == '__main__':
    for arg in sys.argv: 1
# use the command line to call the function from a single script.
    if arg == "help":
        help()
    elif arg == "setup":
        setup()
    elif arg == "serial":
        serialretrieve()
    elif arg == "register":
        serialregister()
    elif arg == "user":
        registeruser()
    elif arg == "authcode":    
        authcode()
    else:
        print " The options available are help,setup,serial,register,user,authcode"
        print " e.g. 'palolicencereterival.py help'"
        print " or 'palolicencereterival.py serial'"
       