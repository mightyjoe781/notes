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