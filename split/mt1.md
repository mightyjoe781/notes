# Mt Notes - Part 1
Generated on: 2025-06-01 14:34:33
Topic: mt
This is part 1 of 1 parts

---

## File: mt/index.md

## Minetest

Minetest is a free and open-source sandbox video game and game creation system developed by a team of volunteers, with significant contributions from the community.It was created by Perttu Ahola, and released on Web in November 2010.

Minetest is programmed in C++ using the Irrlicht Engine. Minetest provides an API for users to create their own games and mods written in Lua.

#### Server

[Creating a Minetest Server](server.md)

[Setting up a server for Minetest](vpssetup.md)

[Server Scripts](scripts.md)

#### Resources

- [Minetest: Official Website](https://www.minetest.net/)
- [Minetest API Documentation](https://minetest.gitlab.io/minetest/)
- [Official Forum](https://forum.minetest.net)

- [Minetest Modding Book](https://rubenwardy.com/minetest_modding_book/en/index.html)

---

## File: mt/scripts.md

### Patches (Optional)

#### Stamina mod Texture Fix in Multicraft (Optional)

If you are not using default inbuilt hunger mod, and instead using stamina mod. There may be some misalignment of hunger and health bar.

To fix the issue follow the steps

````bash
# Navigate to multicraft installation folder
cd multicraft/builtin/games/
rm statsbar.lua
wget https://raw.githubusercontent.com/minetest/minetest/stable-5/builtin/game/statbars.lua
# restart the server
````

Why would you wanna use the stamina mod over default hunger mod. Stamina mod is well integrated with mesecons and related virtual player type mods and mostly will save you a lot of time fixing the crashes.

#### Texture patch (Optional)



---

## File: mt/server.md

### Minetest Server

Minetest is an open source voxel game engine.It requires a game which utilises engine API to provide a gameplay.By default it ships with a devtest game which is mostly used for development puporses. A better playable game called as Minetest Game is also available.

#### Considerations

Before creating a server there are some question that should be considered.

- Cost of Server
- Cost of Time
- Dedication to fix server crashes
- Updating mods and fixing mods
- Managing Server
- Staff for Server
- Longevity of Server

##### Minimum Requirements

For a lightly modded server with decent traffic (10 users) a 2GB RAM/ 50GB Storage should be fine.

##### Hosting Solutions

There are few hosting providers in minetest community which provide very cheap hosting solution along with support for fixing the issues.

- [Edgynet](https://edgy1.net) : Costs $8 USD/month
- [MineCity](https://minecity.online/) : Costs $5 USD/month

#### Minetest’s Forks & Games

##### **Multicraft**

Created by Maksym as an attempt to develop a “ready-made” game that has a nice interface and doesn’t require the player to have any development skills and just wants to play.

Most of famous servers currently run on multicraft because of availability of players and support for both 0.4 and 5.x clients. Most of mods may require little bit of tweaking for working with multicraft.

##### **Mineclone** 2 Game

Created by Wuzzy, as the name suggests game attempts to provide a gameplay similar to MineCraft. It has really come quite far and its very stable.

##### Final Minetest

Created by Robert Kiraly, provides improvements to original minetest game in terms of speed and completeness. It has been used as an education tool for school in Italy.

Some quite interesting feature offered are free hosting (limited), P2P server lists, 64x64 skins.

#### Alternate Free Hosting Solutions

- Old personal computer as a server
- Raspberry Pi

---

## File: mt/vpssetup.md

### MultiCraft Server Setup

#### Dependency

For Debian/Ubuntu users:

```bash
sudo apt install g++ make libc6-dev libirrlicht-dev cmake libbz2-dev libpng-dev libjpeg-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-gnutls-dev libfreetype6-dev zlib1g-dev libgmp-dev libjsoncpp-dev git postgresql postgresql-contrib libpq-dev postgresql-server-dev-all luajit libncurses5-dev libluajit-5.1-dev doxygen libcurl4-openssl-dev libleveldb-dev libzstd-dev
```

#### Build

Clone the source repository.

````bash
git clone --depth 1 https://github.com/MultiCraft/MultiCraft2.git
mv MultiCraft2 multicraft
cd multicraft
````

Adding a game to multicraft, you can add any game you want but minetest_game seems to be a fine choice considering lot of mods depend on it.

````
git clone --depth 1 https://github.com/minetest/minetest_game.git games/minetest_game
````

Irrlicht is not required for server only build.

````bash
cmake . -DRUN_IN_PLACE=1 -DBUILD_SERVER=1 -DBUILD_CLIENT=0\
				-DENABLE_POSTGRESQL=1 -DENABLE_CURSES=1 -DENABLE_LUAJIT=1\
				-DVERSION_EXTRA="smk" -DENABLE_SYSTEM_JSONCPP=1
				
make -j$(nproc)
````

#### Configuration

This is a good configuration settings for starting up a public server. Make changes accordingly.

````
bind_address = adv.edgy1.net
### General Server Settings ###
# Admin Name
name = smk
# Logs parameter - 0 = none, 1 = warning, 2 = action, 3 = info, 4 = verbose
debug_log_level = action
debug_log_size_max = 0
creative_mode = false
enable_damage = true
disallow_empty_password = true
default_stack_max = 64
max_users = 20
default_privs = interact, shout, fast, home, tp
enable_rollback_recording = true
enable_minimap = true

### SERVER AND PUBLIC INFORMATIONS ###
server_name = Adventure Time
server_description = Welcome to a world full of adventure where you make new friends,hatch dragons and fight lots of monsters. Join our discord: https://discord.gg/NQvCBhy9pu.
motd = Welcome to Adventure Time! Experience a survival server like never before.
server_url = https://adv.minetest.in/
server_announce = true
server_address = adv.edgy1.net
port = 30029
#pgsql_connection = host=db port=54414 user=smk password=somerandomstring dbname=smk_mc24

### MODS PARAMETERS ###
static_spawnpoint = 1810, 7, 1767
node_drop = false
item_collection = true
# enable_hunger = true
give_initial_stuff = true
initial_stuff = default:torch 64,default:pick_steel,default:axe_steel,default:apple 64
bones_mode = place
````

Save above config to `~/multicraft/multicraft.conf`.

#### Setup

By default all the worlds go into `~/multicraft/worlds/worldname/`. All the logs gets written into `~/multicraft/debug.txt` and config file read is `~/multicraft/multicraft.conf`.

For Installing mods we can either utilise `~/multicraft/mods/` or `~/multicraft/worlds/worldname/worldmods/`. Later is preffered because we can use same engine installation to host multiple worlds which use different modsets and we don’t have to define a `enable_modname=true` for every mod we install.

- World files : `~/multicraft/worlds/worldname`
- Logs files : `~/multicraft/debug.txt`
- Config files : `~/multicraft/multicraft.conf`

So Idea now is to redefine and make this structured for maintaining multiple worlds and its much easier to debug the server crashes when we have smaller log files with dates written on them rather than a long debug.txt file.

````bash
cd ~
mkdir -p logs config worlds
touch start.sh
chmod +x start.sh
````

Now copy following to `start.sh`

````bash
#!/bin/sh
if [ -z "$STY" ]; then exec screen -dm -S mc /bin/bash "$0"; fi
while sleep 3; do $HOME/multicraft/bin/multicraftserver --world $HOME/worlds/prismo --terminal --logfile $HOME/logs/`date +"%m%d"`.txt --config $HOME/config/prismo.conf; done
````

Above script attaches a screen session in behind and executes multicraftserver in it. To access screen session do `screen -rx`.To come back to console from screen session you can type `^ A + d`. See `screen(1)` man page for more details.

Replace `prismo` with appropriate server name.

---

