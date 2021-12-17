# log4shell_sysdig_report
Quickly hacked together on a Friday night, no error handling, very little testing...

Make sure to have 2 environment variables set appropriately
```
export API_TOKEN="<Your Sysdig Secure API Token>"
export API_ENDPOINT="https://app.au1.sysdig.com"
```
  
Script gets a list of all scanned images (not just ones in runtime) and then queries each individually to get a list of vulnrabilities and if any of them have a log4j package_name then adds it to the list to be added to the output report
  
It will take a while to run, tested against an environment with ~2,000 image scan results and took approx 30mins
  
Output report is written to the same directory as you run the script as output.csv and output.json
  
Good Luck & Merry Xmas :)

## Sample CSV output
  ```
  fullTag,imageID,vuln,vulnrabilityId,package,packageCPE,packageName,packagePath,packageType,severity
gcr.io/google-samples/microservices-demo/adservice:v0.3.2,89793da0d166cd17d4e54879fdf9e3ac34718f6ca07631239e938e2dec4ca649,VULNDB-275958,VULNDB-275958,log4j-2.13.3,cpe:/a:-:log4j:2.13.3:-:-,log4j,/app/build/install/hipstershop/lib/log4j-core-2.13.3.jar,java,Critical
gcr.io/google-samples/microservices-demo/adservice:v0.3.2,89793da0d166cd17d4e54879fdf9e3ac34718f6ca07631239e938e2dec4ca649,VULNDB-275958,VULNDB-275958,log4j-2.13.3,cpe:/a:-:log4j:2.13.3:-:-,log4j,/app/build/install/hipstershop/lib/log4j-api-2.13.3.jar,java,Critical
docker.io/bencer/example-voting-app-worker:jmx-1,d483a18d607a33cf6ab56799422b593c20ff2c8cba8626c5c419d0a10d50ba5b,VULNDB-275958,VULNDB-275958,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Critical
docker.io/bencer/example-voting-app-worker:jmx-1,d483a18d607a33cf6ab56799422b593c20ff2c8cba8626c5c419d0a10d50ba5b,VULNDB-220038,VULNDB-220038,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Critical
docker.io/bencer/example-voting-app-worker:jmx-1,d483a18d607a33cf6ab56799422b593c20ff2c8cba8626c5c419d0a10d50ba5b,CVE-2020-9488,CVE-2020-9488,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Low
docker.io/nestorsalceda/example-voting-app-worker:latest,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,VULNDB-275958,VULNDB-275958,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Critical
docker.io/nestorsalceda/example-voting-app-worker:latest,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,VULNDB-220038,VULNDB-220038,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Critical
docker.io/nestorsalceda/example-voting-app-worker:latest,73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088,CVE-2020-9488,CVE-2020-9488,log4j-1.2.12,cpe:/a:-:log4j:1.2.12:-:-,log4j,/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar,java,Low
gcr.io/google-samples/microservices-demo/adservice:v0.3.0,842294023ab0c8432ee9e2a778986f931c279bc528d06c00b50ac666fcab0417,VULNDB-275958,VULNDB-275958,log4j-2.13.3,cpe:/a:-:log4j:2.13.3:-:-,log4j,/app/build/install/hipstershop/lib/log4j-core-2.13.3.jar,java,Critical
gcr.io/google-samples/microservices-demo/adservice:v0.3.0,842294023ab0c8432ee9e2a778986f931c279bc528d06c00b50ac666fcab0417,VULNDB-275958,VULNDB-275958,log4j-2.13.3,cpe:/a:-:log4j:2.13.3:-:-,log4j,/app/build/install/hipstershop/lib/log4j-api-2.13.3.jar,java,Critical
```
  
## Sample JSON output
  
  ```
  [
   {
      "fullTag":"gcr.io/google-samples/microservices-demo/adservice:v0.3.2",
      "imageID":"89793da0d166cd17d4e54879fdf9e3ac34718f6ca07631239e938e2dec4ca649",
      "vuln":"VULNDB-275958",
      "vulnrabilityId":"VULNDB-275958",
      "package":"log4j-2.13.3",
      "packageCPE":"cpe:/a:-:log4j:2.13.3:-:-",
      "packageName":"log4j",
      "packagePath":"/app/build/install/hipstershop/lib/log4j-core-2.13.3.jar",
      "packageType":"java",
      "severity":"Critical"
   },
   {
      "fullTag":"gcr.io/google-samples/microservices-demo/adservice:v0.3.2",
      "imageID":"89793da0d166cd17d4e54879fdf9e3ac34718f6ca07631239e938e2dec4ca649",
      "vuln":"VULNDB-275958",
      "vulnrabilityId":"VULNDB-275958",
      "package":"log4j-2.13.3",
      "packageCPE":"cpe:/a:-:log4j:2.13.3:-:-",
      "packageName":"log4j",
      "packagePath":"/app/build/install/hipstershop/lib/log4j-api-2.13.3.jar",
      "packageType":"java",
      "severity":"Critical"
   },
   {
      "fullTag":"docker.io/bencer/example-voting-app-worker:jmx-1",
      "imageID":"d483a18d607a33cf6ab56799422b593c20ff2c8cba8626c5c419d0a10d50ba5b",
      "vuln":"VULNDB-275958",
      "vulnrabilityId":"VULNDB-275958",
      "package":"log4j-1.2.12",
      "packageCPE":"cpe:/a:-:log4j:1.2.12:-:-",
      "packageName":"log4j",
      "packagePath":"/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
      "packageType":"java",
      "severity":"Critical"
   },
   {
      "fullTag":"docker.io/bencer/example-voting-app-worker:jmx-1",
      "imageID":"d483a18d607a33cf6ab56799422b593c20ff2c8cba8626c5c419d0a10d50ba5b",
      "vuln":"VULNDB-220038",
      "vulnrabilityId":"VULNDB-220038",
      "package":"log4j-1.2.12",
      "packageCPE":"cpe:/a:-:log4j:1.2.12:-:-",
      "packageName":"log4j",
      "packagePath":"/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
      "packageType":"java",
      "severity":"Critical"
   },
   {
      "fullTag":"docker.io/bencer/example-voting-app-worker:jmx-1",
      "imageID":"d483a18d607a33cf6ab56799422b593c20ff2c8cba8626c5c419d0a10d50ba5b",
      "vuln":"CVE-2020-9488",
      "vulnrabilityId":"CVE-2020-9488",
      "package":"log4j-1.2.12",
      "packageCPE":"cpe:/a:-:log4j:1.2.12:-:-",
      "packageName":"log4j",
      "packagePath":"/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
      "packageType":"java",
      "severity":"Low"
   },
   {
      "fullTag":"docker.io/nestorsalceda/example-voting-app-worker:latest",
      "imageID":"73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
      "vuln":"VULNDB-275958",
      "vulnrabilityId":"VULNDB-275958",
      "package":"log4j-1.2.12",
      "packageCPE":"cpe:/a:-:log4j:1.2.12:-:-",
      "packageName":"log4j",
      "packagePath":"/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
      "packageType":"java",
      "severity":"Critical"
   },
   {
      "fullTag":"docker.io/nestorsalceda/example-voting-app-worker:latest",
      "imageID":"73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
      "vuln":"VULNDB-220038",
      "vulnrabilityId":"VULNDB-220038",
      "package":"log4j-1.2.12",
      "packageCPE":"cpe:/a:-:log4j:1.2.12:-:-",
      "packageName":"log4j",
      "packagePath":"/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
      "packageType":"java",
      "severity":"Critical"
   },
   {
      "fullTag":"docker.io/nestorsalceda/example-voting-app-worker:latest",
      "imageID":"73666529d5ee968a3f85073a771db84f751b34e67069faa31009cc30887ca088",
      "vuln":"CVE-2020-9488",
      "vulnrabilityId":"CVE-2020-9488",
      "package":"log4j-1.2.12",
      "packageCPE":"cpe:/a:-:log4j:1.2.12:-:-",
      "packageName":"log4j",
      "packagePath":"/root/.m2/repository/log4j/log4j/1.2.12/log4j-1.2.12.jar",
      "packageType":"java",
      "severity":"Low"
   },
   {
      "fullTag":"gcr.io/google-samples/microservices-demo/adservice:v0.3.0",
      "imageID":"842294023ab0c8432ee9e2a778986f931c279bc528d06c00b50ac666fcab0417",
      "vuln":"VULNDB-275958",
      "vulnrabilityId":"VULNDB-275958",
      "package":"log4j-2.13.3",
      "packageCPE":"cpe:/a:-:log4j:2.13.3:-:-",
      "packageName":"log4j",
      "packagePath":"/app/build/install/hipstershop/lib/log4j-core-2.13.3.jar",
      "packageType":"java",
      "severity":"Critical"
   },
   {
      "fullTag":"gcr.io/google-samples/microservices-demo/adservice:v0.3.0",
      "imageID":"842294023ab0c8432ee9e2a778986f931c279bc528d06c00b50ac666fcab0417",
      "vuln":"VULNDB-275958",
      "vulnrabilityId":"VULNDB-275958",
      "package":"log4j-2.13.3",
      "packageCPE":"cpe:/a:-:log4j:2.13.3:-:-",
      "packageName":"log4j",
      "packagePath":"/app/build/install/hipstershop/lib/log4j-api-2.13.3.jar",
      "packageType":"java",
      "severity":"Critical"
   }
]
  ```
