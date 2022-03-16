### Routing browsing through a `squid` proxy

If you wish,  you  can use your Debian server  to change your apparent country in web browsers.

One  reason to do  this would be to access content  that is restricted based on location. This will  only work,  though,  if your server's IP address  is  located in a country or region  for which  such access is permitted.

To do this, proceed as follows:

a. Determine  the  IPV4 address of the connection  that  you'd like to relocate.  One way to  do this is to go to Google  and enter  "What is my IP address?"  Another way is  to visit the following website.  Note that the URL in question uses "http" and not "https":

    http://showip.net/

b. Execute:

    sudo apt-get install squid

c. Edit the text file "/etc/squid.conf". Find this part:

    #Default:
    # forwarded_for on

Add the following setting right after that:

    forwarded_for delete

Find this part:

    #Default:
    # Deny, unless rules exist in squid.conf.

Add the following part right after that:

    acl moocow src 111.222.333.444
    http_access allow moocow

Replace 111.222.333.444 with the IPV4 address that you identified previously.

Note: You should see the following right after the new lines:

    # Recommended minimum Access Permission configuration:
    #
    # Deny requests to certain unsafe ports
    http_access deny !Safe_ports

d. sudo service squid restart

Allow 5 minutes for the preceding command to complete.

e. Install a proxy management add-on in your web browser.  Or, in some browsers, you may be able to edit network settings directly. In either case, set up your connection, or a proxy profile, as follows:

    Proxy host: 123.456.123.456
    Proxy port: 3128
    Use this proxy for all protocols
    No Proxy For: localhost; 127.0.0.1

Replace 123.456.123.456 with the IPV4 or hostname for your box.

If the last 2 settings aren't offered, proceed without them.

f. Clear your browser cache,  restart your browser,  and check the ap-
parent IPV4 address.

g. If your  client-side  IPV4  address changes,  you'll need to update "squid.conf" accordingly. Subsequently, execute:

    sudo service squid restart

Note, again, that this may take up to 5 minutes.

h. "squid"  offers  multiple benefits in addition  to location change. It's advised that you read about the program.

i. Never run "squid" without the edits discussed above.  If you do so, 100s of people  will flood in to use your proxy and you'll be held responsible for whatever they do.