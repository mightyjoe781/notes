### A talk with OldCoder aka Robert Kiraly

#### Study: What should a Linux FOSS developer learn?

Q. Suppose that  somebody is interested in Linux FOSS development  for startup  or employment purposes.  Or just to be able to create or participate in FOSS projects.  What should a related course of study  include?

A. I'll assume that this is  about  building a broad foundation as opposed to a focus on a specialty.

The answers are:

-   Code Languages
-   Data Languages
-   Source Code Management
-   Build Systems
-   Standard Servers
-   Containers and Virtual Machines

These topics are discussed in the following sections.

#### Code Languages

This is a summary of my own languages experience from 2012:

> Perl, Python, PHP. Standard but
> you 'C', I also Lisp
> FORTRAN rocks and TeX rolls
> It's fun to assemble
>
> JavaScript, Forth, Pascal, Bash
> Bash is a smash
> People should not trash
> Bash is a smash
>
> Tcl/Tk: people disrespect it a bit
> but with me it's a hit
> Java is not JavaScript
> Lua how'ja Dua
>
> Octave and Matlab not the same
> Close enough there's no shame
> SQL What the Hell
> Several versions

I'd recommend the following to new developers in 2021:

Learn 'C' (not C++), Perl 5, Python 3, PHP 7 and 8,  JavaScript  (both traditional and "node.js"), Lua and Tcl (they might go well together), and Bash. Later on, Go (Google's replacement for C++).

Java is a good teaching language. I'm referring to Java, the pure language,  as opposed to JNI.  Java is the modern Pascal.  It's so strict that, if a student is able to get a program to  build,  it's likely to run.

I don't  recommend  focusing on Java or going  too deep into the  Java ecosystem.

The Java ecosystem is like the  MS-Windows world:  It's a foreign city actually,  a city on another planet -- where everything down to the plumbing is different.  You'd visit the city and learn the new culture and  myriad different ways of doing things only if you planned to live there.

Learn  enough C++ to  be able to patch C++ programs based on 'C' knowledge.

Avoid Rust and Ruby.  Reasons for dislike of C++, Rust, and Ruby are a separate discussion.

If  you work at a Windows house,  you'll want to  pick up both DOS CLI and PowerShell.

If possible,  avoid the major  MS languages and frameworks  such as C# and .NET. The reason is the same as discussed above in connection with Java.

At some Windows houses,  you'll be able to work in Linux-like environments and use "gcc", Perl, and other FOSS languages much as though you were using Linux.

#### Data Languages

Be familiar with SQL, JSON, YAML, and XML.  Plus HTML 5 and CSS 3  for webdev. Note that HTML 5 is a type of XML.  Learn  enough  CSS 3  that you're able to write responsive web pages.

You should be familiar with CSV  but that one is really just a trivial format.

#### Source Code Management

Learn "git".  There are  other systems of this type,  but "git" is the one to start with.

#### Build Systems

You  don't need to  learn to work  *in* a  build system;  i.e., how to write build scripts.  However, you do need to learn how to use them to build programs.

The two most  important build systems are  "autotools"  (also known as "autohell") and "meson-ninja".  "cmake" is a candidate for  3rd place.

"autotools" was  dominant for years.  It  was,  and remains, horrible. Different releases are incompatible.  A tool  that's designed  to help with this (autoupdate) doesn't work.  The system as a whole is as slow as molasses  and often breaks for reasons that  are difficult to debug and fix.

In response to this,  "meson" and "ninja" have arisen.  This is a pair of programs  that  work together  to build programs  quickly and efficiently.

"cmake"  was an earlier attempt  to escape  the  horror that is "auto-tools".  I don't like "cmake"  because it's often  unable to find libraries and what to do about this isn't clear.

We'll discuss the three systems in greater detail further down.

#### Standard Servers

1. A developer should have a fair understanding of what DNS is and how
   it works. For basic development boxes,  "dnsmasq" is the recommended DNS server.
   Setup instructions are provided elsewhere in this document. For more advanced use cases, it may be  necessary  to set  up "named". "named" is beyond the scope of this discussion.

2. It's also important to be familiar with web server setup. 

   A web server is, of course, any server that supports the "http" and/or "https" protocols. There are many such servers. The ability to do this is, for example, a standard part of most Perl, Python, and PHP installations.

   The two most important web server programs -- i.e., programs dedicated to the purpose -- are "nginx" (aka Engine X) and Apache 2.

   Apache 2 isn't  bad.  However, it's complicated and resource-intensive compared to "nginx".  The recommendation is  to use "nginx" instead of Apache 2 where possible. 

   In some cases,  FOSS software packages require Apache 2.  It should be possible, in a subset of the cases,  to run "nginx" as the primary web server and to relay  requests for Apache 2 pages to a copy of Apache 2 running behind the scenes.

3. FWIW: As of 2021,  "nginx" and Apache 2 are basically tied in terms of market share.

4. "nginx's" features include:

    * Uses much less RAM than Apache 2
    * Much faster than Apache 2
    * Reverse proxy with caching
    * Mail proxy (supports TLS, SMTP, POP3, and IMAP)
    * IPV6
    * Load balancing

5. A third FOSS  web server  that is  worth mentioning is  "lighttpd".
  "lighttpd" is also known as "Lighty"  (a name that is certainly easier
  to pronounce).

  "Lighty's" claims to fame are as follows:

- It's both  venerable and maintained.  The program  dates back to
    2003 but a new release was made in 2021.
* It's lightweight and quite fast.

  "nginx" is  recommended for general use cases,  but "Lighty" is useful
  for some purposes.

6. A Linux FOSS developer should know how to configure SSH both on the
  client side and on the server side.

  There are two major SSH server programs: OpenSSH and Dropbear. OpenSSH setup is discussed elsewhere in this document.  Dropbear notes will be added.

  On the client side, the primary SSH configuration file is "$HOME/.ssh/config". Notes related to that file will be added.

7. An understanding of SSH key pairs is advisable. A few notes related
to key pairs are included elsewhere in this document.

#### Virtual Machines

In the modern FOSS world,  an understanding of  containers and virtual machines is a must.

A virtual machine (or VM) is simply a PC or other computer that  isn't real. I.e, it isn't hardware by itself. It consists partly or entirely of software.

In the classical form,  a virtual machine is a program that interprets machine instructions and  thereby fools  an application into believing that it's running on a compatible machine. The machine doesn't actually exist.

The game device emulators that  started to appear in the 1990s -- MAME is an important example -- were of this type.

It can be more complicated these days.  In some cases, a virtual machine may have access to the underlying real machine's hardware. The access is, however, controlled.

A "VPS" is simply a  virtual machine that is rented out,  usually on a monthly or annual basis.  Typically, it offers WAN access and a static WAN IPV4. So, it's useful for server hosting purposes.

#### Containers

Virtual machines  require lots of resources to run.  Containers  are a lightweight alternative.

A container looks, to some extent, like a virtual machine.  It has its own operating system and filesystem.  So,  for example, you can have a Debian PC and boot a container on the  PC that runs  Fedora instead of Debian.

Terminology: The OS that runs a virtual machine or container is referred to as the "host OS" or simply as the "host". The OS that runs on a virtual machine  or in a container is referred to as the "guest OS" or simply as the "guest".

Containers are more limited than virtual machines in two key respects: (a) There is no virtual hardware. (b) The same kernel needs to be used by the host OS and the guest OS.

So, a guest running on a Linux host must run Linux and the two Linuxes must be the same in terms of kernel and machine type.

The trade-off is that containers are essentially zero cost in terms of resources -- i.e., disk space, RAM, and CPU -- except for  the resources that a guest OS  actually uses. No machine per se is emulated,  so there is no cost for that.

Additionally,  containers don't need to emulate entire OSes.  They can be set up so as  to perform specific tasks such as running one type of server.

##### Container Software

Important container tools include "docker", "lxd", "podman", and "kubernetes".

You probably wouldn't  seek to learn  "kubernetes" without a reason to do so. It's powerful but complicated.

"docker" was a must-know for a few years. However, there's an alternative named "podman" now that may be a better option.  "podman" is discussed elsewhere in this document.

"lxd" is  useful but not a must-know presently for the generalist developer.

#### VM Software

The most important  FOSS virtual machine systems are QEMU and Virtual Box OSE.

QEMU is the one to focus on.

VirtualBox OSE has a polished and friendly GUI.  However, it's part of a commercial  package and  license issues are  a problem  in some contexts.

Additionally, VirtualBox OSE is highly fragile, it requires Qt5 (which is problematic in multiple respects),  and it can be nearly impossible to build.

QEMU is very simple to use for simple use cases.  It also doesn't have as many license issues.

For more  advanced use cases -- for example, those involving complicated network setups -- QEMU commands can  require some effort to figure out.

You'll want to learn to use a system called SPICE with QEMU.  SPICE is needed to get "copy and paste" working between host and guest.  It implements other features as well.

Some  developers use a framework named "libvirt" to set up QEMU operations. I prefer direct control of things and to avoid extra  layers of machinery where possible.  So, QEMU commands  can be complicated but I prefer  to write  them than  to deal with  the machinery introduced by "libvirt".

There's a tool named "vagrant" that is sometimes used to manage remote VMs from the command line.  I like  "vagrant"  but  it's difficult  to build, so I've dropped it.

#### CMS Recommendations

Drupal: Not advised for individuals or small organizations.

Drupal could be thought of as a powerful analogue to WordPress. It has impressive features and  is  a respected CMS.  However,  it's huge and complicated.  A  startup or small business that uses Drupal might find itself trapped in technical debt.

Joomla: Not advised for individuals or small organizations.

Joomla is a competitor to Drupal.  It offers  similar advantages relative to WordPress.  I don't see a clear winner between Joomla and Drupal. Some  reviewers feel that Joomla is more polished, but Drupal may offer features to balance this.

WordPress:  WordPress is O.K. for non-tech would-be CEOs. It isn't for developers who'd like to do things quickly and efficiently. Especially not CLI developers.

Don't deprecate WordPress.  It fills a niche and does it well. A large part of the Web  is  on WordPress.  However,  it's bulky,  awkward and clumsy to  work with.  Additionally, the resulting websites are slower than what you get with lightweight approaches.

This said, for a small startup or business, WordPress is probably preferable to Drupal or Joomla.

Jekyll:  You  can  use  Jekyll "to host [static] sites right from your GitHub repositories".  That's a nice feature.  However, there are some negatives:

* It's written in, and requires, Ruby. That isn't a plus.

* Its use  case  is,  to  some  extent,  integration with Github (even
though Github isn't required).

* It involves more of an ecosystem than I like to see for this type of
application.  I prefer software that doesn't require  as  much commit-
ment.

* It's slow for large sites.

Hugo: Hugo offers a number of pluses:

* It's 35 times faster than Jekyll. Repeat, 35 times.

* Hugo is a compiled Go application -- hence the name Hugo -- and this
means  both  speed  and  fewer  problems  related  to fiddling with an
interpreter.

* Hugo is easier to set up than Jekyll is.

* It supports more data languages than Jekyll does.

* Like Jekyll, files are stored as text as opposed to database.

* Like Jekyll, a development server is provided.

* Hugo can generate and/or post-process CSS and JS code.

* It supports menus, XML sitemaps, and RSS/ATOM feeds.

* It can import Jekyll sites.

Hugo is obviously a winner in this space. There are only two arguments
against it that I can see:

* It's for static sites only as opposed to dynamic sites.

* I prefer  something  simpler for basic use cases.  This brings us to the final options below.

Lightweight tools: I prefer lightweight site-creation tools.

I use both  (a) my own site language translator,  "Haggis",  and (b) a markdown to  HTML translator that I've started  to write.  Haggis supports dynamic pages. The MD to HTML translator is static-only but very easy to use.

There are publicly released FOSS projects in the same space. For example, review Pico:

      https://picocms.org/

Pico supports static sites out of the box.  Additionally, if you don't mind learning a related  framework named  "Twig",  you can add dynamic content.

For basic use cases, these tools are good because  they're simple  and easy  to  use,  they don't require a commitment  to an ecosystem,  and they're often easy to tweak.

Four recommendations:

* Try Pico for static sites and sites that need a small amount of dyn-
amic content.

* Try Hugo for static sites that need more "oomph".

* For sites that are primarily  dynamic in nature,  it might be better
to skip CMS and  work in one of the following: Perl 5, Python 3, PHP 7
or 8, or "node.js".

* If you  need a dynamic site quickly and  a matching template site in
your preferred language isn't available,  WordPress is acceptable as a
fallback option.

#### Use of `autohell`

The sources  for an "autohell"-based FOSS program may include a "configure"  script written in Bash.  To use such a script, one typically executes it as follows:

    mkdir -p /opt/moocow
    bash ./configure \
        --prefix=/opt/moocow           \
        --disable-dependency-tracking  \
        --enable-shared=yes            \
        --enable-static=no

This procedure,  ideally,  creates  a "Makefile" which  can be used to build and  install the program.  Additional option switches may or may not be required.

The sources  may include a "configure.ac" file instead of "configure". In this case, one must use "configure.ac" to create "configure",  then use "configure" to create "Makefile".

The  procedure  used to go from  "configure.ac" to "configure"  varies from program to program. Sometimes, the following command will work:

    autoreconf -fi

Scripts with names such as "autogen", "autogen.sh", or "bootstrap" may be  provided.  These  scripts  typically  will create  "configure" for you.

In some cases, these  scripts may run "configure" automatically  after "configure" is created. In the latter case, the developer must provide the required "configure" switches to these scripts instead of to "configure".

If  a FOSS project is old,  its existing  "configure"  script  may not work.  In such cases,  one hopes that "configure.ac"  is also provided and  uses "configure.ac" to rebuild "configure".  That procedure often fails with obscure error messages.

With luck, "autotools" will disappear soon. It won't be missed.

#### Use of `meson-ninja`

"meson-ninja" projects  are easy to build  except for  one tricky part that we'll come back to. One proceeds as follows:

a. Python 3 is required and must be accessible by PATH.

b. Install dependencies.

c. Go to the appropriate source directory.  This is the directory that contains "meson.build". Execute a script similar to the following:

    mkdir -p /opt/moocow
    rm -fr build
    mkdir  build
    meson  build -D prefix=/opt/moocow
    
    cd build
    if [ \! -f build.ninja ]; then exit 1; fi
    meson configure
    ninja || ninja
    ninja install

That's it, in many cases, except for the tricky part mentioned before. You may need to add more option switches to the "meson build" command. The tricky part  is  determining  the  format  of the option switches.
Sometimes, you'll need to specify "true" or "false" to enable or disable a feature. Other times, you'll need to specify "enabled" or "disabled" instead.

To  find out the  option switches that are supported  for a particular program and whether to use "true-false" or "enabled-disabled" instead, look  for a file named "meson_options.txt" and  review the contents of that file.

Some examples:

* This is my "meson build" command for "tracker-sparql"

    ````bash
    meson build \
        -D prefix=/opt/moocow \
        -D network_manager=disabled
    ````

* A build of "libvirt" is more complicated:

    ````bash
    meson build \
        -D prefix=/opt/moocow   \
        -D docs=enabled         \
        -D driver_qemu=enabled  \
        -D fuse=enabled         \
        -D libnl=enabled        \
        -D libpcap=enabled      \
        -D no_git=true
    ````

`meson-ninja` problem : 

There is one problem with  "meson-ninja" that makes it impossible to use for some purposes: The "meson-ninja" developers  chose  to  make the build system strip one type of information, "rpath", from executables at "install" time. This was insanity. However, the following simple patch to "meson" fixes the problem:

````python
--- meson-0.57.0.old/mesonbuild/minstall.py
+++ meson-0.57.0/mesonbuild/minstall.py
@@ -319,7 +319,8 @@
 
     def fix_rpath(self, *args: T.Any, **kwargs: T.Any) -> None:
         if not self.dry_run:
-            depfixer.fix_rpath(*args, **kwargs)
+            # depfixer.fix_rpath (*args, **kwargs)
+            print ("meson: rpath changes at install time disabled")
 
     def set_chown(self, *args: T.Any, **kwargs: T.Any) -> None:
         if not self.dry_run:
````

#### Use of `cmake`

"cmake" is used as follows:

a. "cmake" must be accessible by PATH.

b. Install dependencies.

c. Go to the appropriate source directory.  This is highest-level directory that contains a "CMakeLists.txt" file. Execute a script similar to the following:

````bash
mkdir build
cd    build
cmake \
    -DCMAKE_BUILD_TYPE=RELEASE          \
    -DCMAKE_INSTALL_PREFIX=/opt/moocow  \
    -DCMAKE_INSTALL_LIBDIR=lib          \
    ..
make && make install
````

This is obviously simple.  The problem is that,  if a  problem such as not being able to find a library occurs, it may be difficult to figure out and fix.