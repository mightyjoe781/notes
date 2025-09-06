# Summary of Practical Vim

TIP 1 : Meet the dot command ! Use `.` command as much as you can.

TIP 2 : Don’t repeat yourself ! Use Two for Price of one.

- Use keys like `C(c$), s(cl), S(^C), A($a), I(^i), o(A<CR>), O(ko)` as much as you can.

TIP 3 : Take One step back, Then Three Forward.

- (Inserting spaces in front and back of a character). Use `s` like this to enter spaces. `f+s<space>+<space>`. We can do this with all occurances using `;` to go to next occurance and use `.` to execute above instruction again.

TIP 4 : Act, Repeat, Reverse

- `@:` or `&` : can repeat last `:` command which could be a `:substitute`. Remember u can always use `u` to reverse unwanted changes.

TIP 5 : Find and Replace by Hand

- Be Lazy : Search without Typing (use `*`).

TIP 6 : Meet the dot formula. (The Ideal : One Keystroke to move, One keystroke to execute)

### Part 1 : Modes

#### Chapter 2 : Normal Mode

TIP 7 : Pause with Your Brush Off the Page (Discussion on why default mode is normal mode)

TIP 8 : Chunck your Undos (Moderating use `ESC` helps us achieve chunking of undo, `u` in vim depends on NormalMode-> InsertMode-> ESC)

TIP 9 : Compose Repeatable Changes. (`daw` is better way to delete a word rather many different ways, because `.` command can be composed to utilise entire operation.)

TIP 10 : Use counts to Do Simple Arithmetic. `{val}Ctrl-a` and `{val}Ctrl-x` . Note cursor need not to be on number ;P

TIP 11 : Don’t count if you can repeat

TIP 12 : Combine and Conquer (Operator + motion = action)

#### Chapter 3 : Insert Mode

TIP 13 : Make correction instantly from Insert Mode

- In insert mode : `<C-h>` Delete one character, `<C-w>` Delete back one word, `<C-u>` delete back one line

TIP 14 : Get back to normal mode

- `<ESC>` or `<C-[>` or `<C-o>` to go into normal mode. Last one is special Insert Normal Mode aka one bullet mode :)

TIP 15 : paste from register without leaving insert mode

- `<C-r>{register}` to paste a register

TIP 16 : Do the back of the envelope calculation in place (The Expression Register) (In insert mode : `<C-r>=`)

TIP 17 : Insert unusual characters by character code. (In insert mode `<C-v>{character_code}`, e.g. `<C-v>065` is same ‘A’)

TIP 18: Insert Unusual characters by digraph. (For example try : In insert mode `<C-k>?I`)

- Fraction are `12, 14, 43` for `1/2 or 1/4 or 4/3`

TIP 19 : Overwrite existing text with Replace Mode. (Note : Use special `gR` : Virtual Replace mode for those tab style weirdos :) and it replaces tabs with spaces)

#### Chapter 4 : Visual Mode

TIP 20 : Grok Visual Mode. (To quickly replace some words  `viw` and then `c` to change its value, we can utilise all motion keybindings in visual mode). To trigger select mode `<C-g>`.

TIP 21 : Define a Visual Selection. (`v` , `V`, `<C-v>`, `gv` (last selection)) You can use `o` to jump around.

TIP 22 : Repeat Line-wise visual commands. (Yes `.` is our friend)

TIP 23 : Prefer Operators to Visual Commands wherever possible. (Sometime `.` doesn’t play well in visual mode)

TIP 24 : Edit tabular data with visual block mode.

TIP 25 : Change the Columns of Table. (Append EOF on visual block on text)

TIP 26 : Append After a ragged Visual Block

#### Chapter 5 : Command Line Mode

TIP 27 : Meet Vim’s Command Line : `:` to invoke command lines, refer [Link](../notes.md) (Ex Commands Strike far and wide than normal mode)

TIP 28 : Execute a command on one or more cosecutive lines. `:{start},{end}` for selection text

TIP 29 : Duplicate or Move lines using `:t` or `:m` commands

TIP 30 : Run normal mode commands across a range. (`:%normal A;`  to semi colon the entire file :) (`:%normal i//` to comment entire file)

TIP 31 : Repeat Last Ex Command. `@:`

TIP 32 : Tab complete your Ex Command. (`<C-d>` to open entire list of suggestion)

TIP 33 : Insert Current word at Command Prompt. (`<C-r><C-w>` copies word under cursor and puts in command prompt)

TIP 34 : Recall commands from History. (`q:`) to quickly access command window.

TIP 35 : Run commands in shell.`!{cmd}` or utilise `:shell` command of vim

- To view output in of vim’s cmd execute `:read!{cmd}`
- To use contents of current buffer as input for cmd `:write!{cmd}`
- Sort a list of numbers using above technique :) `:2,5!sort -k2`

### Part 2 : Files

#### Chapter 6 : Manage Multiple Files

TIP 36 : Run multiple Ex Commands as a Batch

TIP 37 : Track Open files with the Buffer Lists.

- Some Important Commands : `:ls`, `:bnext`, `:bprev`
- Use mappings similar to Tim Pope's unimpaired.vim plugin. (`[b ]b [B ]B`)

TIP 38 : Group Buffers into a Collection with Argument List. (Utilize `:argdo` then to act on that list) (`:args` have buffers those are opened while opening vim).

TIP 39 : Manage Hidden Files

TIP 40 : Divide your workspace in Split windows

TIP 41 : Organize your windows Layout with Tab Pages\

#### Chater 7 : Open Files and Save Them to Disk

TIP 42 : Open a file by its Filepath using `:edit`

TIP 43 : Open a File by Its Filesename using `:find`

TIP 44 : Explore FileSystem with Netrw

TIP 45 : Save Files to Nonexistent Directories. (`:!mkdir -p %:h`)

TIP 46 : Save a File as the Super User. (`:w !sudo tee % > /dev/null`)

### Part 3 : Getting Around Faster

#### Chapter 8 : Navigate Inside Files with Motions

TIP 47 : Keep your Fingers on the Home Row. (Disable Arrow Keys)

TIP 48 : Distinguish between Real Lines and Display Lines. (Difference after enabling wrap mode)

TIP 49 : Move word-wise. Use `w`, `e` ,`b`, `ge`, `W`, `B`, `ea` (feels like one key)

TIP 50 : Find by Character. `f{char}`, `F{char}`, `t{char}`, `T{char}`, `;`, `,`

TIP 51 : Search to Navigate

- We can combine search with motions. `v/ge<CR>` selects text till /ge. or `d/ge<CR>` deletes text till ge.

TIP 52 : Trace your selection with precision Text Objects.

TIP 53 : Delete Around, or Change Inside. (`iw`, `iW`, `is`, `ip` or their `a` variants).

TIP 54 : Mark Your Place and Snap Back to It. `m{a-zA-z}` commands marks the current cursor position.

- {a-z} : are local marks for a buffer, `A-Z` : are global marks.

- `‘{mark}` : move cursor to front of line where cursor was marked. (Used in context of `Ex` commands)
- ``{mark` : moves cursor to exact character where cursor was marked.
- Automatic Marks :`“` (position before last jump) , `".`( location of last change) , `‘^` (location of last insertion) or `gi` , `‘[` (start of last change/yank) , `‘]`, `‘<`(start of last visual selection), `‘>`

TIP 55 : Jump between matching parenthesis. Use `% `

#### Chapter 9 :  Navigate Between Files with Jumps

TIP 56 : Traverse Jump List. (`<C-o> and <C-i>`)

TIP 57 : Traverse Change List. (`g;`, `g,` or hackish `u<C-r>`)

TIP 58 : Jump to the Filename Under the Cursor. (`gf`, Use `suffuxesadd` to configure gf to work correctly for files)

TIP 59 : Snap Between Files Using Global Marks. Always set global marks before executing commands like `bufdo`, `vimgrep`  using `mM`

### Part 4 : Registers

#### Chapter 10 : Copy and Paste

TIP 60 : Delete, Yank, and Put with Vim’s Unnamed Registers.

- Conecpt of Transposing Characters `xp` , Lines `ddp` and `yyp`

TIP 61 : Grok vim’s registers

- `“{register}` , if no register is specified, vim uses unnamed(`“"`) register by default.
- Yank Register `“0` , The BlackHole Register (`”_`)
- System Clipboard (`“+`) and selection (`”*`) Registers, Expression Register (`“=`)

TIP 62 : Replace a Visual Selection with Register. (Useful for swapping values inplace in unnamed register).

TIP 63 : Paste from a register. (Remember this nmenonic : `puP` and `Pup`) We can use `<C-r>0` to paste registers in insert mode.

TIP 64 : Interact with the System Clipboard. (Pasting in windows and linux messes up formatting if autoindent is enabled)

#### Chapter 11 : Macros

TIP 65 : Record and Execute a Macro. (Record : `q{register}` and to stop recording `q` and to replay `@a`)

TIP 66 : Normalize cursor position (`0`) , Strike (Use correct motions like `p`, `w`, text-objects), Abort (vim stops macro execution if it encounters a motion that can’t be replayed).

TIP 67 : Playback with a count. (`qq;.q` to store last command in macro and then executing dot command multiple times.)

TIP 68 : Reapeat a Change on Contigous Lines. (Use parallel execution `Select ---> Apply Macro`) (Select the lines then `:'<,'>normal @a`)

TIP 69 : Append Commands to a Macro. (`q{capital-register}`)

TIP 70 : Act Upon a Collection of Files. `:argdo normal @a`

TIP 71 : Evaluate an Iterator to Number Items in a List.

- Put line number in front of every line, we will utilize rudimentry vim script
- `:let i=1` (declare var i = 1) , `qa` (start macro recording) , `I<C-r>=i<CR>)<ESC>` (prints current value of i), `:let i+=1` (increment counter), `q` (stop macro recorder).

TIP 72 : Edit the Contents of Macro

- `:put a` : put contents of macro at the end file.
- Make changes to macro
- `“add` : yank the text back into macro.

### Part 5 : Patterns

#### Chapter 12 : Matching Patterns and Literals

TIP 73 : Tune the Case Sensitivity of Search Patterns

- sets case sensitivity globally `:set ignorecase`
- Setting Case sensitivity per Search : `\c` (ignorecase) and `\C` (strict case)
- Enabling Smarter Default Case Sensitivity : `smartcase` (disabled ignorecase if search term has capital letters)

TIP 74 : Use the \v Pattern Switch for Regex Searches

- Find Hex Colors with Magic Search
    - `/#\([0-9a-fA-F]\{6}\|[0-9a-fA-F]\{3}\)`
    - `/\v#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})` (very magic, similar to perl, python or Ruby)
    - Using Hex Character class further reduces expression. `/\v#(\x{6}|\x{3})`
    - Very Magic `\v` matches all characters literally except `_`.

TIP 75 : Use the `\V` Literal Switch for Verbatim Search.

- If we search for word `a.k.a` then match result will not work correctly
- `/a\.k\.a\.`  : is correct matching regex
- `/\Va.k.a` : is shorter and Verbatim Search

TIP 76 : Use Parentheses to Capture Submatches.

- `/\v<(\w+)\_s+\1>` : This regex matches duplicate words

TIP 77 : Stake the boundaries of a word.

- In `very magic` Searches `<` and `>` represents word boundary delimiters. `\v<the><CR>` : for searching the word `the` exactly. Zero Width Items.
- In `nomagic` , `magic`, `very nomagic` searches `<` and `>` needs to be escaped.
- Anyways `*` and `#` also does the same thing and includes word delimiter and `g*` and `g#` doens’t include word delimiter.

TIP 78 : Stake the Boundaries of a Match

- Vim’s `\zs` and `\ze` allows us to specify a broad search pattern and then focus on a subset of a match.
- Conceptually similar to Perl’s *lookaround assertions*.
- `\v"\zs[^"]+\ze"<CR>` : Matches quote words but not quote marks.

TIP 79 : Escape Problem Characters

- `\V` literal switch makes easier to search for text verbatim because disables the meaning for the `.`, `+` and `*` symbols, but there are a few characters whose special meaning can’t be turned off.

#### Chapter 13 : Search

TIP 80 : Meet the Search Command. (`/{search-pattern-text}` forward search, or use `?` for backward search).

- `gn` and `gN` can visual select search matches

TIP 81 : Highlight Search Matches. `hlsearch` . Sometimes it can be a very annoying option and we can utilize this mapping to clear highlighted searches and redraw screen. `nnoremap <silent> <C-l> :<C-u>nohlsearch<CR><C-l>`

TIP 82 : Preview the First match Before Execution.

- Enable `incsearch`
- Autocomplete : `<C-r><C-w>`

TIP 83 : Offset the Cursor to the End of a Search Match

- `/lang/e` : puts cursor at the end of word match
- This could be done even after the search has been executed : Use `//e<CR>`

TIP 84 : Operate on a Complete Search Match. Utilise `gn` to jump to next word as well and condense the DOT formula.

- Improved dot formula requires only 1 step `.` command only, by default it jumps to next occurance.

TIP 85 : Create Complex Pattern by Iterating upon Search History. Utilise `q/` to prepopulated search history to revise our search patterns. Then we can use `:%s//"\1"/g` (empty search field defaults to last search, and `\1` register stores current match word)

TIP 86 : Count the Matches for the Current Pattern

- `/{text-to-search}` then `:%s///gn ` (mathes last search and counts its occurence)
- `/{text-to-search}` then `:vimgrep //g %` , you can then navigate using `n` , `N` or `:cnext`, `:cprev`

TIP 87 : Search for Current Visual Selection

#### Chapter 14 : Substitution

TIP 88 : Meet the Substitution Command

- `:[range]s[ubstitute]/{pattern}/{string}/[flags]` : General format for substitution phrase.
- Flags : `g` : globally, `c` : confirm/reject choice, `n` : usual substitute behaviour with reporting # occurances that will be affected, `&` : reuse same flags from previous substitute command
- Special Characters for Replacement String : `\r` , `\t` , `\\` , `\1` , `\2`, `\0` ,`&`,`~` and `\={vim-script}`

TIP 89 : Find and Replace Every Match in a File

- By default command works line wise and including `g` makes it act on entire line
- `%` range is applied on every line of file.

TIP 90 : Eyeball Each Substitution. (C flag is very useful)

- `%s/content/copy/gc` : substitution with global confirm

TIP 91 : Reuse the Last Search Pattern. (Leaving the search field of substitute command blank instructs vim to reuse most recent search pattern)

TIP 92 : Replace with the Contents of a Register.

- Pass by value : `:%s//<C-r>0/g`
- Pass by reference : `:%s//\=@0/g`

TIP 93 : Repeat the Previous Substitute Command

- `:s/target/replacement/g` to repeat it we can utilise `:%s//~/&`

- `:&&` (last ex command followed by last flags) or `g&` repeats last substitutions

TIP 94 : Rearrange CSV Fields Using Submatches

- swapping order of fields in CSV three fields : `/\v^([^,]*),([^,]*),([^,]*)$` Now execute substitute to search and reference these submatches `:%s//\3,\2,\1`

TIP 95 : Perform Arithmetic on the Replacement

- Example promote all hx tags by 1 value : Search : `/\v\<\/?h\zs\d` now Substitue : `:%s//\=submatch(0)-1/g`

TIP 96 : Swap two or more words

- Simple trick , we will create a dictionary like this : `:let swapper={"dog":"man", "man":"dog"}` now `swapper["dog"] = man` and vice-versa
- Together in order : Search `/\v(<man>|<dog>)` then substitute `:%s//\={"dog":"man","man":"dog"}[submatch(1)]/g`
- Even though in above example it seem like expensive thing to do for 2 variable but its very powerful when we got multiple variable whose value need to be changed.
- You could try the Tim pope’s Abolish.vim : `:%S/{man,dog}/{dog,man}/g`

TIP 97 : Find and Replace Across Multiple Files

- Project Wide Search : `/Pragmatic\ze Vim` then `:vimgrep // **/*.txt ` (Every result from vimgrep is stored in quick fix list, can be confirmed using `copen`).
- Project-Wide Substitution : `:set hidden` then `:cfdo %s//Practical/gc` then `:cfdo update` Last two commands combined : `:cfdo %s//Practical/gc | update` (cfdo operates on quickfix list).

#### Chapter 15 : Global Commands

`:global` Commands combine the power `EX` commands with Vim’s Pattern matching ability

TIP 98 : Meet the Global Command

- `:[range] global[!] /{pattern}/ [cmd]` : (default range in `%`) 
- `global!` is same as `vglobal` which inverts the functionality of above command

TIP 99 : Delete lines containing a Pattern

- Combining the `:global` and `:delete` commands allows us to cut down the size of a file rapidly.
- Deleting Matching lines with `:g/re/d` : First lets search : `/\v\<\/?\w+>`(matches html tags) then `:g//d`
- Keep only matching lines with `:v/re/d` : Use this functionality `:v/href/d`

TIP 100 : Collect TODO Items in a Register. (Combining the `:global` and `:yank` command allows us to collect all lines that match a {pattern} in a register.)

- Lets assume file has text `// TODO : {some-todo}`
- Collect all those files that have TODO text : `:g/TODO `(default cmd is :print so it actually prints the lines)
- Yanking all lines that contain TODO text in a register. First clear the reigster `qaq`. Now `:g/TODO/yank A`
- We could combine the `:global` command with either `:bufdo` or `:argdo` to collect all TODO items from a set of files.
- We could also copy text to end of file : `:g/TODO/t$` 

TIP 101 : Alphabetize the properties of Each Rule in a CSS File.

- `:g/{pattern}/[range][cmd]` : limits the execution of gloabl command
- A generalised form of this `:global` command goes like this `:g/{start}/ .,{finish} [cmd]`
- Sorting all blocks of rules with this trick `:g/{/ .+1,/}/-1 sort` or we could indent all properties inside blocks `:g/{/ .+1,/}/-1 >` to silent `:>` prints use `:sil` command like this `:g/{/sil . +1,/}/-1 >`

### Part 6 : Tools

#### Chapter 16 : Index and Navigate Source Code with ctags

TIP 102 : Meet ctags

- Installing Exuberant Ctag

  ```bash
  sudo apt-get install exuberant-ctags
  ```

  MacOS user already have BSD version of ctags.

- Indexing a Codebase with ctags : `ctags *.rb`, Now directory contains a plain text file called as `tags`

- Anatomy of a tags File

    - Keywords Are Addressed by Pattern, Not by Line Number
    - Keywords Are Tagged with Metadata

TIP 103 : Configure Vim to work with ctags

- Tell vim where to find the tags file. `:set tags? `output should be `tags=./tags,tags`. So vim only matches till first match. Ideally we should have tags file in every directory or we could keep things simple by having a global tags file at root of project directory.
- Execute ctags Manually : `:!ctags -R`, we could create mapping for it. `:nnoremap <f5> :!ctags -R --exclude=.git --languages=-sql<CR>`
- Vim’s autocommands can execute ctags Each Time a File is Saved. `:autocmd BufWritePost * call system("ctags -R")`
- Automatically execute ctags with Version Control Hooks : In “Effortless Ctags with Git,” Tim Pope demonstrates how to set up hooks for the post-commit, post-merge, and post-checkout events

TIP 104 : Navigate Keyword Definitions with Vim’s Tag Navigation Commands

- Usage of `<C-]>` and `g<C-]>` to navigate using ctags.
- Use `<C-t>` as a history button to navigate tag history.
- In case of multiple matches use `g<C-]>` and select the appropriate jump.
- Using Ex Commands : We don’t have to move the cursor on top of a keyword to jump to its tag using  `:tag {keyword/regex}` and `:tjump {keyword/regex}`.
- Other keys `:tnext` , `:tprev` ,`:tfirst` , `:tlast` , `:tselect` ,`:pop` or `<C-t>`, `:tjump`

#### Chapter 17 : Compile Code and Navigate Errors with the Quickfix List

TIP 105 : Compile code without Leaving Vim

- Preparation : Download the Examples. Cd to `code/quickfix/wakeup` directory.
- Compile project in the shell : `gcc -c -O wakeup.o wakeup.c`
- You will get some errors but thats alright.
- Compiling from inside the vim. Launching vim with Makefile. `vim -u NONE -N wakeup.c`
- From inside vim execute : `:make`. Upon encountering error vim moves you to the first error in quickfixlist. To avoid moving cursor automatically. `:make!` or use `<C-o>`
- Now fixing the issue and recompiling using `:make` causes vim to clear quickfix list (since no errors) and leaves the cursor as it is.

TIP 106 : Browse the Quickfix List

- Main set of commands : `:cnext` , `:cprev`, `:cfirst` , `:clast` , `:cnfile` (first item in next file), `:cpfile` (last item in previous file), `:cc N` jumps to *n*th item.
- `:copen` : opens quickfix window, `:cclose` : closes quickfix window.
- `:cdo {cmd}` : execute {cmd} on each line listed in quickfix list
- `:cfdo {cmd}` : execute {cmd} once for each file listed in quickfix list.

TIP 107 : Recall Results from a Previous Quickfix List

- Use `:colder` to get old quickfix list and `:cnewer` to get to new quickfixlist.

TIP 108 : Customize the External Compiler. (vim’s definition of external compiler is loose)

- Customize so that `:make` calls node lint on your machine.
- Install nodelint : `npm install nodelint -g`
- Configure `:make` to invoke Nodelint : `:setlocal makeprg=NODE_DISABLE_COLORS=1\ nodelint\ %`
- Populate the Quickfix List Using Nodelint’s Output : `:setglobal errorformat?` list current error format. Let’s correct it according to Nodelint. `:setlocal efm=%A%f\,\ line\ %l\,\ character\ %c:%m,%Z%.%#,%-G%.%#`
- Setup `makeprg` and `erroformat` with a single command. `:compiler nodelint`

#### Chapter 18 : Search Project-Wide with grep, vimgrep, and Others

TIP 109 : Call grep without leaving vim

- Using grep from command line : `grep -n Waldo *`
- Now we know waldo occurs on line 6  and 9. We can open vim at that exact line number. `vim goldrush.txt +9`
- Now calling grep from Inside Vim `:grep Waldo *`
- Vim parses the result and populates quickfix list and we navigate around very easily

TIP 110 : Customize the grep Program

- `:grep` in vim is a wrapper for external grep program and can be manipulated using `grepprg` and `grepformat`.

- Defaults for both values are :

   	grepprg="grep -n $* /dev/null"
   	grepformat="%f:%l:%m,%f:%l%m,%f  %l%m"

- Make `:grep` call `ack`. Visit this link for details.[Link](https://betterthangrep.com). `:set grepprg=ack\ --nogroup\ $*`

- To make ack store columns also set this :

  ````
  :set grepprg=ack\ --nogroup\ --column\ $*
  :set grepformat=%f:%l:%c:%m
  ````

TIP 111 : Grep with Vim’s Internal Search Engine.

- `:vim[grep][!] /{pattern}/[g][j] {file}`

- `:vimgrep /going/ clock.txt tought.txt where.txt`
- Searching in entire project. First : `/[Dd]on't` then `:vim //g *.txt`

#### Chapter 19 : Dial X for Autocompletion

TIP 112 : Meet Vim’s Keyword Autocompletion

- We can use `<C-p>` and `<C-n>` in insert mode to invoke generic keyword autocompletion.
- `<C-n>` : generic keywords, `<C-x><C-n>` : Current buffer keywords, `<C-x><C-i>` : Included file keywords, `<C-x><C-]>` : tags file keywords, `<C-x><C-l>` whole line completion, `<C-x><C-f>` : filename completion and `<C-x><C-o>` : Omni-completion.

TIP 113 : Work with the Autocomplete Pop-up Menu

- `<C-n>` : use the next match from the list.
- `<C-p>` : Use the previous match from the list.
- `<Down>` : Select the next match from the word list.
- `<Up>` : Select the previous match from the word list.
- `<C-y>` : accept the currently selected match (yes)
- `<C-e>` : Rever to originally typed text (exit from the autocompletion)
- `<C-h>` delete one character from current match
- `<C-l>` add one character from current match
- `{char}` stop completion and insert {char}
- Refine the Word List as You type : `<C-n><C-p>` or `<C-p><C-n>`, similar for omni autocompletion : `<C-x><C-o><C-p>` to perform live filtering on omni autocompletion, or `<C-x><C-f><C-p>` to do the same with filename completion.

TIP 114 : Understand the source of the keyword

- The Buffer List
- Included Files
- Tag Files
- Put It All Together

- Default setting for generic autocompletion : `complete=.,w,b,u,t,i` , to remove or add `:set complete-=i` and `:set complete+=k` respectively

TIP 115 : Autocomplete words from the dictionary

- Triggered using `<C-x><C-k>`
- Use `:set spell` to enable vim’s spell checker

TIP 116 : Autocomplete Entire Lines. (Use `<C-x><C-l>`)

TIP 117 : Autocomplete Sequence of Words. (Vim understand word pasting context and proceeds with pasting words faster) (Utilise `<C-x><C-p>` in rhythm)

TIP 118 : Autocomplete Filenames. (Use `<C-x><C-f>` command)

TIP 119 : Autocomplete with Context-Awareness. (Omni-completion is Vim’s answer to intellisense) It provides a list of suggestion that’s tailored for the context of the cursor placed. Trigger it using `<C-x><C-o>` command. Remember to enable `set nocompatible` and `filetype plugin on`

#### Chapter 20 : Find and fix typos with Vim’s Spell Checker

TIP 120 : Spell Check Your Work. `:set spell`

- Use `[s` and `]s` to jump forward and backward to bad spelled words.
- Press `z=` to check list for correct word
- if confident that first word in spell will be correct use `1z=`
- `zg` (Add current word to spell file) , `zw` (remove current word from spell file), `zug`  revert `zg` or `zw` command for current words.

TIP 121 : Use Alternate Spelling Dictionaries

- Specify a Regional Variant of a Language `:set spelllang=en_us`
- Obtain Spell Files for Other Languages at [here](http://ftp.vim.org/vim/runtime/spell/) : `:set spelllang=fr`

TIP 122 : Add words to the Spell File

- `zg` : adds word to dictionary and `zw` removes the word from dictionary and makes it misspelled word.

- Create a spell file for specialist Jargon. 

  ````vimscript
  setlocal spelllang=en_us
  setlocal spellfile=~/.vim/spell/en.utf-8.add
  setlocal spellfile+=~/books/practical_vim/jargon.utf-8.add
  ````

TIP 123 : Fix Spelling errors from insert mode. 

- Preparation : `:set spell`
- Usual Way : `[s` to jump to previous errors `1z=` put correct word, `A` to come back to insert mode.
- Fast Way : `<C-x>s` or `<C-s><C-x>` to invoke it.
- If line has multiple words which can be corrected try using `<C-x>s` mulitple times its very fast to fix mistakes.

#### Chapter 21 : Now What ?

- Keep Practicing

- Make Vim Your Own

- Know the Saw, Then Sharpen It (Understand vim core functionality before copying someone else’s vimrc)

- Customize Vim to suit your preferences. Read Bram Moolenaar’s classic essay “Seven Habits of Effective Text Editing,”

- Customize Vim to Suit your preference

- Change Vim’s Settings on the Fly

- Apply Customization to Certain Types of Files

  ````vimscript
  if has("autocmd")
  	filetype on
  	autocmd FileType ruby setlocal ts=2 sts=2 sw=2 et
  	autocmd FileType javascript setlocal ts=4 sts=4 sw=4 noet
  	autocmd FileType javascript compiler nodelint
  endif
  ````

  We could put these customization in a separate files also in `~/vim/after/ftplugin/javascript.vim` (ftplugin meaning filetype plugins)

- Enable filetype plugins in vimrc `filetype plugin on`





