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

