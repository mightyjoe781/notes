### Patches (Optional)

#### Stamina mod Texture Fix in Multicraft (Optional)

If you are not using the default built-in hunger mod and are instead using the stamina mod, there may be some misalignment of the hunger and health bars.

To fix the issue, follow these steps:

````bash
# Navigate to multicraft installation folder
cd multicraft/builtin/games/
rm statsbar.lua
wget https://raw.githubusercontent.com/minetest/minetest/stable-5/builtin/game/statbars.lua
# restart the server
````

Why use the stamina mod over the default hunger mod? Stamina mod integrates well with Mesecons and related virtual player mods, which will save a lot of time debugging crashes.
