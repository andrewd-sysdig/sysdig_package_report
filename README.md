# log4shell_sysdig_report
Quickly hacked together on a Friday night, no error handling, very little testing...

Make sure to have 2 environment variables set appropriately 
export API_TOKEN="<Your Sysdig Secure API Token>"
export API_ENDPOINT="https://app.au1.sysdig.com"
  
Script gets a list of all scanned images (not just ones in runtime) and then queries each individually to get a list of vulnrabilities and if any of them have a log4j package_name then adds it to the list to be added to the output report
  
Output report is written to the same directory as you run the script as output.csv and output.json
  
Good Luck & Merry Xmas :)
