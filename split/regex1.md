# Regex Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: regex
This is part 1 of 1 parts

---

## File: regex/index.md

# Regular Expressions



## Mastering Regular Expressions Notes

- [Chapter 1: Introduction to Regular Expression](jeff/ch1.md)
- [Chapter 2: Extended Introductory Examples](jeff/ch2.md)
- [Chapter 3: Overview of Regular Expression Features and Flavors](jeff/ch3.md)
- [Chapter 5: Practical Regex Techniques](jeff/ch5.md)

---

## File: regex/jeff/ch1.md

## Introduction to Regular Expression

- You are tasked with checking all pages of a web server for double words !
  - accept any number of files, report each line of each file that has doubled words, results nicely formatted
  - word of the end of a line is repeated at the beginning of next line
  - ignore Capitalization
  - find doubled words even when separated by HTML tags.
- Above tasks could be done using Regular Expression with some effort but significantly less than traditional solutions

*Regular Expressions are key to powerful, flexible, and efficient text processing.* Regular expressions allow you to describe and parse text. With additional support by tools being used, regular expression can add, remove, isolate, and generally fold, spindle and mutilate all kinds of text and data.

#### Solving Real Problems

- to check a lot of files (70 per say) for whether each file container `SetSize` exactly as often as it contained `ResetSize`. To complicate matters consider capitalization optional.
- find pair of send and recieve emails from few hundred of emails without actually digging thru content :P

#### Regular Expressions as a Language

full regular expression are composed of two types of characters

- MetaCharacters (`* ? +`)
- Literal (e.g. Normal text character)

#### Regular Expression Frame of Mind

- **Searching Text Files: Egrep**

Solving Email problem :

```bash
egrep '^(From|Subject):' mailbox-file
```

Above Regex matches all the mails for words that start with word `From:` or `Subject:`. Here metacharacters are `^ ( ) |`.

Simple example finding word `cat` will match all words which are `cat` or `vacation` without regard of word boundary.

#### Metacharacters

**Typographical Conventions**

- `^` : (caret) represents start of a line
- `$` : (dollar) represents end of a line

**Character Classes**

- Matching any one of several characters
- Example lets say you want to match all words for ‘grey’ but you want to make sure if it were spelled ‘gray’ too. A simple regex like this can be used to define character class:  `gr[ea]y`
- Within character classes `-` represents range of characters : for detecting header tags : `<H[1-6]>` or several combination are `[0-9]` or `[a-z]`
- We can define multiple ranges : `0123456789abcd...` rather `[0-9a-fA-F]` 

NOTE : `-` is metacharacter only when used in character classes otherwise its a normal dash character.

**Negated Character Classes**

- Using `[^...]` negates the range defined in the character class meaning all charcters except specified.

**Matching Any Characters with Dot**

- `.` : match any character. Example find the dates that could be defined as dd/mm/yy or dd-mm-yy or some other format use this character to find dates : `13.11.2001`

**Alternation**

- `|` : (or) : For example to search for Jeffrey or Jeffery we can use either of these three
  - `Jeffrey|Jeffery`
  - `Jeff(rey|ery)`
  - `Jeff(re|er)y`
- NOTE: Character Class only matches one character while this can take in as many as characters. So `Jeff[re][re]y` might seem correct but it is not :P it matches `Jeffrry or Jeffeey` too.

**Ignoring Differences in Capitalization**

- One approach is to `[Jj]` for each capitalization or use `egrep -i` which ignores case

**Word Boundaries**

- to match word boundries we can `\< or \>` : for our cat example : `\<cat\>` This matches words starting and ending with cat.
- Note : `<` or `>` is not metacharacters, we need `\` to escape them
- NOTE : not all `egrep` version supports this metacharacter.

**Optional Items**

- Lets find words : `color` and `colour` :)
- `?` means optional character.
- Above could be done using : `colou?r`
- Another use Case lets find characters where `(July|Jul) (fourth|4th|4)` can be reduced to `July? (fourth|4th|4)`
- further simplication can be done `July? (fourth|4(th)?)` . NOTE: here `()` are used to create subexpression for `?`

**Repetition**

- `+` : one or more of the immediately preceding item
- `*`: any number, including none of the item

phrased differently

- `...*` : means match as many times as possible, but its ok to settle for nothing if need be
- `...+` : means match as many times as possible, but fails only if not even single match found

NOTE: `...?` or `...*` always succeeds as they match none also

NOTE : `.?` means a single space while `.*` means everything.

A direct consequence of above is that lets say you want to match 15 or any number : one way is `[0-9][0-9]` (which is wrong) another is just `[0-9]+`

**Defined range of matches: intervals**

- `...{min,max}` : some version of `egrep` supports a metasequence for providing min and max occurrences.
- `...{3,12}` matches upto 12 times if possible, but settles for 3
- `[a-zA-Z]{1,5}` : this can match US stock ticker from 1-5 letters. So our `?` is just `{0,1}` :)

**Parentheses and Backreferences**

- In many regex flavors, parenthesis can “remember” text matched by subexpression they enclose
- We are now equipped to solve double word problem : `\<the.+the\>` (note . here only represents space) this should display all double occuring `the` word (word boundries are important here) : let’s replace the with general word : `\<[A-Za-z]+.+[A-Za-z]+\>` this solution can be minimized in size by back capture of first match using `()` and can be backreferenced using `\1` : this order goes from left to right for each capture group numbering.
- Effectively our regex becomes : `\<([A-Za-z]+).+\1\>`

**The Great Escape**

- how to match metacharacters ? we can use escape characters for that. `ega\.att\.com`
- Another example is escaping `\([A-Za-z]+\)` : this matches parenthesised words

### The Goal of Regular Expression

Sometimes goal of regex is not just to match but also operate on the matched text. For example looking for some number in a text file to update/add/subtract it.

Other interesting Examples : 

- Variable Names : doesn’t start with digit. they are matched by `[a-zA-Z_]*`. If there is limit on size of varible name you can replace that by `{0,32}` or something else.
- A string within double quotes : `"[^"]*"` inner `^"` prevents matching of unbalanced quotes :P
- Dollar amount with optional cents : `\$[0-9]+(\.[0-9][0-9])?`
- An HTTP/HTML URL : `\<http://[-a-z0-9_.:]+/[-a-z0-9_:@&?=+,.!/~*%$]*\.html?\>` this could be simplified to `\<http://[^ ]*\.html?\>`
- Knowing the data you’ll be searching is an important aspect of finding the balance between complexity and completeness.
- An HTML Tag : `<.*>` (little incorrect but this is simpler)
- Time of day such as “9:17am” or “12:30pm” : `[0-9]?[0-9]:[0-9][0-9] (am|pm)` This is very generic but we know time is maximum till 12:00 am/pm. Further simplifying : `(1[012]|[1-9]):[0-5][0-9] (am|pm)`

### Regular Expression Nomenclature

- Regex : Short form of Regular expression
- Matching
- Metacharacter
- Flavor (don’t confuse with different tools, same tool’s older version may behave differently)
- Subexpression
- Character



---

## File: regex/jeff/ch2.md

## Extended Introductory Examples

Double word problem might look like this in perl

````perl
$/=".\n"
while(<>) {
	next if !s/\b([a-z]+)((?:\s|<[^>]+>)+)
	(\1\b)/\e[7m$1\e[m$2\e[7m$3\e[m/ig;
  s/^(?:[^\e]*\n)+//mg;	# Remove any unmarked lines.
  s/^/$ARGV: /mg;		# Ensure lines begin with filename.
	print;
}
````



Most of this program revolves around three regular expression

- `\b([a-z]+)((?:\s|<[^>]+>)+)(\1\b)`
- `^(?:[^\e]*\n)+`
- `^`

All three look different because they are written in perl flavor not the egrep flavour.

#### A Short Introduction to Perl

Perl is a powerful scripting language first developed in the late 1980s, drawing ideas from many other programming language and tools.

A simple program

````perl
$celsius=30;
$fahrenheit=($celsius*9/5)+32;			# this is a comment
print "$celsius C is $fahrenheit F.\n";
````

when executed prints : `30 C is 86 F.`

Another construct

````perl
$celsius=30;
while($celsius<=45){
  $fahrenheit=($celsius*9/5)+32;			# this is a comment
  print "$celsius C is $fahrenheit F.\n";
  $celsius=$celsius+5;
}
````

To run above script : `perl -w temps`

#### Matching Text with Regular Expressions

checking `$reply` contains only digits

````perl
if($reply=~m/^[0-9]+$/) {			# here m : is for matching m/reg-exp/
	print "only digits\n"
} else {
	print "not only digits\n"
}
````

Now combine both examples to validate stdin is providing correct number only to Celsius

Allowing negative/positive number `[-+]`

````perl
$celsius =~ m/^([-+]?[0-9]+)([CF])$/
````

Note pairs of `()` those are added for capturing matches and can be referenced by `$1 or $2` in perl.

Lets add more intertwined regex and allow floating point numbers

````perl
$celsius =~ m/^([-+]?[0-9]+(\.[0-9]*)?)([CF])$/
````

Capture groups : $1 : entire number, while \$2 is just floating part and \$3 is C/F.

We can even add more minute details like allowing spaces and tabs using Perl’s metacharacter inspired based of ASCII characters

`\t \b(word_boundary) \f \n`

NOTE: `\b` matches word boundary normally but matches backspace within character class

**Generic “whitespace” with \s**

Rather than making combination of `\t` and `\ ` we use `\s` to denote generic space

To make matching case insensitive we can use `i` modifier like this `m/regexp/i`. Other important modifiers are `/g(global-match) or /x(free form expression)`

| Character | Description                                                  |
| --------- | ------------------------------------------------------------ |
| `\t`      | a tab character                                              |
| `\n`      | a newline character                                          |
| `\r`      | a carriage-return character                                  |
| `\s`      | matches “any” whitespace(space, tab, newline, formed, and such) |
| `\S`      | anything not `\s`                                            |
| `\w`      | `[a-zA-Z0-9_]` (useful as in `\w+`,extensibly to match a word) |
| `\W`      | anything not `\w`                                            |
| `\d`      | `[0-9]`, i.e. a digit                                        |
| `\D`      | anything not `\d`                                            |

### Modifying Text with Regular Expression

We will use `$var=~ s/regex/replacement` is used to replace matches.

Example : replace Jeff with Jeffrey in the text :

`$var =~ s/\bJeff\b/Jeffrey`

Example of form letter with references left for later substitution based on input from other script or same program is best. You can use `/g` flag to make perl keep on making substitutions

#### Example: Prettyfying a Stock Price

Let’s price of a stock is `9.050000003723` but we want to display it as `9.05`. We could do so by some fancy printf. So our choice is take two fraction digit only if third one is 0 or else take all 3 digits.

```perl
$price =~ s/(\.\d\d[1-9]?)/$1/			# see we used captured value :)
```

#### Automated Editing

So let’s say we want to replace all occurances of word `sysread` with `read`, we can do so just by using perl command line

```perl
perl -p -i -e 's/sysread/read/g' file
```

#### A Small Mail Utility

-- READ in BOOK -- (Interesting approach to solve reply tree problem in mails)

**Adding Commas to a Number with Lookaround**

Convert the following number into 298444215 into 298,444,215. When we think of this, we mentally make pairs of 3 digits and append commas while doing that from right to left. We can use a feature called `lookaround` to solve this problem.

Lookaround doesn’t match text, but rather match *positions* within the text. similar to (`\b` or `^` or `$`). Lookahead is a special type of look around which peeks forwards in text (towards right) to see if subexpression can match, and is successful as a regex component if it can.

Positive lookahead is done using `(?=...)` Another lookaround is lookbehind which looks back (toward left) `(?<=...)`

**Lookaround doesn’t consume text**

Let’s see an example : There is a word by Jeffrey Friedl

`(?=Jeffrey)` only matches the position only `by ^Jeffrey Friedl` (here ^ denotes position matched by lookahead) now we can apply regex to this lookahead like this `(?=Jeffrey)Jeff`

This will help us not match words like “by Thomas Jefferson”

Another lookahead that is correct would be `Jeff(?=rey)` So our solution becomes

```perl
$pop =~ s/(?<=\d)(?=(\d\d\d)+$)/,/g
```

this resolves `^.123.456.789` (`.` representing lookahead match, `^` representing lookbehind match)

`(?<=\d)` : at least some digits on left

`(\d\d\d)+$` : matches sets of triple digits to the end of the string.(nothing follows or else we get 1,2,3,4,5,678 as matches)

NOTICE we didn’t capture any of the word for replacement, rather we captured locations.

**Word Boundaries and negative lookaround**

how can we use this expression to replace word in a sentence for commas like this : “The population of 31414151 is growing.”. Now in this case `$` reference fails and we end up with 3,1,4,1,4,151 becase anchor to end fails but we can replace `$` with something like `\b` to match word boundary.

| type                | regex      | successful if enclosed subexpression   |
| ------------------- | ---------- | -------------------------------------- |
| Positive Lookbehind | `(?<=...)` | successful if can match to the left    |
| Negative Lookbehind | `(?<!...)` | successful if can’t match to the left  |
| Positive Lookahead  | `(?=...)`  | successful if can match to the right   |
| Negative Lookahead  | `(?!...)`  | successful if can’t match to the right |

So our new expression using above becomes, by anchoring last character being not a digit i.e. alphabet

````perl
$text =~ s/(?<=\d)(?=(\d\d\d))+(?!\d)/,/g;
````

**Commaficatin without lookbehind**

lookbehind is not supported as widely as lookahead. so solution with lookahead only.

````perl
$text =~ s/(\d)(?=(\d\d\d)+(?d!\d))/$1,/g;
````

Here note we are not capturing position, instead every digit that is fourth from end and just replacing that with itself and a comma.

Other fun examples : Convert txt to HTML, Matching the username and hostname.

Tip with enought knowledge of perl seek out understanding double word problem mentioned in the start of the chapter.



---

## File: regex/jeff/ch3.md

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



---

## File: regex/jeff/ch5.md

## Practical Regex Techniques

Writing good regular expression is more than skill - it’s an art. One doesn’t teach or learn this art with lists or rules, but rather, through experience.

Writing good regex involves striking balance among several concerns:

- matching what you want, but only what you want
- keeping the regex manageable and understandable
- For an NFA, being efficient. (Context-Dependent)

### A Few Short Examples

#### Matching an IP Address

Four numbers separated by dots such as : `1.2.3.4`, often padded with 0 and can be maximum of 3 digit.

Most simplest regex would be `[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*`, but it looks vague and matches incorrectly as it only matches 3 dots. Let’s fix this : first let’s change * with + because there should be atleast one number between dots. Next we ensure entire string is IP address only using `^` and `$`.

Now regex becomes `^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$`. let’s simplify more using `\d` for `[0-9]`. New regex `^\d+\.d+\.d+\d+$` but its still wrong as it can match any number of digits, let’s fix the range.

New regex `^\d{1,3}\.d{1,3}\.d{1,3}\d{1,3}$` or we could use following if range is not available `\d\d?\d?`

Still this is not correct because above matches IP address `999.999.999.999` so let’s limit that range. One silly approach might be `[1|2|...|254|255]` if we include zero padding things become worse :P and for FNA altercation can be expensive.

A realistic approach would be focusing on digits. If a number is only one or two digits long, there is no worry as to whether the value is within range, so `\d|\d\d` takes care of that. more refined approach is `[01]\d\d` further on same lines `\d|\d\d|[01]\d\d` this is good for limit of 000-199 with allowing padding zeroes.

Let’s apply above solutino for 000-255. `\d|\d\d|[01]\d\d|2[0-4]\d|25[0-5]`, actually now we can combine first 3 alternation into `[01]?\d\d?|2[0-4]\d|25[0-5]`. Repeating this 3 times would make a correct original regex.

But above is still incorrect as it allows `0.0.0.0` which could be removed using lookahead. `(?!^0+\.0+\.0+\.0+$)`. So with this, we can see choosing how much details you need for your pattern totally depends on the potential text you are going to get :). Know your context.

#### Working with Filenames

**Removing the leading path from a filename**

A simple example is /usr/local/bin/gcc, let’s redact it to file name only that is gcc. In this case we want to remove everything upto last `/`. How about `.*` greediness :). With `^.*/` we basically remove everything upto last / and then stop that leaves the last name only. so we replace this match with empty characters leaving last name. In perl `$f =~ s{^.*/}{};`

Let’s understand how NFA based regex engine will work, it will first anchor at start and keeps matching greedily till end, then it backs off from there and finding last `/`. but same again starts from second character because of how `.*` mechanics work. all NFA engines are smart enough to know if first match from first character for `.*` failed, then it will ultimately fail for all upcoming characters. Still we can improve on this and define more clearer regex.

Another approach is bypass the filepath and just match the file name. `[^/]*$`. It always matches and only requirement is that string ends. but note its very inefficient the way NFA engine works. it backtracks over 40 times before matching. but anyways 40 backtracks is nothing :P

**Both leading path and filename**

We could do something like this to capture `$1, $2` using `^(.*)/(.*)$` we know first `.*` is greedy and does what we want but never leave same for $2, here it works fine but not always so rather use this. `^(.*)([^/]*)$`

**Matching Balanced Sets of Parentheses**

Its a very interest C problem but could be done using regex as well. Its useful problem while defining configuration files, programs or such.

First ignoring the fact that there could be nested `[]` we could come up with `\bfoo\([^)]*\)` but it won’t work. here we used foo for C function like `foo(somevar,2,7)`

Assume Text : `val = foo(bar(this), 3.7) + 2 * (that - 1);`

you could up with 3 approach

- `\(.*\)` : doesn’t work as matches too much
- `\([^)]*\)` : doesn’t work correctly check for above example
- `\([^()]*\)` : doesn’t even match anything

The real issues is you simple can’t match arbitarily nested constructs with regex. For long time it was universally true, but with Perl, .NET, and PCRE/PHP all offers construct that make it possible.

```perl
$regex = '\(('.'(?:[^()]|\('x $depth .'[^()]*'.'\))*'x $depth .\)';
```



**Matching a Delimited Text**

- Matching a C comment enclose in `/* -- code -- */`
- Matching an HTML tag, which is text wrapped by `<...>`
- Extracting items between HTML tags, such as ‘super exciting’ of HTML `a<i>super exciting</i> offer!`
- Matching a line in .mailrc file. This file gives email aliases, where each line is in format : `alias shorthand fulladdress` (delimiter is whitespace lol)
- Matching a quoted string but allowing it ot contain quotes if they are escaped
- parsing CSV files

We here have three requirements

1. Matching opening delimiter
2. Match the main text
3. Match the closing delimiter

**Allowing escaped quotes in double-quoted strings**

**Parsing CSV Files**

Parsing CSV can be little bit tricky, as it can be a raw CSV or withing double quotes CSV and different delimiters.

Example : Ten Thousand, 10000, 2710 ,,”10,000”, “It’s ”“10 Grand”“,baby”, 10K

Above row is 7 fields separated by `,` but not inside quotes. So we will need an expression to cover each two types of fields. The non-quoted ones are easy- they contain anything except commas and quotes so `[^",]+`

A double quoted field can contain commas, spaces and in fact anything except a double quote. It can also contain two quotes in a row that represent one quote in the final value. So a double-quoted field is matched by any number of `[^ "]` between `“..."`, which gives us `"(?:[^ "] | "")*"`. Putting together both pieces we get `[^",]+ | "(?:[^"] | "")*"`

We missed something subtle tho, that is we missed empty field :P

---

