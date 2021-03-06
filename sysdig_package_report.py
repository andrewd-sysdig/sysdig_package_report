# Make sure to have 2 environment variables set
# export API_TOKEN="<Your Sysdig Secure API Token>""
# export API_ENDPOINT="https://app.au1.sysdig.com"
# If you are using on-prem you may want to disable SSL Verification by setting:
# export API_SSL_VERIFY=False

import requests
import os
import json
import csv
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_TOKEN = os.getenv('API_TOKEN')
API_ENDPOINT = os.getenv('API_ENDPOINT')
if os.getenv('API_SSL_VERIFY') in ("False","0","false","f"):
    API_SSL_VERIFY = bool(False)
else:
    API_SSL_VERIFY = bool(True)

API_HEADERS = {
  'Authorization': 'Bearer ' + API_TOKEN,
  'Content-Type': 'application/json'
}

result_list = []

def opts():
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--report_type",
                        help="Report type: static|runtime", default="runtime")

    parser.add_argument("-c", "--cluster",
                        help="Filter report on cluster name")

    parser.add_argument("-n", "--namespace",
                        help="Filter report on namespace name")

    parser.add_argument("-p", "--package_name",
                        help="Filter report on package name. ie log4j")

    parser.add_argument("-f", "--custom_filter", default="",
                        help="Filter static reports")

    args = parser.parse_args()

    if args.namespace and not args.cluster:
        parser.error('Cluster is required when passing Namespace')

    return {
        'TYPE':args.report_type,
        'CLUSTER':args.cluster,
        'NAMESPACE':args.namespace,
        'PACKAGE_NAME':args.package_name,
        'FILTER':args.custom_filter
    }

def pipeline_images(registry):
    url = API_ENDPOINT + '/api/scanning/v1/resultsDirect?filter=' + registry + '&sort=desc&sortBy=scanDate'
    response = requests.request("GET", url, headers=API_HEADERS, verify=API_SSL_VERIFY)
    return response.json()

def running_containers(cluster, namespace):
    url = API_ENDPOINT + '/api/scanning/v1/query/containers'
    if namespace is None:
        print('Getting Runtime Images for all Clusters and namespaces ...')
        payload = json.dumps({
            "useCache": True,
            "skipPolicyEvaluation": False,
            "limit": 10000
        })
    else:
        print('Getting Runtime Images for Cluster: ' + cluster + ' and Namespace: ' + namespace + ' ...')
        payload = json.dumps({
        "scope": "kubernetes.cluster.name = \""+cluster+"\" and kubernetes.namespace.name = \""+namespace+"\"",
        "useCache": True,
        "skipPolicyEvaluation": False,
        "limit": 10000
        })
    response = requests.request("POST", url, headers=API_HEADERS, data=payload, verify=API_SSL_VERIFY)
    return response.json()

def non_os_vulns(image):
    url = API_ENDPOINT + "/api/scanning/v1/images/by_id/" + image + "/vulnDirect/non-os"
    response = requests.get(url, headers=API_HEADERS, verify=API_SSL_VERIFY)
    return response.json()

def os_vulns(image):
    url = API_ENDPOINT + "/api/scanning/v1/images/by_id/" + image + "/vulnDirect/os"
    response = requests.get(url, headers=API_HEADERS, verify=API_SSL_VERIFY)
    return response.json()

def vuln_data(image, image_vulns, package_name):
    if package_name is not None:
        for vuln in image_vulns["vulns"]:
            if vuln['package_name'] == package_name:
                dict_data = data_format(image, image_vulns, vuln)
                result_list.append(dict_data)
    else:
        for vuln in image_vulns["vulns"]:
            dict_data = data_format(image, image_vulns, vuln)
            result_list.append(dict_data)

def data_format(image, image_vulns, vuln):
    if 'fullTag' in image:
        dict_format = {
            "fullTag": image['fullTag'],
            "imageID": image['imageId'],
            "vtype": image_vulns.get('vtype', 'None'),
            "vuln": vuln['vuln'],
            "vulnURL": vuln.get('url', 'None'),
            "package": vuln['package'],
            "packageCPE": vuln['package_cpe'],
            "packageName": vuln['package_name'],
            "packagePath": vuln['package_path'],
            "packageType": vuln['package_type'],
            "severity": vuln['severity'],
            "fixVersion":  vuln.get('fix', 'None'),
            "lastEvaluated": image.get('lastEvaluatedAt', '0'),
            "disclosureDate": vuln.get('disclosure_date', '0'),
            "solutionDate": vuln.get('solution_date', '0'),
        }
    elif 'repo' in image:
        dict_format = {
            "fullTag": image['repo'],
            "imageID": image['imageId'],
            "vtype": image_vulns.get('vtype', 'None'),
            "vuln": vuln['vuln'],
            "vulnURL": vuln.get('url', 'None'),
            "package": vuln['package'],
            "packageCPE": vuln['package_cpe'],
            "packageName": vuln['package_name'],
            "packagePath": vuln['package_path'],
            "packageType": vuln['package_type'],
            "severity": vuln['severity'],
            "fixVersion":  vuln.get('fix', 'None'),
            "lastEvaluated": image.get('lastEvaluatedAt', '0'),
            "disclosureDate": vuln.get('disclosure_date', '0'),
            "solutionDate": vuln.get('solution_date', '0'),
        }
    return dict_format

def generate(report_type, package_name, imageList):
    if report_type == 'static':
        for image in imageList["results"]:
            print(image['repository'] + ':' + image['tag'])

            image_vulns = os_vulns(image['imageId'])
            if len(image_vulns['vulns']) != 0:
                vuln_data(image, image_vulns, package_name)

            image_vulns = non_os_vulns(image['imageId'])
            if len(image_vulns['vulns']) != 0:
                vuln_data(image, image_vulns, package_name)
    elif report_type == 'runtime':
        for image in imageList["images"]:
            print(image['repo'] + ':' + image['tag'])

            image_vulns = os_vulns(image['imageId'])
            if len(image_vulns['vulns']) != 0:
                vuln_data(image, image_vulns, package_name)

            image_vulns = non_os_vulns(image['imageId'])
            if len(image_vulns['vulns']) != 0:
                vuln_data(image, image_vulns, package_name)
    return result_list

def main():
    args = opts()
    
    if args['TYPE'] == 'static':
        imageList = pipeline_images(args['FILTER'])
        vulnList = generate(args['TYPE'], args['PACKAGE_NAME'], imageList)

    elif args['TYPE'] == 'runtime':
        imageList = running_containers(args['CLUSTER'], args['NAMESPACE'])
        vulnList = generate(args['TYPE'], args['PACKAGE_NAME'], imageList)

    # Output JSON Results to terminal
    print(json.dumps(vulnList,indent=4, sort_keys=False))

    # Write json file
    with open('output.json', 'w') as outfile:
        json.dump(vulnList, outfile)

    # Write CSV file
    csv_columns = ['fullTag','imageID', 'vtype', 'vuln', 'vulnURL', 'package', 'packageCPE', 'packageName', 'packagePath', 'packageType', 'severity', 'fixVersion', 'lastEvaluated', 'disclosureDate', 'solutionDate' ]
    csv_file = "output.csv"
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in vulnList:
            writer.writerow(data)

if __name__ == '__main__':
    main()