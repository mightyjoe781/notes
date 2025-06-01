# Vim Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: vim
This is part 1 of 1 parts

---

## File: vim/index.md

# Vim

Vim, an abbreviation of Vi IMproved, is a free and open-source, screen-based text editor. It is an enhanced clone of Bill Joy's vi. Bram Moolenaar, the author of Vim, developed it from a port of the Stevie editor for Amiga and released a public version in 1991. Vim is designed for use from both a command-line interface and as a standalone application in a graphical user interface.

#### Resources : 

- [Notes](notes.md)
- [Summary Practical Vim](practical_vim/index.md)

- [Vimrc Examples](vimrc.md)
- [Plugins](https://vimawesome.com/)

- [Vimways](https://vimways.org/2019/)

- [vi-improved](https://www.vi-improved.org/recommendations/)

- [Good Vimrc](https://github.com/nelstrom/dotfiles)

#### Other Command Line Editors

- Joe
- neovim
- emacs
- nano



---

## File: vim/notes.md

# Vim Notes

Vim = VI + Improved

why vim ?

1. Vim is Ubiquitous
2. Vim is amazingly powerful
3. Vim’s Knowledge Is Transferable
4. Vim is Cross-Platform
5. Vim is available in a TUI and a GUI
6. Vim has Syntax Highlighting
7. Commands are easy to Remember
8. Vim is Like a Language
9. Vim is Thoroughly Documented

Different Modes in Vim

- Normal/Command Mode
- Insert Mode
- Visual Mode
- Line Mode (`:`)

To exit Vim type `:q`

To open a new file `vim myday.txt`

To save and exit the file `:wq`

`.` repeats previous command !

`!` forces commands in vim. (there are more than 3 uses of !) : Toggle a setting, execute external commands

### Navigation in Vim

- Always use `h, j, k, l` for navigation instead of arrow keys.
- `Ctrl-f` : Page up and `Ctrl-b` : Page Down
- `w` : move forward one word, `W`: move forward one word (ignore punctuation)
- `b` : move backward one word, `B`: move backward one word (ignore punctuation)
- `e` : jumps to end of current work, and move forward to the end of next word, similar as above with `E`
- `z-CR` : move the view up
- `0` or `^` : jump to start of line , `$` : jump to end of line
- `gg` : to move top of file, `G` or `:$` : move to bottom of file
- `Ngg` or `:N` : to jump to Nth line
- `Ctrl-g` : view file info, like status etc, to enable this automatic `set ruler` (Note to disable this : `set ruler!` or `set noruler`)

### Deleting Text and “Thinking in Vim”

- You can combine vim motions with delete !! : “operator + motion“
- Utilise motions to navigate to errors !
- `x` : to delete character cursor is on, `X` : deletes character to left of cursor
- `dw` : delete the word, try `dh, dj, dk, dl` and also `d0, d^, d$`
- `dd` : delete current line, `D` or `d$` deletes all character from cursor to line end
- `Ndd` : delete N lines : “Count + operator + motion”

### Getting Help

- `:help` to get help, use `:q` to exit
- `:help <command>` to get help specific to a command. e.g. `:help dd` 
- `:help {subject}` to get help on a given subject. e.g.  `:help count`
- `:h` is short version of help.
- `Ctrl-w w` to switch to editing and help window.
- `Ctrl-o` : to move to previous cursor position,  `Ctrl-i` to move to next cursor position
- Commands are of two types : `linewise` and `characterwise`, always lookout for this in documentation
- `:h help` to get understanding of how to read the documentation.

### Deleting, Yanking and Putting

- Register is clipboard like storage location
- All deletes are stored in `p` *put* command via **unnamed/default** register
- `p` : put text after cursor, `P` : puts before the cursor
- Copy is usually performed by using yank `y` command puts the text in register.
- cut-copy-paste : delete-yank-put
- `yw, y$, y^` : command + motion
- `yy` : yank lines, `Nyy` : yank N lines
- `u` : undo operations, `Ctrl-R` : redo operation

#### Registers 

- Unnamed  = `“”`
- Numbered = `“1 ”2 "3 "4 ... "9`
- Named = `“a ”b ... "z`

- `“”` : holds text from d, c, s, x and y operation
- `“0` : holds the last text yanked (y)
- `“1` : holds the last text deleted (d) or changed (c)
- Numbered registers shift with each d or c
- To view register contents `:reg`
- To paste the contents of register `“x` type : `“xP ` e.g. `“1P`, where x is a register
- BlackHole register is used to execute commands without affecting other register. `“_dd`
- To yank lines to specific register `“ayy`
- To append more text to a register `“Ayy`
- Trick : `teh` to fix this spelling take cursor to `e` and execute `xp` that should swap `eh`. Very useful trick :) when you are a fast typist.

### Transforming and Substituting text in Vim

- `i` : put your in insert mode.  `I` command puts you in insert mode and towards start of line.
- `a` : appends(puts in insert) after the current character on cursor , `A` : append at the end of line
- `o` : start new line and puts in insert mode. `O` : start new line above and put in insert mode.
- `80i*` : can create a line with 80 asterisk. (Count) + operation
- `5o#` : can create 5 comment lines :P
- `R` invokes ‘REPLACE’ mode that overwrites the characters it encounters
- `r` : invokes replace for only 1 character and keeps you in normal mode
- `cw` : change the entire word, `c$` or `C` : change till end of line (insert mode), `cc` change entire line
- `~` : change the case of character. `g~w` for changing case of entire word, `g~~` or `g~$` change case on entire line.
- `gUU` changes the case the case to upper for entire line, `guu` changes the case to lower for entire line
- `J` joins two lines together with a space. `gJ`  joins two lines without space, `NJ` : to join N lines

### Search, Find and Replace

- `f{char}` : find the first occurance of x towards right of line, `F{char}` : find the first occurance of x towards left of line (Note : both case sensitive) (can combine count also)
- use `;` to repeat `fx` search forwards and `,` for searching backwards
- `tx` and `Tx` : similar to `fx` put cursor before the search hit
- `dfx` : deletes till character x (including x) `dtx` : deletes till charcater x (doesn’t delete x)
- use `/{key}` to search for key in file. `n` : cycle next occurrence and `N` : cycle previous occurence
- Enable incremental search its very useful `set is` also disable highlight search `set nohls`
- A Trick : use `/{key}` to search key and `cw` to change it to `lock` and then `n` to next occurence and `.` to repeat previous command. you could also use `:%s/key/lock/gc` it takes time to type this ;)
- To reverse direction of search `?{key}`
- `*` : searches word under cursor and use normal cycle keys `n` and `N`. or use `#` a reversed search
- To yank all the text from start to first occurance of x in register a  `“ay/x`
- search and replace (substitute) : `:[range]s/old/new/flag` : flags : `g` : global, `gc` : global confirm. Note this works on current line. Now here usually `:%g/old/new` is used for entire file, you could also use some specific line like `:1/x/old/new`. for changing from line 1-5 : `:1,5s/g/old/new`. `$` represent last line in file while `.` represents first line in file. range could also a searchword `:/firstword/,/secondword/s/old/new` 
- For linux user they need to change directory location it maybe difficult to write all escaping `\` characters they can use **pattern separator**. `:%s#/local/mail#/usr/local/mail`

### Text Objects

- `daw` deletes entire word on which cursor is placed (space after word also), `diw` only deletes the word on which cursor is placed.
- pattern : {operator}{a}{object} or {operator}{i}{object}
- most used shortcut is `ciw`(change inner word) and `daw` (delete a word) to quickly refactor variables. (Note use `das` deletes the sentence. try `cis` also)
- So `a` includes the boundaries while `i` doesn’t include boundries of delimiter.
- `dip` (delete inner paragraph, doesn’t include boundry), `dap` includes boundry and deletes paragraph
- most used shortcut to edit the variable value `int name = "smk"`. Take the cursor on value of variable name. `ci"` changes the inner text of delimiter `“` while `da"` will delete word along with delimiter.
- `ci(`, `ci[` or `ci<` or `ci>` are some of other very used shortcuts, you can also yank these value `ya(` or `yi(`
- for html you can use special `at` or `it`.

### Macros

- Macros are recorded sequence of keystrokes. Useful for complex repeated tasks. 
- There are no special registers for macros. There is only one a register.
- `q{register}` : To record in macro in a register. To stop, type `q`.
- `@{register}` : Replay the macro stored in register.
- `@@` : Repeats most recent macro.’
- Best Practices while using macros
  - Normalise the cursor position : 0, 
  - Perform edits and operations
  - position your cursor to enable easy replays : j
- To execute macro on specific range of lines, `:15,20normal @a`
- You can update macros any time : Its as simple as update register use capital letters for macros
- Saving Macros
  - viminfo files : `.viminfo` or `_viminfo`
  - Stores history and non-empty registers
  - read when vim starts
  - can easily overwrite registers
  - vimrc files : `let @d = 'dd'`

### Vim Visual Mode

- `v` : characterwise visual mode, `V` : linewise visual mode, `ctrl-v` : blockwise visual mode
- vim motions and text-objects can be used to expand the visual area
- Commands that work in visual mode
  - ~ : Switch Case, c : Change, d : Delete, y : Yank, r : Replace, x : Delete, I : Insert, A : Append, J : Join, u : Make lowercase, U : make Uppercase
  - \> : shift right, \< : shift left (very important to tab things)
- Blocks mode : `O` toggles current boundry left and right `o` toggles up and down boundary
- Block mode can be utilised to make changes to blocks of lines for example to append `end` to all lines in a block, select block `Aend` will add same word each line
- Note : shiftab defines how much shift operator shifts the selected text
- you can use selected lines/blocks as range in substitue commands
- you can also center text block using selection then `:'<,'>center` (Notice before center represents selection and are populated automatically)
- `gv` reselects last selected text

### vimrc

- rc = `run commands`
- system-wide vimrc and personal virmc
- each line is executed as a command
- To check which vim files are being sourced `:version`
- To check value of some option or its disabled or enabled : `:set {option}?`

````vimrc
" keep 1000 items in history
set history=1000

" show cursor position
set ruler

" show incomplete commands
set showcmd

" shows a menu while using tab completion
set wildmenu

set scrolloff=5
set hlsearch
set incsearch
set ignorecase
set smartcase

set nu
set backup
" set bex=

set lbr "easier linebreak

set ai " autoindent
set si " smartindent

set bg=light
color slate

"map KEY KEYSTROKE
map <F2> iJohn Smith<CR>123 Main Street<CR>London, UK<CR><ESC>

let mapleader=","
map <leader>w :w!<CR>
````

### Vim Buffers

- Temporary area where memory is stored while its being processed
- original file remained unchanged until you write that buffer to file
- `set hidden` : because vim always warns about open unsaved buffer which may be trouble when you wanna switch buffers quickly without saving
- `:buffers` or `:ls`: lists all open buffers
- `:b3` : switches to buffer 3, `:b smk.txt` : switched to buffers assiociated with file `smk.txt`
- `:bn` or `:bnext` : switches to next buffer , `:bp` or `:bpreviouse` : switches to previous buffers (cyclic wrap)
- `Ctrl-^` or `:b#` : switches to last opened buffer (represented by `#` in `:ls` list)
- `+` flag means changes of buffer has not been saved
- `h` or `a` : are hidden and active buffers. Buffers that do not have any flag are not loaded into memory
- `:badd smk.txt` : adds `smk.txt` to buffer
- `:bdelete` or `:bd1` : deletes and removes a buffer
- `:bufdo %s/#/@/g` : applies some operation to all buffers (if `set hidden` is not used then vim can’t switch buffers :) )
- `:wall` : saves all buffers
- `:E` : opens explorer

### Windows

- A window is a view of buffer. (Previously we had multiple files in buffers but to look at more than one buffer at the same time we use window)
- `:sp` or `:split `: splits and puts the same buffer in two windows horizontally
- `:vs` or `:vsplit` or `Ctrl-w v` : splits and puts the same buffer in two windows vertically
- `Ctrl-w w` : cycle windows, `Ctrl-w {motion}` : cycles cursor according motion
- `:q` or `Ctrl-w q` : closes the split window
- `:on` or `:only` : closes all window except only currently active window
- `Ctrl-w {resize operation}` : can be used to resize windows : operations allowed (+ , -, _,|, =, <, >)
- `Ctrl-w J` or `Ctrl-w H`.. : can be move the cursor window around
- Similar to `:bufdo` we have `:windo` that executes some command to all windows

### Gvim and MacVim

- Why use graphical version of vim
  - leverage some features which are not available in command line version of vim
  - scrolling, text selection using mouse and copy-paste, etc.
- Vim usually maintains its own register systems for system clipboard, if you copy something in system, it can be accessed uses vims `“*` register and `“+` registers
- To make vim share system clipboard rather than using its own system `:set clipboard=unnamedplus` (operates on `+` register, for only using `*` register use `:set clipboard=unnamed`
- `commandKey+v` : works in MacVim because it behind the scenes pastes the `*` register using  `“*gP`
- gvimrc file is used to apply some specific settings to gvim versions.
  - `:set gfn=*` : font-selector for gvim



---

## File: vim/practical_vim/index.md

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







---

## File: vim/vimrc.md

## Vimrc Files

My dotfiles : [Link](https://raw.githubusercontent.com/mightyjoe781/.dotfiles/master/vim/.vimrc)

````.vimrc
"---------------------------------------------------------------------
" File     : .vimrc
" Purpose  : config file for vim
" Revision : 210419
" License  : MIT
" Author   : smk
"---------------------------------------------------------------------
"
" Basic Config

set nocompatible

syntax on
set noerrorbells visualbell t_vb=
" tab characters that are 4-spaces-wide
set tabstop=4 softtabstop=4
" indent to corresponding single tab
set shiftwidth=4
set expandtab
set smartindent
set nu
set nowrap
set smartcase
set noswapfile
set nobackup
set undodir=~/.vim/undodir
set undofile
" incremental search
set incsearch

set textwidth=70 
set colorcolumn=72
highlight ColorColumn ctermbg=0 guibg=lightgrey

set backspace=indent,eol,start
set encoding=utf-8
" Disable the default Vim startup message.
set shortmess+=I

" Show relative line numbers
set number 
set relativenumber

" shows status bar below
set laststatus=2
set statusline=%-4m%f\ %y\ \ %=%{&ff}\ \|\ %{&fenc}\ [%l:%c]

" By default, Vim doesn't let you hide a buffer (i.e. have a buffer
" that isn't shown in any window) that has unsaved changes.  This is
" to prevent you from forgetting about unsaved changes and then
" quitting e.g. via `:qa!`. We find hidden buffers helpful enough to
" disable this protection. See `:help hidden` for more information on
" this.
set hidden

" This setting makes search case-insensitive when all characters in
" the string being searched are lowercase. However, the search becomes
" case-sensitive if it contains any capital letters. This makes searc
" -hing more convenient.
set ignorecase 
set smartcase

" Unbind some useless/annoying default key bindings.
nmap Q <Nop> 

" 'Q' in normal mode enters Ex mode. You almost never want this.

" mouse support enable
set mouse+=a 
filetype plugin indent on " enable file type detection
set autoindent
" open new split panes to right and bottom, which feels more natural
set splitbelow 
set splitright
" remove arrow keys
nnoremap <Left>  :echoe "Use h"<CR> 
nnoremap <Right> :echoe "Use l"<CR> 
nnoremap <Up>    :echoe "Use k"<CR> 
nnoremap <Down>  :echoe "Use j"<CR>
" ...and in insert mode
inoremap <Left>  <ESC>:echoe "Use h"<CR> 
inoremap <Right> <ESC>:echoe "Use l"<CR> 
inoremap <Up>    <ESC>:echoe "Use k"<CR> 
inoremap <Down>	 <ESC>:echoe "Use j"<CR>

" quicker window movement
nnoremap <C-j> <C-w>j 
nnoremap <C-k> <C-w>k 
nnoremap <C-h> <C-w>h
nnoremap <C-l> <C-w>l

"--------------------------------------------------------------------
" Basic-Config 2

" common typos
command! -bang Q q<bang>
command! -bang W w<bang>

set tags=./tags;/ 
map <A-]> :vsp <CR>:exec("tag ".expand("<cword>"))<CR>

"---------------------------------------------------------------------
" Plug Config

" Install vim-plug if not found
if empty(glob('~/.vim/autoload/plug.vim'))
  silent !curl -fLo ~/.vim/autoload/plug.vim --create-dirs
    \ https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
endif

call plug#begin('~/.vim/plugged')

" Utilities

Plug 'jremmen/vim-ripgrep'
Plug 'tpope/vim-fugitive'
" original ctrp is not maintained anymore
Plug 'https://github.com/ctrlpvim/ctrlp.vim'
" Requires vim built with python 3.7+
" Plug 'lyuts/vim-rtags'
Plug 'mbbill/undotree'

" Themes
Plug 'morhetz/gruvbox'
" Plug 'altercation/vim-colors-solarized'

" Syntax and AutoCompletion
Plug 'scrooloose/syntastic'
Plug 'leafgarland/typescript-vim'
" YCM requires python3.8 and cmake
" Plug 'valloric/YouCompleteMe', { 'do': './install.py --clang-completer --system-libclang --gocode-completer' }


call plug#end()

colorscheme gruvbox
set background=dark

if has("autocmd")
    au BufNewFile,BufRead *.sgml,*.ent,*.xsl,*.xml call Set_SGML()
    au BufNewFile,BufRead *.[1-9] call ShowSpecial()
endif " has(autocmd)
````



---

