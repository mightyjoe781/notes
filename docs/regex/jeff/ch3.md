## Overview of Regular Expression Features and Flavors

when looking at regex in context of host language or tool there are 3 broad issues

- what metacharacters are supported, and their meaning. Often called the regex “flavour”
- how regular expressions “interface” with language or tool
- how regular expression engine actually goes about applying regular expression to some text.

### History of Regular Expressions

#### The Origins

- first described by 1940 by two neuro-physiologists, Warren McCulloch and Walter Pitts, who developed models of how they believed the nervous system worked at the neuron level. Later few years down the road mathematician Stephen Kleene formally described these models in an algebra he called regular sets. He devised a simple notation to express these regular sets, and called them *regular expression*.
- The first computaional use of regex we could find is Ken Thompson’s 1968 article Regular Expression Search Algorithm in which he describes a regular expression compiler that produced IBM 7094 object code. This let to his work on *qed*, an editor formed basis for Unix editor *ed*
- ed was the editor that made use of regular expression widespread.

##### Grep’s metcharacters

- only `*` was supported early on along with line anchors. Altercation or `+` or `?` was not supported at that time.
- later (30 yrs from now) grep evolved and got new features at Bell Labs adding new features like `\{min,max}` syntax and many basic functionality we take granted for.

##### Egrep evolves

- Alfred Aho (also at AT&T Bell Labs) had written egrep, which provided most of the richer set of metacharacters, More importantly he implemented them in a completely different way (better). Not only `+` and `?` added, but could be applied to parenthesized expressions, later altercation was also implemented.

##### Other species evolve

- at the same time, programs like `awk, lex` and `sed` evolved and started growing at their pace.

##### POSIX-An attempt at standardization

- POSIX distills the flavors into BREs (Basic) and ERE(Extended).
- One important feature of POSIX standard is the notion of a *locale*. locale aims to allow programs to be internationalised. They are not a regex-specific concept, although can affect regex.

##### Henry Spencer’s regex package

- appeared in 1986 completely written in C, which could be freely incorportated by other into their own programs.

##### Perl evolves

- Larry wall started developing a tool that would later become the language Perl, he already greatly enhaced distributed software development with his *patch* program.
- Larry released its version 1 in Dec 1987. Perl was immediate hit because it blended so many useful features of other languages.
- Perl2 releases 1988, Larry replaces regex code entirely using enhance version of Henry Spencers package.
- later on more features added to perl, and advanced were perfectly timed for the WWW revolution. Perl was built for text processing, and the building of web pages is just that, so Perl quickly become language of web development.

### Care and Handling of Regular Expressions

In general, a programming language can take one of three approaches to regex.

#### Integrated Handling

- Example perl’s approach `$line =~ m/regex/modifier`, $line stores the text and if match is found some code is executed and if used in a conditionals references are passed as `$1,2`. 
- What goes on behind is quite difficult to grasp here.

#### Procedural and Object-Oriented Handling

- normal functions are provided by procedures or methods rather that some internal built in operators

##### Java

````java
import java.util.regex.*;
Pattern r = Pattern.compile("^Subject: (.*)", Pattern.CASE_INSENSITIVE);
Matcher m = r.matcher(line);
if (m.find()) {
  subject = m.group(1);
}
````

- Java does provide procedural approach too, using Pattern.matches(...)
- Sun has occasionally integrated regular expressions into other parts of language like `if(! line.matches("\\s*")){}` (test for blank lines :P)

##### PHP

````php
if (preg_match('/^Subject: (.*)/i', $line, $matches))
  $Subject = $matches[1];
````

##### Python

````python
import re;

R = re.compile("^Subject: (.*)", re.IGNORECASE);
M = R.search(line)
if M:
  subject = M.group(1)
````

