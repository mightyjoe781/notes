## RCLONE

Rclone is a command-line program to manage files on cloud storage. Its feature rich and cross platform, excellent for writing scripts which stays longer than locking with a specific cloud vendors cli solution.

Users call rclone *The Swiss army knife of cloud storage*, and *Technology indistinguishable from magic*.

What I like about rclone is that is vendor lockin proof and we can apply encryption, compression, chunking, hashin and joining all costly operation for free. rclone works on all OS, be it linux, windows or freeBSD.

### Installing rclone

````bash
# on macOS
brew install rclone
# on linux
sudo apt-get install rclone
````

**[Note] : If you are using rclone and same config on various system, try to remain on same version of rclone.**

### Setup rclone

````bash
rclone config
````

- you will need to setup a remote for each cloud vendor you wish to add.
- proceed with some remote name then select your cloud vendor.
- then you will need to authenticate your rclone using token to access cloud vendor’s storage.
    - GUI System : If you have some browser, then u can use auto generate token and follow the link provided by cli
    - Headless System : In case of headless system since there is no browser what you will need to create token on some another system and add it to the headless system.

