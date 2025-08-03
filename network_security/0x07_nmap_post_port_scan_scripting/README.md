# Nmap Post Port Scan & Scripting

This project demonstrates advanced Nmap usage for post-port scan scripting, vulnerability detection, and service enumeration.

## Scripts

- **0-nmap_default.sh**  
  Runs Nmap with default scripts and service/version detection.  
  `nmap -sC -sV "$1"`

- **1-nmap_vulners.sh**  
  Scans ports 80 and 443 for vulnerabilities using the vulners script.  
  `nmap -p 80,443 --script vulners "$1"`

- **2-vuln_scan.sh**  
  Uses the http-vuln-cve2017-5638 script to check for a specific vulnerability.  
  `nmap --script http-vuln-cve2017-5638 "$1" -oN vuln_scan_results.txt`

- **3-comprehensive_scan.sh**  
  Runs multiple scripts for HTTP, SSL, and FTP vulnerabilities.  
  `nmap --script http-vuln-cve2017-5638,ssl-enum-ciphers,ftp-anon "$1" -oN comprehensive_scan_results.txt`

- **4-vulnerability_scan.sh**  
  Runs all scripts matching http-vuln*, mysql-vuln*, ftp-vuln*, smtp-vuln*.  
  `nmap --script http-vuln* mysql-vuln* ftp-vuln* smtp-vuln* "$1" -oN vulnerability_scan_results.txt`

- **5-service_enumeration.sh**  
  Enumerates services and runs banner, SSL, default, and SMB domain enumeration scripts.  
  `nmap -sV -A --script="banner,ssl-enum-ciphers,default,smb-enum-domains" "$1" -oN service_enumeration_results.txt`

## Usage

Each script should be run with the target IP or domain as the first argument.  
Example:  
```sh
[0-nmap_default.sh](http://_vscodecontentref_/0) example.com