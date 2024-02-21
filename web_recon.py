#! usr/share/bin/env python

import requests


def request(url):
    try:
        return requests.get("https://" + url)
    except requests.exceptions.ConnectionError or KeyboardInterrupt:
        pass


print("1.Subdomain Enumeration\n2.Directory Enumeration")

opt = int(input("Chose Option: "))
u_target = str(input("Enter the URL: (eg google.com): "))
if opt == 1:
    target_url = u_target
    with open("E:/Codes/Bug_Bounty_Scripts/Domains/Wordlists/subdomains_2.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = word + "." + target_url
            response = request(test_url)
            if response:
                print("[+]Discovered Subdomain ---> " + test_url)
            else:
                pass

else:
    target_url= u_target
    with open("E:/Codes/Bug_Bounty_Scripts/Domains/Wordlists/subdomains_2.txt", "r") as wordlist_file:
        for line in wordlist_file:
            word = line.strip()
            test_url = target_url+ "/"+ word
            response = request(test_url)
            if response:
                print("[+]Discovered URL ---> " + test_url)
            else:
                pass

