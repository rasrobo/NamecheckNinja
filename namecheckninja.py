import requests
from xml.etree import ElementTree as ET
from tabulate import tabulate
import argparse
from datetime import datetime
import logging
import subprocess

# Configuration
api_username = '***********'
api_key = '***********'
username = '***********'
client_ip = '***********'

def run_curl_command(api_username, api_key, username, client_ip):
    curl_command = f'curl -s "https://api.namecheap.com/xml.response?ApiUser={api_username}&ApiKey={api_key}&UserName={username}&ClientIp={client_ip}&Command=namecheap.domains.getList"'
    result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
    return result.stdout

def get_all_domains(verbose=False):
    all_domains = []
    page = 1
    while True:
        url = f"https://api.namecheap.com/xml.response?ApiUser={api_username}&ApiKey={api_key}&UserName={username}&ClientIp={client_ip}&Command=namecheap.domains.getList&Page={page}"
        response = requests.get(url)
        
        if verbose:
            logging.debug(f"Domain list API response (Page {page}): {response.status_code}")
            logging.debug(f"Domain list API response content (Page {page}):\n{response.text}")
        
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            
            if verbose:
                logging.debug(f"XML structure:\n{ET.tostring(root, encoding='unicode', method='xml')}")
            
            # Define the namespace
            namespace = {'nc': 'http://api.namecheap.com/xml.response'}
            
            command_response = root.find(".//nc:CommandResponse", namespace)
            if command_response is None:
                logging.error("Could not find CommandResponse element in the XML response")
                break
            
            domain_list_result = command_response.find("nc:DomainGetListResult", namespace)
            if domain_list_result is None:
                logging.error("Could not find DomainGetListResult element in the XML response")
                break
            
            domains = domain_list_result.findall("nc:Domain", namespace)
            if not domains:
                logging.debug(f"No domains found on page {page}")
                break
            
            for domain in domains:
                domain_info = {
                    'Domain Name': domain.attrib.get('Name', 'N/A'),
                    'Created': domain.attrib.get('Created', 'N/A'),
                    'Expires': domain.attrib.get('Expires', 'N/A'),
                    'IsExpired': domain.attrib.get('IsExpired', 'N/A'),
                    'IsLocked': domain.attrib.get('IsLocked', 'N/A'),
                    'AutoRenew': domain.attrib.get('AutoRenew', 'N/A'),
                    'WhoisGuard': domain.attrib.get('WhoisGuard', 'N/A'),
                    'IsPremium': domain.attrib.get('IsPremium', 'N/A'),
                    'IsOurDNS': domain.attrib.get('IsOurDNS', 'N/A')
                }
                all_domains.append(domain_info)
            
            paging_info = command_response.find("nc:Paging", namespace)
            if paging_info is not None:
                total_items = int(paging_info.find("nc:TotalItems", namespace).text)
                current_page = int(paging_info.find("nc:CurrentPage", namespace).text)
                page_size = int(paging_info.find("nc:PageSize", namespace).text)
                
                if current_page * page_size >= total_items:
                    break
            else:
                break
            
            page += 1
        else:
            logging.error(f"Error fetching domain list: {response.status_code} - {response.text}")
            break
    
    if verbose:
        logging.debug(f"Total domains fetched: {len(all_domains)}")
    
    return all_domains

def main():
    parser = argparse.ArgumentParser(description="Fetch and display Namecheap domain information.")
    parser.add_argument('--verbose', action='store_true', help="Enable verbose output for debugging")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    if args.verbose:
        curl_output = run_curl_command(api_username, api_key, username, client_ip)
        logging.debug(f"Curl command output:\n{curl_output}")

    domains = get_all_domains(args.verbose)

    # Sort domains by IsExpired status (true first), then by Expires date ascending
    domains_sorted = sorted(
        domains,
        key=lambda x: (
            x.get('IsExpired') == 'false',  # True should come before False
            datetime.strptime(x.get('Expires'), '%m/%d/%Y'),
        )
    )

    domain_info = []
    for index, domain in enumerate(domains_sorted, start=1):
        domain_info.append([
            index,
            domain.get('Domain Name', 'N/A'),
            domain.get('Created', 'N/A'),
            domain.get('Expires', 'N/A'),
            domain.get('IsExpired', 'N/A'),
            domain.get('IsLocked', 'N/A'),
            domain.get('AutoRenew', 'N/A'),
            domain.get('WhoisGuard', 'N/A'),
            domain.get('IsPremium', 'N/A'),
            domain.get('IsOurDNS', 'N/A')
        ])

    headers = [
        "Index",
        "Domain Name",
        "Created",
        "Expires",
        "IsExpired",
        "IsLocked",
        "AutoRenew",
        "WhoisGuard",
        "IsPremium",
        "IsOurDNS"
    ]

    print(tabulate(domain_info, headers=headers, tablefmt='grid'))

    active_domains_count = sum(1 for domain in domains if domain.get('IsExpired') == 'false')
    print(f"\nTotal active domains: {active_domains_count}")

if __name__ == "__main__":
    main()