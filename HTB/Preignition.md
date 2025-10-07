## Name: Preignition   //   Difficulty: Very Easy   //   Topic: Dirbusting    
#### By: Kyle Zimmer    
       
**Overview: After stumbling across our first webserver on HTB, we were led to a dead end 404... but there had to be something there. We brute forced the directories for common filenames and found a few of interest.**       
   
<img width="286" height="94" alt="image" src="https://github.com/user-attachments/assets/f9c25bd3-ce72-4e4d-a37e-f785a3514649" />     

To start, let's throw our usual version scan syntax: `nmap -sV -sS -n -Pn --disable-arp-ping [target ip]`     
  
<img width="786" height="194" alt="image" src="https://github.com/user-attachments/assets/20de0d0a-d36a-4ab3-bc86-7e4e70c360c4" />       
   
Knowing that there's an nginx website running on this server. Let's take the easiest first step and just browse to it and maybe try checking for a robots.txt to find restricted file pages.    

<img width="338" height="136" alt="Screenshot 2025-10-06 232902" src="https://github.com/user-attachments/assets/1bcdc4b8-637f-4791-a7f3-d16dc3d2cf70" />     

<img width="912" height="868" alt="image" src="https://github.com/user-attachments/assets/306cde8a-2987-4a7a-8b62-211bea826430" />    

Looks like it's just an unconfigured nginx splash page with nothing hidden in the source code.    

<img width="570" height="273" alt="image" src="https://github.com/user-attachments/assets/0e3d2cdc-11ae-4644-aaa5-8bcecd332553" />     

We also saw that robots.txt was a dud. Let's go ahead and try to see if this server might be storing any other directories or files behind that front page. People often spin up web servers to quickly host files to download across the network (in as short as one command line [i.e. python3 -m http.server])      

We'll use a wordlist from dirbuster (find with `locate dirbuster/wordlists`) to brute force our way to any possible hidden files or folders.      

<img width="579" height="190" alt="image" src="https://github.com/user-attachments/assets/df16cfca-2d35-4de5-b304-e6e84b286d7b" />    

As a taste of what's inside one of these files, I've ran the `more` utility on the medium list:    

<img width="572" height="919" alt="image" src="https://github.com/user-attachments/assets/e84bdd11-f420-47f6-9319-12e9e4bc955a" />     

`gobuster dir --url 10.129.105.170 --wordlist /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -e .php --ne`   

* `gobuster dir`: Specify directory/file brute forcing
* `--url http://[target ip]:80/`: specifies the target domain (url) we want to direct our enumeration at.
* `--follow-redirect`: Follow any redirect HTTP codes.
* `--wordlist [path]`: Specifies the wordlist to iterate through at the end of the URL.
* `--ne`: No errors -- Won't display them.

<img width="1190" height="308" alt="image" src="https://github.com/user-attachments/assets/e3053ff1-aca7-4c9a-8ea1-a56d04f00e2b" />     
 
Halfway through this query I had to swap out the medium.txt for the small.txt and it still took my VM over 10 minutes to run without finding anything. The questions along with the box hint me towards searching for php files, so I'm going to add `-e ".php"` onto the end to steer use in the right direciton.       

<img width="542" height="60" alt="image" src="https://github.com/user-attachments/assets/9e0d5a0d-fa19-4154-b052-3dba19495fbb" />

We see that it found admin.php as a file being hosted by the web server. We can use curl to query for that page in our terminal and display the HTTP headers in detail with -v: `curl http://[target ip]/admin.php -v`     

<img width="1131" height="811" alt="image" src="https://github.com/user-attachments/assets/395c1135-9d22-4f04-a5d2-5c4eed55e381" />    

It successfully (response code 200) returned what looks to be an admin login page. Lets browse to it in our browser.

<img width="779" height="449" alt="image" src="https://github.com/user-attachments/assets/0c83f08b-f478-487d-88d2-ec1550dd5c9d" />   

Being that we don't have any further information about this system, we can only assume that this box is not configured and likely using default or simple credentials for anything. With that in mind, I'm going to throw some default-ish looking creds in-line with the title of this page: admin.php.... admin/password, admin/pass, admin/admin.        

<img width="791" height="245" alt="image" src="https://github.com/user-attachments/assets/f8e4dae1-eb1b-483c-8b9d-03536432df8c" />     

And Bob's your uncle! admin/admin worked. Highly insecure, but this is the type of service you'd see on someone's system that needs to get a quick job done. In a production envrionment, this would be unacceptable.   

<img width="678" height="577" alt="image" src="https://github.com/user-attachments/assets/e059b90f-b0fc-44c0-bff1-e59c6cd70da7" />   


Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.     
