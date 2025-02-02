# Chapter 4 : Working with Text And Buffer

#### Scrolling Through Output with Copy Mode

- To enable copy mode : `PREFIX [`
- To enable vi style movement add this line in config

````.tmux.conf
#enable vi keys.
setw -g mode-keys vi
````

#### Moving Quickly Through Buffer

- Utilize vi shortcuts like `g`, or `G` and `CTRL-b` or `CTRL-f`

#### Searching Through Buffer

- Use vi shortcuts like `/{pattern}` or for previous search `?{pattern}`

#### Copying and Pasting Text

- Go in copy mode and press `SPACE` and move cursor to end of line/word you want to copy and hit `ENTER`
- This copies contents into a paste buffer, to print its contents : `PREFIX ]`

#### Capturing a Pane

- To copy entire visible buffer contents : `PREFIX :capture-pane`

#### Showing and saving contents of buffer

- Use : `tmux show-buffer` then to save it `save-buffer buffer.txt`

#### Using Multiple Paster Buffers

By design, tmux stores a stack of paste buffers.

Now try copying multiple line in paste buffers and list buffers : `list-buffers`

By default : `PREFIX ]` always applies paste buffer 0, but we can use `choose-buffer` to select a buffer before pasting its content.

#### Remapping Copy and Paste Keys

Make the binding same as vim

````.tmux.conf
bind Escape copy-mode
bind-key -T copy-mode-vi v send -X begin-selection
bind-key -T copy-mode-vi v send -X copy-selection
unbind p
bind p paste-buffer
````

#### Working with Keyboard on Linux

- Install `xclip` : `sudo apt-get install xclip`

Now add following lines in tmux

````.tmux.conf
# Prefix Ctrl-C takes what's in the buffer and send to system clipboard via xclip
bind C-c run "tmux save-buffer - | xclip -sel clip -i"
````

To invoke it : `PREFIX CTRL-c`

We could also bind it to y key.

````.tmux.conf
# y in copy mode takes selection and send it to system via xclip
bind-key -T copy-mode-vi y send-keys -X copy-pipe-and-cancel "xclip -sel clip -i"
````

To make `PREFIX Ctrl-v` to paste buffers into tmux windows

````.tmux.conf
# prefix Ctrl-v fills tmux buffer from system clipboard via xclip, then pastes from buffer into tmux window
bind C-v run "tmux set-buffer \"$(xclip -sel clip -o)\";tmux paste-buffer"
````

#### Using macOS Clipoboard Commands

In MacOS there is already `pbcopy` and `pbpaste` to work with clipboard.

Inside of tmux you can execute : `tmux show-buffer | pbcopy`

or paste the contents of clipboard : `tmux set -buffer $(pbpaste); tmux paste-buffer`

````.tmux.conf
# Prefix Ctrl-C takes whats in the buffer and sends it to system clipboard via pbcopy
bind C-c run "tmux save-buffer - | pbcopy"

# y in copy mode takes selection and sends it to system clipboard via pbcopy
bind-key -T copy-mode-vi y send-keys -X coyp-pipe-and-cancel "pbcopy"

# prefix ctrl-v fills tmux buffer from clipboard via pbpaste then pastes from buffer into tmux window
bind C-v run "tmux set-buffer \"$(pbpaste)\"; tmux paste-buffer"
````

