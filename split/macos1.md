# Macos Notes - Part 1
Generated on: 2025-06-01 16:46:27
Topic: macos
This is part 1 of 1 parts

---

## File: macos/index.md

### Installing yt-dlp

````bash
# install yt-dlp
brew install yt-dlp ffmpeg fprobe

# put all your youtube links in a file separated by new file
echo "SOME_YT_URL" >> playlist.txt

# get cookies.txt file, install cookies.txt mozilla extension
# login into yt and run the extension to download the file or
yt-dlp --cookies cookies.txt --cookies-from-browser firefox

# downloading entire list of videos
yt-dlp --cookies cookies.txt -a playlist.txt

# downloading a playlist

````

### Fixes

Universal Clipboard not working correctly even when handoff is enabled and both iphone and macbook are on same network

````bash
defaults write ~/Library/Preferences/com.apple.coreservices.useractivityd.plist ClipboardSharingEnabled 1
````

Above command explicity enables it. Sometimes due to glitch its possible copy work in one direction then just restart the macbook.

---

