grid_search = {'temperature': [0, 1],
               'prompts': ["""Use the following step-by-step guide to extract information from cyber threat reports. 

Step 1 - Extract the starting date of the campaign, the Advanced Persistent Threats (APTs), the CVE codes of the vulnerabilities exploited by the APT, and the attack vectors which the APT used.

         Note: - The name of the actor in the campaign and the name of the APT must be the same. 
               - If there is more than one date available list them all, but always convert them in the indicated format. 
               - Only extract the CVE which are directly attributed to the threat actor in the report. 
               - Only extract the attack vectors which are directly attributed to the threat actor in the report. 
               - It is possible to have more than one vulnerability. 
               - It is possible to have more than one attack vector. 
               - The name of the attack vector can only be one of the following: drive-by compromise, supply chain compromise, exploit public-facing application, spearphishing via service, spearphishing attachment, valid accounts, external remote services, spearphishing link.
               - In case the attack vector is unknown assign to it 'unknown'. 
               - Each node will have an id, composed of the acronym of the node and the number of the entity.
               - If you do not find the name of the attack vector or the vulnerability, do not create the dictionary in the belonging list.
                   
Step 2 - Return the information filling in this JSON format: 

         "nodes": {
            "campaign": [
                {
                    "actor": "", // name of the threat actor
                    "date_start": ["yyyy-mm", "yyyy-mm"], // list of dates
                    "id": "campaign1" // id of the campaign
                }
            ],
            "APT": [
                {
                    "name": "", // name of the threat actor
                    "id": "APT1" // id of the APT
                }
            ],
            "attack_vector": [
                {
                    "name": "",  // name of the attack vector
                    "id": "attack_vector1" // id of the attack vector
                },
                {
                    "name": "", // name of the attack vector
                    "id": "attack_vector2" // id of the attack vector
                }             
            ],
            "vulnerability": [
                {
                    "name": "CVE-yyyy-", // name of the vulnerability                                                  
                    "id": "vulnerability1" // id of the vulnerability
                },
                {                                                        
                    "name": "CVE-yyyy-", // name of the vulnerability                                                   
                    "id": "vulnerability2" // id of the vulnerability
                }
            ]
        }
""",
"""Use the following step-by-step guide to extract information from cyber threat reports. 

Step 1 - Extract the starting date of the campaign, the Advanced Persistent Threats (APTs), the CVE codes of the vulnerabilities exploited by the APT, and the attack vectors which the APT used.

         Note: - The name of the actor in the campaign and the name of the APT must be the same. 
               - If there is more than one date available list them all, but always convert them in the indicated format. 
               - Only extract the CVE which are directly attributed to the threat actor in the report. 
               - Only extract the attack vectors which are directly attributed to the threat actor in the report. 
               - It is possible to have more than one vulnerability. 
               - It is possible to have more than one attack vector. 
               - The name of the attack vector can only be one of the following: drive-by compromise, supply chain compromise, exploit public-facing application, spearphishing via service, spearphishing attachment, valid accounts, external remote services, spearphishing link.
               - In case the attack vector is unknown assign to it 'unknown'. 
               - Each node will have an id, composed of the acronym of the node and the number of the entity.
               - If you do not find the name of the attack vector or the vulnerability, do not create the dictionary in the belonging list.

        Examples to help understand which attack vector the APT used: 
            "to configure a client-side mail rule crafted to download and execute a malicious payload from an adversary-controlled WebDAV server" -> spearphishing attachment. 
            "We also confirmed that the user installed this program via a download link delivered over email." -> spearphishing link. 
            "the sites, which appear to be Outlook Web Access, Yahoo, and Google login pages, have been leveraged in spear-phishing messages." -> spearphishing via service.
            "has been linked to a watering hole attack" -> drive-by compromise.
            "Initial Access External Remote Services" -> external remote services.
            "employed legitimate user credentials to access its targets' networks." -> valid accounts. 
   
Step 2 - Return the information filling in this JSON format: 

         "nodes": {
            "campaign": [
                {
                    "actor": "", // name of the threat actor
                    "date_start": ["yyyy-mm", "yyyy-mm"], // list of dates
                    "id": "campaign1" // id of the campaign
                }
            ],
            "APT": [
                {
                    "name": "", // name of the threat actor
                    "id": "APT1" // id of the APT
                }
            ],
            "attack_vector": [
                {
                    "name": "",  // name of the attack vector
                    "id": "attack_vector1" // id of the attack vector
                },
                {
                    "name": "", // name of the attack vector
                    "id": "attack_vector2" // id of the attack vector
                }             
            ],
            "vulnerability": [
                {
                    "name": "CVE-yyyy-", // name of the vulnerability                                                  
                    "id": "vulnerability1" // id of the vulnerability
                },
                {                                                       
                    "name": "CVE-yyyy-", // name of the vulnerability                                                   
                    "id": "vulnerability2" // id of the vulnerability
                }
            ]
        }
"""]}

grid_search_infer = {'temperature': [0, 1],
                     'prompts': [
"""Use the following step-by-step guide to find, based on your knowledge, information about a specific Advanced Persistent Threat (APT), given its name and description.

Step 1 - Find the country of the APT, all the attack vectors employed by the APT, all the vulnerabilities exploited by the APT, the goal of the APT, and the label of the APT. 
         
         Note: - It is possible to have only one country. 
               - It is possible to have more than one vulnerability. 
               - It is possible to have more than one attack vector.
               - The name of the attack vector can be one of the followings: Credential Dumping, Command-Line Interface, Remote Desktop Protocol, Data from Local System, Data Compressed, Scripting, Process Discovery, Email Collection, Masquerading, System Network Connections Discovery, Account Discovery, Automated Collection, Pass the Hash, Network Share Discovery, System Service Discovery, System Network Configuration Discovery, Unknown, User Execution, Exploitation for Client Execution, Spearphishing Attachment, Web Service, External Remote Services, File and Directory Discovery, Obfuscated Files or Information, Standard Application Layer Protocol, Valid Accounts, Commonly Used Port, Registry Run Keys / Startup Folder, Remote File Copy, Scheduled Task, File Deletion, System Information Discovery, Data Encoding, Regsvr32, Rundll32, System Owner/User Discovery, DLL Side-Loading, Modify Registry, PowerShell, Drive-by Compromise, Modify Existing Service, Deobfuscate/Decode Files or Information, Hidden Window, Data Obfuscation, Replication Through Removable Media, Dynamic Data Exchange, Hidden Files and Directories, Timestomp, Spearphishing Link, Peripheral Device Discovery, Screen Capture, Indicator Removal on Host, Component Object Model Hijacking, Data from Information Repositories, Logon Scripts, Network Sniffing, Bootkit, Exploitation for Privilege Escalation, Exploitation for Defense Evasion, Access Token Manipulation, Data from Removable Media, Data Staged, Trusted Relationship, Communication Through Removable Media, Rootkit, Connection Proxy, Exploitation of Remote Services, Input Capture, Office Application Startup, Template Injection, Custom Cryptographic Protocol, Application Access Token, Steal Application Access Token, Accessibility Features, Bypass User Account Control, Windows Management Instrumentation Event Subscription, Software Packing, Multi-hop Proxy, Windows Management Instrumentation, Pass the Ticket, Domain Fronting, Standard Non-Application Layer Protocol, Shortcut Modification, Redundant Access, Graphical User Interface, Remote System Discovery, Uncommonly Used Port, Permission Groups Discovery, New Service, Multi-Stage Channels, Exfiltration Over Command and Control Channel, Create Account, Indicator Removal from Tools, Account Manipulation, Windows Admin Shares, Brute Force, Credentials in Files, Application Deployment Software, Web Shell, NTFS File Attributes, Binary Padding, Signed Script Proxy Execution, Mshta, Custom Command and Control Protocol, Network Service Scanning, Data Encrypted, Query Registry, Service Execution, File and Directory Permissions Modification, Exfiltration Over Alternative Protocol, Standard Cryptographic Protocol, Execution Guardrails, Audio Capture, Execution through API, Process Injection, Disk Structure Wipe, Code Signing, System Shutdown/Reboot, Clipboard Data, Runtime Data Manipulation, Transmitted Data Manipulation, Stored Data Manipulation, Data Encrypted for Impact, Data Destruction, Remote Services, Domain Generation Algorithms, Supply Chain Compromise, Resource Hijacking, Clear Command History, Fallback Channels, Compiled HTML File, System Time Discovery, Data from Network Shared Drive, Disabling Security Tools, Remote Access Tools, CMSTP, Security Software Discovery, XSL Script Processing, Signed Binary Proxy Execution, Spearphishing via Service, Forced Authentication, Taint Shared Content, Component Firmware, Input Prompt, Video Capture, Application Shimming, Virtualization/Sandbox Evasion, Process Hollowing, AppCert DLLs, Automated Exfiltration, Change Default File Association, Browser Extensions, Application Window Discovery, Multiband Communication, Service Stop, Disk Content Wipe, BITS Jobs, Component Object Model and Distributed COM, Compile After Delivery, Credentials from Web Browsers, Exploit Public-Facing Application, Password Policy Discovery, Hooking, Image File Execution Options Injection, DLL Search Order Hijacking, Windows Remote Management, Data Transfer Size Limits, Network Share Connection Removal, Winlogon Helper DLL, PowerShell Profile.
               - It is possible to have only one goal.
               - The goal of the APT can be one of the followings: 'espionage,sabotage', 'espionage', 'espionage,financial gain,sabotage', 'financial gain', 'sabotage', 'espionage,financial gain'.
               - The APT can have only one label. 
               - The label of the APT can be one of the followings: 'spy', 'criminal', 'terrorist', 'nation-state', 'crime-syndicate', 'activist'.
               - Each node will have an id, composed of the acronym of the node and the number of the entity. 
 
Step 2 - Return the information filling in this JSON format:   
 
          "nodes": {
             "APT": [
                 {
                     "name": "", // name of the APT
                     "goals": "", // goal of the APT
                     "labels": "", // type of the APT
                     "id": "APT1", // id of the APT
                 }
             ]
             "country": [
                 {
                     "name": "", // name of the country the APT is from
                     "id": "country1" // id of the country
                 }
             ], 
             "attack_vector": [
                 {
                     "name": "", // name of the attack vector                                       
                     "id": "attack_vector1" // id of the attack vector
                 }, 
                 {
                     "name": "", // name of the attack vector
                     "id": "attack_vector2" // id of the attack vector
                 }
             ]
             "vulnerability": [
                 {
                     "name": "CVE-yyyy-", // name of the vulnerability                                                  
                     "id": "vulnerability1" // id of the vulnerability
                 },
                 {                                                          
                     "name": "CVE-yyyy-", // name of the vulnerability                                                   
                     "id": "vulnerability2" // id of the vulnerability
                 }
             ]                                      
         }
""",
"""Use the following step-by-step guide to find, based on your knowledge, information about a specific Advanced Persistent Threat (APT), given its name and description.
                         
Step 1 - Find the country of the APT, all the attack vectors employed by the APT, all the vulnerabilities exploited by the APT, the goal of the APT, and the label of the APT. 
 
          Note: - It is possible to have only one country. 
                - It is possible to have more than one vulnerability. 
                - It is possible to have more than one attack vector.
                - The name of the attack vector can be one of the followings: Credential Dumping, Command-Line Interface, Remote Desktop Protocol, Data from Local System, Data Compressed, Scripting, Process Discovery, Email Collection, Masquerading, System Network Connections Discovery, Account Discovery, Automated Collection, Pass the Hash, Network Share Discovery, System Service Discovery, System Network Configuration Discovery, Unknown, User Execution, Exploitation for Client Execution, Spearphishing Attachment, Web Service, External Remote Services, File and Directory Discovery, Obfuscated Files or Information, Standard Application Layer Protocol, Valid Accounts, Commonly Used Port, Registry Run Keys / Startup Folder, Remote File Copy, Scheduled Task, File Deletion, System Information Discovery, Data Encoding, Regsvr32, Rundll32, System Owner/User Discovery, DLL Side-Loading, Modify Registry, PowerShell, Drive-by Compromise, Modify Existing Service, Deobfuscate/Decode Files or Information, Hidden Window, Data Obfuscation, Replication Through Removable Media, Dynamic Data Exchange, Hidden Files and Directories, Timestomp, Spearphishing Link, Peripheral Device Discovery, Screen Capture, Indicator Removal on Host, Component Object Model Hijacking, Data from Information Repositories, Logon Scripts, Network Sniffing, Bootkit, Exploitation for Privilege Escalation, Exploitation for Defense Evasion, Access Token Manipulation, Data from Removable Media, Data Staged, Trusted Relationship, Communication Through Removable Media, Rootkit, Connection Proxy, Exploitation of Remote Services, Input Capture, Office Application Startup, Template Injection, Custom Cryptographic Protocol, Application Access Token, Steal Application Access Token, Accessibility Features, Bypass User Account Control, Windows Management Instrumentation Event Subscription, Software Packing, Multi-hop Proxy, Windows Management Instrumentation, Pass the Ticket, Domain Fronting, Standard Non-Application Layer Protocol, Shortcut Modification, Redundant Access, Graphical User Interface, Remote System Discovery, Uncommonly Used Port, Permission Groups Discovery, New Service, Multi-Stage Channels, Exfiltration Over Command and Control Channel, Create Account, Indicator Removal from Tools, Account Manipulation, Windows Admin Shares, Brute Force, Credentials in Files, Application Deployment Software, Web Shell, NTFS File Attributes, Binary Padding, Signed Script Proxy Execution, Mshta, Custom Command and Control Protocol, Network Service Scanning, Data Encrypted, Query Registry, Service Execution, File and Directory Permissions Modification, Exfiltration Over Alternative Protocol, Standard Cryptographic Protocol, Execution Guardrails, Audio Capture, Execution through API, Process Injection, Disk Structure Wipe, Code Signing, System Shutdown/Reboot, Clipboard Data, Runtime Data Manipulation, Transmitted Data Manipulation, Stored Data Manipulation, Data Encrypted for Impact, Data Destruction, Remote Services, Domain Generation Algorithms, Supply Chain Compromise, Resource Hijacking, Clear Command History, Fallback Channels, Compiled HTML File, System Time Discovery, Data from Network Shared Drive, Disabling Security Tools, Remote Access Tools, CMSTP, Security Software Discovery, XSL Script Processing, Signed Binary Proxy Execution, Spearphishing via Service, Forced Authentication, Taint Shared Content, Component Firmware, Input Prompt, Video Capture, Application Shimming, Virtualization/Sandbox Evasion, Process Hollowing, AppCert DLLs, Automated Exfiltration, Change Default File Association, Browser Extensions, Application Window Discovery, Multiband Communication, Service Stop, Disk Content Wipe, BITS Jobs, Component Object Model and Distributed COM, Compile After Delivery, Credentials from Web Browsers, Exploit Public-Facing Application, Password Policy Discovery, Hooking, Image File Execution Options Injection, DLL Search Order Hijacking, Windows Remote Management, Data Transfer Size Limits, Network Share Connection Removal, Winlogon Helper DLL, PowerShell Profile.
                - The APT can have only one goal.
                - The goal of the APT can be one of the followings: 'espionage,sabotage', 'espionage', 'espionage,financial gain,sabotage', 'financial gain', 'sabotage', 'espionage,financial gain'.
                - The APT can have only one label. 
                - The label of the APT can be one of the followings: 'crime-syndicate', 'spy', 'terrorist', 'criminal', 'nation-state', 'activist'.
                - Each node will have an id, composed of the acronym of the node and the number of the entity. 
                
          Examples to help understand which country the APT is from: 
              "APT37 is a suspected North Korean cyber espionage group" -> North Korea
              "APT39 have targeted the telecommunication and travel industries to collect personal information that aligns with Iran's national priorities" -> Iran
              "Threat Group-3390 is a Chinese threat group that has extensively used strategic Web compromises to target victims" -> China
            
          Examples to help understand the goal of the APT: 
              "APT 38 concentrates on stealing money" -> financial gain
              "APT39 have targeted the telecommunication and travel industries to collect personal information that aligns with Iran's national priorities" -> espionage
              "APT33 has shown particular interest in organizations in the aviation sector involved in both military and commercial capacities, as well as organizations in the energy sector" -> espionage,sabotage
              
          Examples to help understand the label of the APT: 
              "APT39 have targeted the telecommunication and travel industries to collect personal information that aligns with Iran's national priorities" -> nation-state
              "APT41 is a group that carries out Chinese state-sponsored espionage activity" -> nation-state 
 
 Step 2 - Return the information filling in this JSON format:   
 
          "nodes": {
             "APT": [
                 {
                     "name": "", // name of the APT
                     "goals": "", // goal of the APT
                     "labels": "", // type of the APT
                     "id": "APT1", // id of the APT
                 }
             ]
             "country": [
                 {
                     "name": "", // name of the country the APT is from
                     "id": "country1" // id of the country
                 }
             ], 
             "attack_vector": [
                 {
                     "name": "", // name of the attack vector                                       
                     "id": "attack_vector1" // id of the attack vector
                 }, 
                 {
                     "name": "", // name of the attack vector
                     "id": "attack_vector2" // id of the attack vector
                 }
             ]
             "vulnerability": [
                 {
                     "name": "CVE-yyyy-", // name of the vulnerability                                                  
                     "id": "vulnerability1" // id of the vulnerability
                 },
                 {                                                          
                     "name": "CVE-yyyy-", // name of the vulnerability                                                   
                     "id": "vulnerability2" // id of the vulnerability
                 }
             ]                                      
         }
 """]}

relations = """relations": {
                     "origins": [
                         [
                             "APT1",
                             "country"
                         ]
                     ],
                     "targets": [
                         [
                             "campaign1",
                             "vulnerability1"
                         ],
                         [
                             "campaign1",
                             "vulnerability2"
                         ]
                     ],
                     "uses": [
                         [
                             "campaign1",
                             "attack_vector1"
                         ]
                     ]
            }
"""


prompt_dates = """You are a Cyber Threat Analyst. Use the following step-by-step guide to extract information from cyber threat reports. 

Step 1 - Find all the dates present in the report.

Note: - If there is more than one date list them all. 
      - Examples of formats in which you will fine the dates: May 2015, 2015/05, 2015
      - Always convert the dates you find in the format: yyyy-mm. If there is not the month, the month is January.

Step 2 - Return the information filling this JSON format: 

        {
            "nodes": {
                "date_start": ["yyyy-mm", "yyyy-mm", "yyyy-mm"]
            }
        }
"""

json_campaign_validation = ['259.json', '253.json', '305.json', '88.json', '233.json', '173.json', '311.json',
                            '99.json', '35.json', '190.json', '15.json', '218.json', '14.json', '59.json', '45.json',
                            '111.json', '103.json', '206.json', '2.json', '203.json', '294.json', '130.json',
                            '325.json', '289.json', '213.json', '296.json', '3.json', '333.json', '193.json',
                            '247.json', '196.json', '270.json', '209.json', '77.json', '200.json', '10.json',
                            '1.json', '139.json', '107.json', '131.json', '91.json', '49.json', '17.json', '228.json',
                            '65.json', '89.json', '312.json', '249.json', '210.json', '69.json', '227.json', '264.json',
                            '157.json', '75.json', '290.json', '147.json', '6.json', '121.json', '188.json', '141.json',
                            '266.json', '56.json', '60.json', '256.json', '216.json', '25.json', '109.json', '208.json',
                            '76.json', '0.json', '235.json', '163.json', '197.json', '164.json', '328.json', '207.json',
                            '338.json', '162.json', '28.json', '105.json', '38.json', '136.json', '64.json', '242.json',
                            '53.json', '192.json', '263.json', '71.json', '229.json', '255.json', '117.json', '297.json',
                            '132.json', '172.json', '29.json', '20.json', '217.json', '144.json', '100.json', '237.json',
                            '243.json', '135.json', '223.json', '12.json', '267.json', '323.json', '212.json',
                            '257.json', '286.json', '248.json', '134.json', '187.json', '33.json', '310.json', '148.json',
                            '198.json', '4.json', '72.json', '246.json', '302.json', '161.json', '191.json', '321.json',
                            '251.json', '145.json', '204.json', '271.json', '234.json', '219.json', '180.json',
                            '159.json', '87.json', '66.json', '244.json', '230.json', '140.json', '138.json',
                            '106.json', '260.json', '62.json', '26.json', '326.json', '52.json', '285.json', '258.json',
                            '252.json', '167.json', '238.json', '335.json', '336.json', '300.json', '332.json',
                            '74.json', '272.json', '250.json', '92.json', '224.json', '189.json', '160.json', '166.json',
                            '182.json', '334.json', '50.json', '327.json', '73.json', '47.json', '21.json', '101.json',
                            '225.json', '301.json', '194.json', '110.json', '299.json', '24.json']

json_campaign_test = ['104.json', '108.json', '112.json', '119.json', '128.json', '129.json', '133.json', '142.json',
                      '143.json', '146.json', '155.json', '156.json', '168.json', '169.json', '170.json', '171.json',
                      '174.json', '18.json', '181.json', '183.json', '184.json', '185.json', '186.json', '19.json',
                      '195.json', '201.json', '214.json', '215.json', '220.json', '221.json', '222.json', '232.json',
                      '236.json', '239.json', '240.json', '241.json', '245.json', '265.json', '269.json', '287.json',
                      '291.json', '292.json', '295.json', '30.json', '306.json', '31.json', '313.json', '315.json',
                      '320.json', '324.json', '330.json', '337.json', '339.json', '340.json', '37.json', '40.json',
                      '43.json', '46.json', '48.json', '51.json', '54.json', '55.json', '61.json', '63.json', '67.json',
                      '68.json', '7.json', '70.json', '86.json', '9.json', '90.json', '93.json', '97.json', '98.json']

json_context_validation = ['76.json', '57.json', '28.json', '29.json', '38.json', '63.json', '77.json', '37.json',
                           '44.json', '50.json', '7.json', '81.json', '1.json', '54.json', '65.json', '47.json',
                           '27.json', '25.json', '84.json', '35.json', '46.json', '75.json', '48.json', '32.json',
                           '5.json', '15.json', '67.json', '64.json', '6.json', '72.json', '20.json', '42.json',
                           '36.json', '43.json', '30.json', '22.json', '24.json', '26.json', '49.json', '45.json',
                           '31.json', '18.json', '14.json', '56.json', '16.json', '68.json', '13.json', '23.json',
                           '4.json', '2.json', '71.json', '58.json', '82.json', '51.json', '21.json', '70.json',
                           '12.json', '11.json', '10.json', '74.json']

json_context_test = ['61.json', '19.json', '0.json', '39.json', '66.json', '55.json', '41.json', '80.json', '83.json',
                     '34.json', '52.json', '33.json', '40.json', '8.json', '9.json', '79.json', '17.json', '59.json',
                     '53.json', '60.json', '78.json', '62.json', '73.json', '3.json', '69.json']

