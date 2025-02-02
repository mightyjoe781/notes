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

