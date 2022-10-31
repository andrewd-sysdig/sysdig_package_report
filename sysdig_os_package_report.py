# This script queries the legacy runtime engine os packages installed, even if there are no vulnerabilities in it.

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

    parser.add_argument("-c", "--cluster",
                        help="Filter report on cluster name")

    parser.add_argument("-n", "--namespace",
                        help="Filter report on namespace name")

    parser.add_argument("-p", "--package_name",
                        help="Filter report on package name. ie openssl",
                        required=True)

    args = parser.parse_args()

    if args.namespace and not args.cluster:
        parser.error('Cluster is required when passing Namespace')

    return {
        'CLUSTER':args.cluster,
        'NAMESPACE':args.namespace,
        'PACKAGE_NAME':args.package_name
    }

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

def get_os_packages(image):
    url = API_ENDPOINT + "/api/scanning/v1/images/by_id/" + image + "/content/os"
    response = requests.get(url, headers=API_HEADERS, verify=API_SSL_VERIFY)
    return response.json()


def generate(package_name, imageList):
    for image in imageList["images"]:
        #print(image['repo'] + ':' + image['tag'])
        packages = get_os_packages(image['imageId']) # returns json payload including all os packages for this image

        #print(json.dumps(packages,indent=4, sort_keys=False))
        if 'content' in packages: #if the package hasn't been scanned then skip it
            for package in packages["content"]:
                if package['package'] == package_name:
                    dict_data = data_format(image, package)
                    result_list.append(dict_data)
                    # Print out Repo:Tag, imageID, Package Naame, package version
                    # print(image['repo'] + ':' + image['tag'] + ", " + image['imageId'] + ", " + package['package'] + ", " + package['version'] )
    return result_list

def data_format(image, package):
    dict_format = {
        "fullTag": image['repo'] + ":" + image['tag'],
        "imageID": image['imageId'],
        "packageName": package['package'],
        "packageVersion": package['version'],
    }
    return dict_format

def main():
    args = opts()

    imageList = running_containers(args['CLUSTER'], args['NAMESPACE'])
    packageList = generate(args['PACKAGE_NAME'], imageList)

    # Output JSON Results to terminal
    print(json.dumps(packageList,indent=4, sort_keys=False))

    # Write json file
    with open('output.json', 'w') as outfile:
        json.dump(packageList, outfile)

    # Write CSV file
    csv_columns = ['fullTag','imageID', 'packageName', 'packageVersion']
    csv_file = "output.csv"
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in packageList:
            writer.writerow(data)


if __name__ == '__main__':
    main()