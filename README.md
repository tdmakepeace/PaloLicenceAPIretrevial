# PaloLicenceAPIretrevial
Been written by Toby Makepeace to demostrate the Licence API interface for automation.

The tool, will register and retrieve the licence key files from the Palo Alto Licenceing API.
You need to have the LicenseAPI key from the Palo Alto support site for this to work.

Initally, run the script
"palolicencereterival.py setup" to create the config.py for storing the API key in.

Then you have 3 
options 1. just retrieve the licences based on the serial number.
This would work for customers wanting to build a Bootstrap iso for the hardware as well as the VM's

Option 2. Register a VM based on the CPUID UUID and authcode.

Option 3. Retrieve all the serial numbers for a authcode, and chose if you want to create the licence files.

Option 4 is still be worked on, and that is for the CSSP registration process.


https://www.paloaltonetworks.com/documentation/80/virtualization/virtualization/license-the-vm-series-firewall/licensing-api
