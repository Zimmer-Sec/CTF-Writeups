## Name: Disk, disk, sleuth! II   //   Difficulty: Medium   //   Topic: Forensics
#### By: Kyle Zimmer


**Overview: This challenge helped to practice the basics of using a command-line disk analyzer. For this task we used [The Sleuth Kit (TSK)](https://wiki.sleuthkit.org/index.php?title=TSK_Tool_Overview) to sift through the different layers (media, block, inode, and filename) of file system structure to uncover a key file's location within many hidden files.**

<img width="866" height="486" alt="image" src="https://github.com/user-attachments/assets/e8baac6a-1d80-4d40-bb4f-5a2d67e1f4ac" />

After downloading the provided file, it was quickly obvious that it was compressed with the `gzip` utility. We can confirm this by running `file dds2-alpine.flag.img.gz`. The decompression utility counterpart for this scenario would be `gunzip dds2-alpine.flag.img.gz`. 

<img width="1353" height="171" alt="image" src="https://github.com/user-attachments/assets/750a38d5-cb88-47b4-afe4-f47fa3f968f8" />

Knowing that this file is now just a file system image, we can utilize a plethora of tools to begin analyzing it, but to start, we want to look at how the disk image is partitioned. To begin this process, I’ll turn to The Sleuth Kit’s media layer command tools. The command we’ll want to use is `mmls`, this command performs a listing (ls) of the media layer to give a high level overview of partitioning table using the `mmls` command.

<img width="642" height="176" alt="image" src="https://github.com/user-attachments/assets/0672864e-cb9f-4b44-965b-05bcdc58e4a2" />

From this output we can see that the image has one 2048-byte space of unallocated memory alongside a 260096-byte partition described as Linux (most likely an ext.) Using that starting index (offset) number of 0000002048 (or just 2048 for short), we can begin to look closer at that memory space’s file name layer, using `fls -o 2048 dds2-alpine.flag.img`

<img width="594" height="377" alt="image" src="https://github.com/user-attachments/assets/a45cbdec-af85-4881-817d-4b5e980905aa" />

This command provides us a clear overview of Linux file system. We can continue to use fls while indexing the disk image’s memory offset (2048) along with the listed directory’s inode number added to the end of the command line. Another note: the fls command has useful flags to help show hidden files. I demonstrate this by listing the files in the home folder, looking for user accounts.

<img width="682" height="84" alt="image" src="https://github.com/user-attachments/assets/ccafa00c-aef3-4f05-bf39-57382f9d9471" />

Knowing that this flag is called ‘down-at-the-bottom.txt’ I’m sure that we will have to do some digging to get to it: Thankfully, the fls command comes with a recursive search through directories (-r). Using this, I can just dump the whole file system's structure and pipe the output to grep to query for the file name we’re searching for.

<img width="739" height="399" alt="image" src="https://github.com/user-attachments/assets/3d4c362b-def2-477b-ab9a-31326d017189" />

The syntax `fls -r -a -o 2048 dds2-alpine.flag.img | grep down` does the functionality of iterating (-r) through all (-a) directory on the system while the pipe sends the output to grep to search for the keyword “down”. After discovering the file, I took the inode number (18291) for that file (r/r) and utilized the inode layer’s `icat` command to read the data spread across the block space, revealing the picoCTF{} flag.

Note: Don’t submit the flag that appeared on my screen. It is unique to my account and will cause your account to be flagged for cheating.
