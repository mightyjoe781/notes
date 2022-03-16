### Mypaste : sortable download links

This step is  for developers and is optional.  It  requires  a working
"nginx" website with PHP 7 support.  "Apache" isn't presently support-
ed for this purpose.

The following tarball  contains a directory tree that includes an "in-
dex.php" file in the top-level directory:

    /root/setupfiles/mypaste.tgz

Unpack the tarball somewhere in the website  directory tree.  Then add
files  (any that you'd like to distribute) to the  top-level directory
of the tree that you just unpacked.

If  the new tree is  accessed via the  Web,  "index.php" will  display
download links for the files that you add.

"sortable"  means that  the list of download links can be sorted based
on  any of  several  attribute columns  (filename,  modification date,
etc.).

Subdirectories are supported.

For credits,  license information, and other details, see the code and
comments in the "index.php" file.

You may or may not wish to "chown" the directory tree as follows (mod-
ify the path shown here appropriately):

    chown -R www-data.www-data /var/www/mypaste/

If  you'd like to  use this feature to  distribute files both publicly
and privately, use two separate copies of the directory tree,  one for
public files and one for private files.