### Install CPAN modules using `cpanm`

If  the  new box is going to be used for Perl development,  you should
install a set of CPAN modules. There are two ways to do this:

​	(a) Install them from the distro repos

​	(b) Build   them from source

(a) is faster and  more reliable.  However, the distro repos don't in-
clude a full set of modules.  Additionally, repo copies of modules may
be outdated.

We may  document (a) at a later date.  This  revision of this document
discusses (b).

Advisories:

​	(c) This procedure may take up to an hour or longer
​	(d) Some builds may fail. See below for a work-around.

If a build of a given module fails due to a  test failure,  one  work-
around  is to disable testing for that module.  To do that,  replace a
command of the form:

      cpanm Foo::Bar
with:
      `cpanm --notest Foo::Bar`

If builds fail for other reasons, consult a developer.

To proceed:

      bash -e /root/setupdoc/files/addcpan.sh

Note that:

  (a) This must be done as "root"
  (b) Internet access is required
  (c) The work-around discussed above may be required

#### CPAN documentation

To  see what a given CPAN module does,  execute the command  "perldoc"
followed by a space and the module name. For example:

    perldoc Algorithm::FastPermute

#### CPAN Examples

##### CPAN example:  Print a sorted list of all  unique permutations of an array. Skip redundant lines.

````perl
use strict   ;
use Carp     ;
use warnings ;

use Algorithm::FastPermute ('permute');

my @array = qw (dog cat woof meow woof cow milk);
my %list  = ();
permute { $list {"@array\n"} = 1; } @array;
for (sort keys %list) { print; }
````

##### CPAN example: Download a file from the Web and store it locally.

````perl
use strict   ;
use Carp     ;
use warnings ;

use LWP::Simple;

die "Error: Download failed\n"
    unless getstore ("https://google.com/", "/tmp/google.html");
print "File downloaded\n";
````



##### CPAN example: Compute and display an MD5 sum.  The output is consistent with that produced by "md5sum -b".

````perl
use strict   ;
use Carp     ;
use warnings ;

use Digest::MD5 qw (md5_hex);

my $data   = "moo\n";
my $md5sum = md5_hex ($data)  ;
print "MD5 sum is: $md5sum\n" ;
````

