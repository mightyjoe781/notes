### Fixes

Universal Clipboard not working correctly even when handoff is enabled and both iphone and macbook are on same network

````bash
defaults write ~/Library/Preferences/com.apple.coreservices.useractivityd.plist ClipboardSharingEnabled 1
````

Above command explicity enables it. Sometimes due to glitch its possible copy work in one direction then just restart the macbook.