## 9. Securing your System

Securing your system means ensuring that your computer’s resources are used only by authorized people for authorized purposes. Even if you have no important data on system, you still have valuable CPU time, memory, and bandwidth.

Many folks who think their systems were too unimportant for anyone to bother breaking into found themselves an unwitting relay for an attack that disabled a major corporation. See Botnets.

Generally, OS are not broken into; the program running on OS are. Even the most paranoiac, secure-by-default OS in the world can’t protect badly written programs from themselves. Occasionally, one of those program can interact with OS in a way as to actually compromise OS. The most well-know of these are *buffer overflows*, where an intruder’s program is dumped straight into CPU’s execution space and the OS runs it. FreeBSD has undergone extensive auditing to eliminate buffer overflows as wells as myraid other well-understood security issues, but that’s no guarantee that they have been eradicated.

FreeBSD provides many tools to help secure your system against attacker, both internal and external. While no one of these tools are sufficient, all are desirable. Treat everything you learn about system security as a tool in a kit, not as the answer to all your problems.

### Who is the Enemy ?

#### Script Kiddies

Script Kiddies are not sysadmins and they are not skilled. They download attack points and work on a point-and-click basis and go look for vulnerability. To defend against : just keep your software up-to-date and follow good computing practices.

#### Disaffected Users

A organization’s employees are people most likely to know where the security gaps are, to feel that the rules don’t apply to them, and to have the time to spend breaking your security. You might have all patched and downright misanthropic firewall installed, but if anyone who knows the password is *Current93* can dial the back rook modem, you’re in trouble.

To stop people like these is simply not to be sloppy. Don’t leave projects insecurely half-finished or half-documented. When someone leaves the company, disable his account, change all administrative passwords, inform all employees of that person’s departure, and remind them not to share confidential information with that person. 

#### Botnets

Botnets are more numerous than either of the above. They are machines compromised by malware and controlled from a central point. Botnets can include millions of machines. The malware authors control the botnets and use them for anything from searching for more vulnerable hosts to sending spam or breaking into secure sites. Most botnets are composed of Windows and Linux Machines, But there is no reason why FreeBSD OS can’t be assimilated into botnets.

Fortunately, botnet defense is much like script kiddie defense; keeping your software patched and following good computing practices goes a long way.

#### Motivated Skilled Attackers

The most dangerous group - skilled attackers are competent system admins, security researchers, penetration specialists, and criminals who want access to your specific resources. Computer penetration is a lucrative criminal field these days, especially if the victim has resources that can be used for DDOS attacks or mass spam transmission. If one of these people *really* wants to break into your network, he’ll probably get there.

If you can make the intruder’s break-in plan resemble a Hollywood script no matter how much he knows about your network, your security is probably pretty good.

### FreeBSD Security Announcements

The FreeBSD Project includes volunteers who specialize in auditing source code and watching for security issues with both the base operating system and add-on software. These developers maintain a very low-volume mailing list, FreeBSD-security-notifications@FreeBSD.org, and subscribing is a good idea. While you can monitor other mailing lists for general announcements, the security notifications list is a single source forFreeBSD-specific information. To subscribe to the security notifications mailing list, see the instructions on http://lists.freebsd.org/. The FreeBSD security team releases advisories on that mailing list as soon as they’re available.

### User Security

FreeBSD has a variety of ways to allow users to do their work without giving them free rein on the system.

#### Creating User Accounts

FreeBSD uses standard UNIX user management programs such as `passwd(1)`, `pw(8)`, and `vipw(8)`. FreeBSD also includes a friendly interactive user-adding program, `adduser(8)`. Only *root* may add users, of course.

![image-20220329002843030](ch9.assets/image-20220329002843030.png)

The username is the name of account. FreeBSD lets you choose a numerical user ID (UID). FreeBSD starts numbering UIDs at 1,000; while you can change this, all UIDs below 1000 are reserved for system use. Just press enter to take next available UID.

![image-20220329003048086](ch9.assets/image-20220329003048086.png)

The user’s default group is important. The FreeBSD default of having each user in their own group is usually the sensible way for most setups. Any of big thick books on system administration offers several grouping schemes.

A login class specifies what level of resource the user has access to.

The *shell* is command line environment. While system default is /bin/sh, I prefer tcsh.

The home directory is where the user’s files reside on disk. The user and the user’s primary group own this directory. You can set custom permissions on the directory if you want, probably so that other users can’t view this user’s directory.

#### Configuring Adduser : /etc/adduser.conf

Creating new users on some Unix systems requires you to manually edit `/etc/passwd`, rebuild the password database, edit `/etc/group`, create a home directory, set permission on that directory, install dotfiles, and so on.

`/etc/adduser.conf` lets you set requirements as defaults while retaining the high degree of automation. To create `adduser.conf`, run `adduser -c` and answer the questions.

#### Editing Users

FreeBSd includes several tools for editing accounts, the simplest are `passwd(1)`, `chpass(1)`, `vipw(8)`, and `pw(8)`. These work on tightly interrelated files `/etc/master.passwd`, `/etc/passwd`, `/etc/spwd.db` and `/etc/pwd.db`.

`/etc/master.passwd` is authoritative source of user account information and includes user passwords in encrypted form.

Any time any standard user management program changes the account information in `/etc/master.passwd`, FreeBSD runs `pwd_mkdb(8)` to update other three files.

**Changing a Password**

Use `passwd(1)` to change passwords.

![image-20220329004438328](ch9.assets/image-20220329004438328.png)

**Changing Accoutns with chpass(1)**

if you use `chpass`, you will get an editro with following text : 

![image-20220329004548626](ch9.assets/image-20220329004548626.png)

If you use `chpass <username>` as root you will get even more options to modify.

**The Big Hammer : vipw(8)**

`vpiw` helps edit multiple user at a time. A FreeBSD system considers `/etc/master.passwd` in case of conflicts with other password files.

Each line in `/etc/master.passwd` is a single account record containing 10 colon-sepearated fields. These fields are the following : 

Username;Encrypted Password, UserID, Group ID, User’s Class, Password Expiration; Account Expiration; Personal Data; User’ Home Directory; User’s Shell.

**Removing a User**

The `rmuser(8)` program deletes user accounts.

**Scripting with `pw(8)`**

Very useful command to lock users and while account is locked, account is active, nobody can log in to it.

`pw lock xistence`

`pw unlock xistence`

### Shells and /etc/shells

The *shell* is the program that provides the user’s command prompt. The file `/etc/shells` contains a list of all legitimate user shells. If you compile your own shell without using a FreeBSD port, you must list the shsell by its complete path in `/etc/shells`.

The FTP daemon won’t allow a user to login via FTP if his shell isn’t listed in `/etc/shells`

### root, Groups, an Management

