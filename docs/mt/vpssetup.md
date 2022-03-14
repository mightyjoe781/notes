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

Note : For Postgresql Support in server, it required to be installed in the VPS beforehand.

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