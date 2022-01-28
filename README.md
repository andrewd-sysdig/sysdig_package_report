# Sysdig Package Report
This script will get a list of images in runtime filtered by cluster & namespace (if specified) and then queries the list of vulnrabilities for those images. You can optionally specify a package name such as log4j with the -p command line parameter, this will then only list vulnrabilities relating to that package. 

Output report is written to the same directory as you run the script as output.csv and output.json

## Usage examples
Make sure to have 2 environment variables set appropriately
```
export API_TOKEN="<Your Sysdig Secure API Token>"
export API_ENDPOINT="https://app.au1.sysdig.com"
```

### Look in the cluster lab4, namespace example-voting-app for any vulnerabilities that have the log4j package
 ``` ./sysdig_package_report.py -c lab4 -n example-voting-app -p log4j ```
 
### Look in the cluster lab4, namespace sock-shop for any vulnerabilities  
 ``` ./sysdig_package_report.py -c lab4 -n sock-shop ```
 
### Look through all clusters and namespaces for any vulnerabilities with the package log4j
 ``` ./sysdig_package_report.py -p log4j ```

## Sample CSV output
  ```
fullTag,imageID,vtype,vuln,vulnURL,package,packageCPE,packageName,packagePath,packageType,severity,fixVersion,lastEvaluated,disclosureDate,solutionDate
docker.io/nestorsalceda/example-voting-app-worker,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,non-os,VULNDB-259358,https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-259358,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Critical,2.0-alpha1,1643321173,1623715200,1623715200
docker.io/nestorsalceda/example-voting-app-worker,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,non-os,VULNDB-220038,https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-220038,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Critical,2.8.2,1643321173,1576627200,1491350400
docker.io/nestorsalceda/example-voting-app-worker,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,non-os,VULNDB-279568,https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-279568,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,High,2.0,1643321173,1642377600,1464566400
docker.io/nestorsalceda/example-voting-app-worker,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,non-os,VULNDB-279567,https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-279567,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,High,2.0,1643321173,1642377600,1464566400
docker.io/nestorsalceda/example-voting-app-worker,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,non-os,VULNDB-276252,https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-276252,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Medium,2.0 2.16.0,1643321173,1639180800,1639353600
docker.io/nestorsalceda/example-voting-app-worker,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,non-os,CVE-2020-9488,https://nvd.nist.gov/vuln/detail/CVE-2020-9488,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Low,None,1643321173,1587772800,0

```
  
## Sample JSON output
  
  ```
  [
    {
        "fullTag": "docker.io/nestorsalceda/example-voting-app-worker",
        "imageID": "73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
        "vtype": "non-os",
        "vuln": "VULNDB-259358",
        "vulnURL": "https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-259358",
        "package": "log4j-1.2.12",
        "packageCPE": "cpe:/a:-:log4j:1.2.12:-:-",
        "packageName": "log4j",
        "packagePath": "/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
        "packageType": "java",
        "severity": "Critical",
        "fixVersion": "2.0-alpha1",
        "lastEvaluated": 1643321173,
        "disclosureDate": 1623715200,
        "solutionDate": 1623715200
    },
    {
        "fullTag": "docker.io/nestorsalceda/example-voting-app-worker",
        "imageID": "73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
        "vtype": "non-os",
        "vuln": "VULNDB-220038",
        "vulnURL": "https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-220038",
        "package": "log4j-1.2.12",
        "packageCPE": "cpe:/a:-:log4j:1.2.12:-:-",
        "packageName": "log4j",
        "packagePath": "/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
        "packageType": "java",
        "severity": "Critical",
        "fixVersion": "2.8.2",
        "lastEvaluated": 1643321173,
        "disclosureDate": 1576627200,
        "solutionDate": 1491350400
    },
    {
        "fullTag": "docker.io/nestorsalceda/example-voting-app-worker",
        "imageID": "73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
        "vtype": "non-os",
        "vuln": "VULNDB-279568",
        "vulnURL": "https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-279568",
        "package": "log4j-1.2.12",
        "packageCPE": "cpe:/a:-:log4j:1.2.12:-:-",
        "packageName": "log4j",
        "packagePath": "/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
        "packageType": "java",
        "severity": "High",
        "fixVersion": "2.0",
        "lastEvaluated": 1643321173,
        "disclosureDate": 1642377600,
        "solutionDate": 1464566400
    },
    {
        "fullTag": "docker.io/nestorsalceda/example-voting-app-worker",
        "imageID": "73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
        "vtype": "non-os",
        "vuln": "VULNDB-279567",
        "vulnURL": "https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-279567",
        "package": "log4j-1.2.12",
        "packageCPE": "cpe:/a:-:log4j:1.2.12:-:-",
        "packageName": "log4j",
        "packagePath": "/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
        "packageType": "java",
        "severity": "High",
        "fixVersion": "2.0",
        "lastEvaluated": 1643321173,
        "disclosureDate": 1642377600,
        "solutionDate": 1464566400
    },
    {
        "fullTag": "docker.io/nestorsalceda/example-voting-app-worker",
        "imageID": "73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
        "vtype": "non-os",
        "vuln": "VULNDB-276252",
        "vulnURL": "https://app.au1.sysdig.com/secure//#/scanning/vulnerabilities/VULNDB-276252",
        "package": "log4j-1.2.12",
        "packageCPE": "cpe:/a:-:log4j:1.2.12:-:-",
        "packageName": "log4j",
        "packagePath": "/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
        "packageType": "java",
        "severity": "Medium",
        "fixVersion": "2.0 2.16.0",
        "lastEvaluated": 1643321173,
        "disclosureDate": 1639180800,
        "solutionDate": 1639353600
    },
    {
        "fullTag": "docker.io/nestorsalceda/example-voting-app-worker",
        "imageID": "73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
        "vtype": "non-os",
        "vuln": "CVE-2020-9488",
        "vulnURL": "https://nvd.nist.gov/vuln/detail/CVE-2020-9488",
        "package": "log4j-1.2.12",
        "packageCPE": "cpe:/a:-:log4j:1.2.12:-:-",
        "packageName": "log4j",
        "packagePath": "/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
        "packageType": "java",
        "severity": "Low",
        "fixVersion": "None",
        "lastEvaluated": 1643321173,
        "disclosureDate": 1587772800,
        "solutionDate": "0"
    }
]
  ```
