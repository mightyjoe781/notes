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

