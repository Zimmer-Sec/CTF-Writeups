## Name: PW Crack 4 // Difficulty: Medium // Topic: General Skills (python)

#### By: Kyle Zimmer  
 
**Overview: Utilizing a program we wrote in the last writeup, I was able to use python to interact with the provided program and automate the brute forcing of a hundred passwords in order to find the flag.**       
  
<img width="848" height="559" alt="image" src="https://github.com/user-attachments/assets/556b2116-57b6-4f57-9cf6-eb60a88f1262" />   
   
Upon reviewing the description for this challenge, we’re being given three files and told that there are one hundred passwords with only one being correct. This sounds a lot like the previous write-up we did on [PW Crack 3](https://github.com/Zimmer-Sec/CTF-Writeups/blob/main/PicoCTF/PW%20Crack%203.md). With that in mind, lets take a look at each of the files.       

<img width="1112" height="966" alt="image" src="https://github.com/user-attachments/assets/a45697a5-dbe6-434b-8a90-f722d22d8dfb" />    
    
As expected, the binary hash file and encrypted flag are completely unreadable. Using `cat  level4_checker.py file` reveals the same exact script as the last challenge except for the possible password list defining far more passwords than the last challenge.    
Looking back at “PW Crack 3”, we had seven options and could easily punch those in by hand. Instead of going full caveman on the last challenge, we developed a test script to open the checker program, enter a password from the list, print the results looking for “pico”, and then iterate to the next password in the list if that keyword (the flag) wasn’t seen in stdout. Here’s the syntax we used for that python script.    
   
<img width="562" height="395" alt="image" src="https://github.com/user-attachments/assets/6eb22d7a-0e4c-453d-a246-79c8218c58ef" />  
  
Now all we have to do is update the checker file name and the pw_list to include the other ninety-seven possible guesses and try running it.  
   
<img width="789" height="463" alt="image" src="https://github.com/user-attachments/assets/6d1941ee-4355-4827-bf0d-4aa40a30d019" />   
   
<img width="505" height="161" alt="image" src="https://github.com/user-attachments/assets/ed351287-3ad8-4d48-9cbd-43b9a6cd6ace" />   
    
<img width="662" height="821" alt="image" src="https://github.com/user-attachments/assets/4803ceee-b012-4817-92b0-f5b1f4e4ea0b" />    

Just as planned… it sped through all those password guesses and stopped once it saw “pico”, making it insanely easy to find that flag!

Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.  
