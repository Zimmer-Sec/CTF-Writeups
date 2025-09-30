## Name: repetitions // Difficulty: Easy // Topic: General Skills (encoding)   
   
#### By: Kyle Zimmer  
   
**Overview: I decided to create a writeup on this challenge because it presented an interesting solution that I had to do a double-take at. The challenge requires you to investigate an encoded text file, but what it was deeper than just one decode...**     

<img width="860" height="471" alt="image" src="https://github.com/user-attachments/assets/5dcfbcda-064a-46ad-be5e-d917ea43a99d" />  

Getting into this, we only have one file to work with. Using `file enc_flag`, we see that it appears to only be plain ASCII text. Opening it with `cat enc_flag` reveals the following data:  

<img width="629" height="167" alt="image" src="https://github.com/user-attachments/assets/2c35c3ae-8a23-48b8-be7e-4819a39cc138" />  

Just from my experience, I can spot the encoding method used right off the rip. The biggest giveaway is the double equals symbols at the end. If you don't know what that hints at, that's okay!   

*Base64 is an encoding algorithm that takes in binary (unreadable 1s and 0s) data and translates it to text using its own 64-characters. After the binary data has been translated (encoded), the algorithm requires that the total data length is a multiple of four characters. If it isn't, it will append equals signs onto the end to meet (or "pad") it to the required length. This padding also gives away the unique encoding mechanism base64.*    
   
Linux comes with a built in base64 utility to help us. We can decode (-d) the file with `base64 -d enc_flag` and output the results to a new file by appending `> dec_flag`  
   
<img width="640" height="173" alt="image" src="https://github.com/user-attachments/assets/64a4ea2c-ad13-4d19-af46-332942b89b07" />   
     
At first I didn't think my syntax worked, but looking closely reveals that the start of the encoded string changed from "Vm..." to "Vj...".    
    
So it looks like they encoded an already encoded string? That's odd. Let's throw this into CyberChef to quickly stack decodes on this problem.    
   
<img width="1660" height="634" alt="image" src="https://github.com/user-attachments/assets/1e8cc3ea-cc71-422d-b1fe-83f26ae8f464" />   

As a quick overview, CyberChef is a very popular GUI mathmatics/data analysis/encoding/decoding/... "swiss army knife" as they call it. You drag operations in the "baking" (cyberCHEF... get it?) section and they are enacted onto your supplied data. We can continue to stack these to take the output from one opertion and send it to the next decode operation.   
   
<img width="1395" height="630" alt="image" src="https://github.com/user-attachments/assets/bff2ec0f-4950-4976-8f47-b8172ba9d997" />   

Stacking three base64 decodes in a row shows what appears to be a string... but I know this is still just base64 data that doesn't have padding on it. Lets keep adding decodes until we get something else.   
   
<img width="1274" height="628" alt="image" src="https://github.com/user-attachments/assets/bebdfeb3-39a3-4752-8283-d7180716f8ac" />    

And just after six decodes strung together, we're presented the picoCTF flag!   

Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.
