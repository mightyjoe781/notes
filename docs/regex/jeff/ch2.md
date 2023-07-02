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

