import urllib
import sys
import json
import urllib.request
import urllib.parse



#try:
#    import urllib.request as urllib2
#except ImportError:
#    import urllib2
	

try:
    from config import *
except ImportError:
    for arg in sys.argv: 1
# use the command line to call the function from a single script.
    if arg == "setup":
        print ("")
    else:
        print ("Run palolicencereterival.py setup")
        sys.exit(0)

def setup(): 	
    
# This section just registers the LicenceAPI key for future use, it should be a one of process and not repeated.
# however if a customer regenerates the key for any reason, they would need to rerun. 

    f = open('config.py', 'w')
    api = input("What is the licenseing API key for your account:")
    key = "api = '%s'\n" %api
    f.write(key)
##    if the customer wanted to register a single authcode to be used 
##    uncomment the following lines. 
#    auth = input("What is the licenseing authcode you want to use for bulk provisioning:")
#    authcode = "authcode = '%s'\n" %auth
#    f.write(authcode)
##    
    f.close()
        
def serialretrieve(): 
    
# this section is to be able to retrieve the licence files for off line installations after the registration is 
# completed either via the API or the portal directly.
# the process generates the licence key files that can be imported. 
# always import the support key first or the base VM key.
    
##########  serial = '001606064532'
    serial = input("What is the Serial number of the licence you wish to retrieve:")
    data = "serialNumber="+serial
    data = data.encode('ascii')
#   debug
#   print data

    url = "https://api.paloaltonetworks.com/api/license/activate"
#    headers = {'apikey':api }
#    print(headers)
    req = urllib.request.Request(url, data )
#    print (req)
    req.add_header( 'apikey', api )
    resp_str = urllib.request.urlopen(req)
#    print(resp_str)
	
    for x in resp_str:
        resp = json.loads(x)
#        print (resp)
## Count the number of licences in the file.
        c = (len(resp))
       
#        
## for every licence create a file with the output.
## use the serial number and the licence type. 
##
        i=0
        while i < c:
            fName = serial+"-"+resp[i]['partidField']+".key"
            file = open(fName,"w") 
            file.write(resp[i]['keyField'])
            file.close() 
            i+=1
    resp_str.close()
    

def serialregister():
# this section is to be able to register a device based on the authcode and the CPUID and UUID
# It will retrieve the licence files for off line installations 

    dname = input("What is the name you wish to have linked to the licences:")
    cpuid = input("What is the cpuid of the device you wish to register:")
    uuid = input("What is the uuid of the device you wish to register:")
#   Comment out the following line if you have set up a static authcode in the setup.
#   You need to uncomment the enablement of this in the set up lines 38-40.
    authcode = input("What is the authcode of the device you wish to register:")
#    
  
    
    data =  urllib.parse.urlencode({ "cpuid" : cpuid , "uuid" : uuid ,"authCode" : authcode })
    data = data.encode('ascii')


######################

    url = 'https://api.paloaltonetworks.com/api/license/activate'
  
#    print(url)
#    print (data)
    req = urllib.request.Request(url=url, data=data )
#    print (req)
    req.add_header( 'apikey', api )
    resp_str = urllib.request.urlopen(req)
    
    for x in resp_str:
        resp = json.loads(x)
#        print (resp)
## Count the number of licences in the file.
        c = (len(resp))
       
#        
## for every licence create a file with the output.
## use the serial number and the licence type. 
##

        i=0
        ## while statement added to address the issues with the fact the auto focus licences
        ## does not have a partidfield to work with
        ## so instead look at the feature Field and if autoforcus
        ## manual set the file name.
        while i < c:
            if resp[i]['featureField'] == ('AutoFocus Device License'):
                fName = dname+"-PAN-VM-autofocus.key"
                file = open(fName,"w") 
                file.write(resp[i]['keyField'])
                file.close() 
                i+=1
            else:
                fName = dname+"-"+resp[i]['partidField']+".key"
                file = open(fName,"w") 
                file.write(resp[i]['keyField'])
                file.close() 
                i+=1
        
    resp_str.close()
 
    
def registeruser():
# Only for the CSSP account to work with.

    
    SERIAL = input("The following details as required to be registered against a device \nWhat is the Serial number of the device you wish to register details against \n:")
    CustomerAccountId = input("Unique Reference number, used for billing tracking:")
    CompanyName = input("End User Company name:")
    Address = input("First Line of the address:")
    Country = input("Country code - Currently only US supported :")
    Region = input("Region (optional):")
    City = input("City:")
    State = input("State - Currently on CA supported :")
    PostalCode = input("Postal Code:")
    EndUserContactEmail = input("The End User Email address:")
    Admin = input("What is the ID of the Admin submitting the request:")
    
    
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
    
    data =  urllib.parse.urlencode(forms)
    data = data.encode('ascii')
    print (data)


    url = 'https://api.paloaltonetworks.com/api/license/ReportEndUserInfo'
    
    
    req = urllib.request.Request(url=url, data=data )
#    print (req)
    req.add_header( 'apikey', api )
    resp_str = urllib.request.urlopen(req)
    result = resp_str.read()
    print (result)


def authcode():
# retrieves all the serial number against the authcode.
# gives you the option to create the licence files for the serial number and authcode.
#
    
    authcode = input("What is the authcode you wish to validate:")
    data = "authcode=%s" %authcode
    data = data.encode('ascii')

    url = 'https://api.paloaltonetworks.com/api/license/get'
    req = urllib.request.Request(url=url, data=data )
#    print (req)
    req.add_header( 'apikey', api )
    resp_str = urllib.request.urlopen(req)
    
    for x in resp_str:
        resp = json.loads(x)
#        print(resp)
        count = resp['UsedCount']
        usedcount = ( "the number of registered devices  = " + str(count) )
#        print (usedcount)
        #print  ("the number of registered devices  = '%s'") d
        c = (len(resp['UsedDeviceDetails']))
        
        i=0
        while i < c:
            display = (resp['UsedDeviceDetails'][i]['SerialNumber'])+","+(resp['UsedDeviceDetails'][i]['CPUID'])+","+(resp['UsedDeviceDetails'][i]['UUID'])
            print (display)
            licence = input("Do you need me to generate licences, y or n :")
    
            if licence == 'y':
                serial = (resp['UsedDeviceDetails'][i]['SerialNumber'])
                data = "serialNumber="+serial

                data = data.encode('ascii')
            #   debug
            #   print data

                url2 = "https://api.paloaltonetworks.com/api/license/activate"
            #    headers = {'apikey':api }
            #    print(headers)
                req2 = urllib.request.Request(url2, data )
            #    print (req)
                req2.add_header( 'apikey', api )
                resp_str2 = urllib.request.urlopen(req2)
            #    print(resp_str)

                for x2 in resp_str2:
                    resp2 = json.loads(x2)
            #        print (resp)
            ## Count the number of licences in the file.
                    c2 = (len(resp2))

            #        
            ## for every licence create a file with the output.
            ## use the serial number and the licence type. 
            ##
                    i2=0
                    while i2 < c2:
                        fName = serial+"-"+resp2[i2]['partidField']+".key"
                        file = open(fName,"w") 
                        file.write(resp2[i2]['keyField'])
                        file.close() 
                        i2+=1
                resp_str2.close()                
                            
                
            else:
                print ("")
                 

            i+=1  

        print ("Finished")
    resp_str.close()
       
def help(): 	
    print (" ") 
    print (" The script has been written to help with the Palo Alto Networks")
    print (" VM-Series licence retrevial for the CSSP program")
    print (" The process will work for any PA unit being hardware or software")
    print (" The process has been written to ask questions to drive the licence")
    print (" generation to key files.")
    print (" ")
    print (" The options available are help,setup,serial,register,user,authcode")
    print (" e.g. 'palolicencereterival.py help'")
    print (" or 'palolicencereterival.py serial'")
    print (" ")
    print (" The 'setup' option is to register you LicenceAPI which you will get")
    print ("  from the support portal")
    print (" ")
    print (" The 'serial' option allows you to retrieve licence for a specific ")
    print (" Serial Number.")
    print (" ")
    print (" The register option, will take the CPUID and the UUID from a ")
    print (" deployed VM, along with the authcode at registion and generate the ")
    print (" licences. At this time the Serial number does not exist, so you are")
    print (" asked to provide a local temp name for the licence file")
    print (" ")
    print (" The 'user' option is to submit the CSSP data to the CSSP portal, it")
    print (" is only for CSSP customers.")
    print (" ")
    print (" The 'authcode' option will allow you to see all the serial numbers ")
    print (" registered to that authcode, and allow you to generate the licences  ")
    print (" for off line usage.")
    print (" ")
    print (" This has been written as a example of what is possible.")
    print (" feel free to take apart and reuse")
    
  
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
        print (" The options available are help,setup,serial,register,user,authcode")
        print (" e.g. 'palolicencereterival.py help'")
        print (" or 'palolicencereterival.py serial'")
       