# PaloLicenceAPIretrevial
Been written by Toby Makepeace to demonstrate the License API interface for automation.

Updated for Python 3.6

The tool, will register and retrieve the license key files from the Palo Alto Licensing API.
You need to have the LicenseAPI key from the Palo Alto support site for this to work.

Initally, run the script
"palolicencereterival.py setup" to create the config.py for storing the API key in.

"palolicencereterival.py help" for more instructions.

https://www.paloaltonetworks.com/documentation/80/virtualization/virtualization/license-the-vm-series-firewall/licensing-api


The script has been written to help with the Palo Alto Networks
VM-Series licence retrevial for the CSSP program
The process will work for any PA unit being hardware or software
The process has been written to ask questions to drive the licence
generation to key files.

The options available are help,setup,serial,register,user,authcode
e.g. 'palolicencereterival.py help'
or 'palolicencereterival.py serial'

The 'setup' option is to register you LicenceAPI which you will get
 from the support portal

The 'serial' option allows you to retrieve licence for a specific 
Serial Number.

The register option, will take the CPUID and the UUID from a 
deployed VM, along with the authcode at registion and generate the 
licences. At this time the Serial number does not exist, so you are
asked to provide a local temp name for the licence file

The 'user' option is to submit the CSSP data to the CSSP portal, it
is only for CSSP customers.

The 'authcode' option will allow you to see all the serial numbers 
registered to that authcode, and allow you to generate the licences  
for off line usage.

This has been written as a example of what is possible.
feel free to take apart and reuse
