# Identifying simple encryption algorithms and functions

In this section, we will take a look at the simple encryption algorithms that are widely used in the wild. We will learn about the difference be-tween symmetric and asymmetric encryption, and we will learn how to identify these encryption algorithms in the malware's disassembled code.

# Types of encryption algorithms

Encryption is the process of modifying data or information to make it un-readable or unusable without a secret key, which is only given to people who are expected to read the message. The difference between encoding or compression and encryption is that they do not use any key, and their main goal is not related to protecting the information or limiting access to it compared to encryption.

There are two basic types of encryption algorithms: symmetric and asym-metric (also called public-key algorithms). Let's explore the differences between them:

·Symmetric algorithms: These types of algorithms use the same key for encryption and decryption. They use a single secret key that's shared by both sides:

<!-- Plaintext: Protected data Encrypt Ciphertext: Dk6aj9jsk1nc ckwnsos8shs Plaintext: Protected data Decrypt  -->
![](https://web-api.textin.com/ocr_image/external/26815e42c37be5e5.jpg)

Figure 4.24-Symmetric algorithm explained

·Asymmetric algorithms: In this case, two keys are used. One is used for encryption and the other is used for decryption. These two keys are called the public key and the private key. One key is shared pub-licly (the public key),while the other one is kept secret (the private key).Here is a high-level diagram describing this process:

18500 04.xhtml# idParaDest-122 12:14 24/12/24

<!-- Plaintext: Protected data Encrypt private hay Ciphertext: Wc6aj9jrk1ni pfw8s1s8shm Plaintext: Protected data Decrypt public key  -->
![](https://web-api.textin.com/ocr_image/external/1553aa8bc8aef5fb.jpg)

Figure 4.25- Asymmetric algorithm explained

Now,let's talk about simple custom-made encryption algorithms com-monly used in malware.

## Basic encryption algorithms

Most encryption algorithms that are used by malware consist of basic mathematical and logical instructions-that is, xor, add, sub,rol,and ror.These instructions are reversible, and you don't lose data while en-crypting with them compared to instructions such as shl or shr,where it is possible to lose some bits from the left and right. This also happens with the and and or instructions, which can lead to data loss when using or with 1 or and with 0.

These operations can be used in multiple ways, as follows:

·Simple static encryption: Here,the malware just uses the aforemen-tioned operations to change the data using the same key. Here is an example of it that uses the rol instruction:

<!-- 31 0 0000 1000 1000 1000 0000 1000 1000 1010 1010 0000 1000 1000 1000 0000 1000 1000  -->
![](https://web-api.textin.com/ocr_image/external/84deb52e31bd1652.jpg)

Figure 4.26- Example of the rol instruction

·Running key encryption: Here, the malware changes the key during the encryption. Here is an example:

loop_start:

mov edx, &lt;secret_key&gt;

xor dword ptr$[<ata_to_encypt>+eax]$,edx

add edx, 0x05 ; add 5 to the key

inc eax

loop loop_start

·Substitutional key encryption: Malware can substitute bytes with each other or substitute each value with another value (for example,for each byte with a value of 0x45, the malware could change this val-ue to 0x23).

18500 04.xhtml# idParaDest-122 12:14 24/12/24

·Other encryption algorithms: Malware authors never run out of ideas when it comes to creating new algorithms that represent a combination of these arithmetic and logical instructions. This leads us to the next question: how can we identify encryption functions?

## Identifying encryption functions in disassembly

The following screenshot demonstrates sections that have been num-bered from 1 to 4.These sections are key to understanding and identify-ing the encryption algorithms that are used in malware:


| .text:100025E8 Loop: |  | ; CODE XREF: DecryptFunc+384j |
| -- | -- | -- |
| .text:100025E8 | movsx  | eax,byte ptr [edx+esi] ① |
| .text:100025EC | cmp  | eax,20h  |
| .text:100825EF | Jnz  | short 1oc_100025F7 |
| .text:100025F1.text:100025FS.text:100825F7 | mov jmp  | byte ptr [edxeesi],0 |
| .text:100025F1.text:100025FS.text:100825F7 | mov jmp  | short loc_10082605 |
| .text:100025F7 |  |  |
| .text:100025F710c_100025F7: |  | ;CODE XREF:DecryptFunc+1F1J |
| .text:100025F7 | sub  | eax,37h 2  |
| .text:100825FA | cmp  | eax,21h  |
| .text:100825FD | Jge  | short loc_10002602 |
| .text:100025FF.text:10082602.text:1008260210c_10002602:.text:10082602.text:10002605.text:100826851oc_10002605:.text:10002605 | add mov Snc  | eax,SEh  |
| .text:100025FF.text:10082602.text:1008260210c_10002602:.text:10082602.text:10002605.text:100826851oc_10002605:.text:10002605 | add mov Snc  |  |
| .text:100025FF.text:10082602.text:1008260210c_10002602:.text:10082602.text:10002605.text:100826851oc_10002605:.text:10002605 | add mov Snc  | ;CODE XREF:DecryptFunc+201j[edx+esi],al 3 ; CODE XREF: DecryptFunc+251j |
| .text:100025FF.text:10082602.text:1008260210c_10002602:.text:10082602.text:10002605.text:100826851oc_10002605:.text:10002605 | add mov Snc  | edx  |
| .text:10002686.text:10082688.text:1000260A | cmp 31  | edx,ecx 4 short Loop  |


Figure 4.27 - Things to pay attention to when identifying the en-cryption algorithm

To identify an encryption function, there are four things you should be searching for, as shown in the following table:


| Sequential data read  | The encryption function must read a block of data from memory-not a fixed value,but an array of bytes,one by one.Therefore,the address from where malware reads the data should change over time.  |
| -- | -- |
| Encrypting the value  | It may sound obvious, but not all the loops with sequential read and write are related to encryption; it may be used just to move the data around.  |
| Seqential data write  | Same as with data read, the address where the data is written should be changing over time.If the function is writing the result to a fixed address,it may just be generating a checksum of this data to check its integrity (this is commonly used to check for INT3 breakpoints).  |
| Loop  | It's important to note that the variable that is used as a loop index is, in most cases,the same one that is used for the sequential read and write operations.It will be changing (usually incrementing) on every iteration.  |


These four points are the core parts of any encryption loop. They can eas-ily be sptted in a small encryption loop but may be harder to spot in a more complicated encryption loop such as RC4 encryption, which we will discuss later.

## String search detection techniques for simple algorithms

In this section, we will be looking into a technique called X-RAYING (first introduced by Petr Ferrie in the PRINCIPLES AND PRACTISE OF X-RAY-ING article in VB2004). This technique is used by antivirus products and other static signature tools to detect samples with signatures,even if they

vsis/9781803240244/B18500 04.xhtml# idParaDest-122 12:14 24/12/24



