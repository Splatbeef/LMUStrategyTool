# LMUStrategyTool

LMUStrategyTool, as the name implies, is a tool to help you with your LMU strategies. In addition, it also helps you keep track of your best laptimes.

## Strategies
On the strategy page, you can fill in all race details, and calculate some preset strategies. These come with full stint plans, including the required fuel, fuel usage per lap, what lap you pit on, etc. (also includes VE needed, usage, and the fuel ratio for VE-enabled cars). There will also be a simple quali plan, detailing how much fuel or VE you need based on how long qualifying is.
Estimation for the number of laps is quite agressive, assuming maximum pace. If you know the race will be shorter, or have a rough idea of the leader pace, there are overrides to use. The calculator does not know if you are the lead class or not, so be aware that as a bottom class, you might need to do an extra lap if the leader is behind you on track when the clock hits 00:00. In the future, the lap count calculations will be refined to be more accurate.

### Before you start calculating
- Make sure you have added the fuel usage of that car/track combination
- Make sure the reference times are imported
Without these, the calculator will not work!

### Current strategy presets
- Push: Always push flat out. Will round down from the number of laps you can do with your fuel usage, and make full stints. The final stint is then the remaining laps. If the race is 62 laps, and you do 18.7 laps on a full tank, this strategy will have you do 18, 18, 18, and 8 laps.
- Plus 1: Same as push, but every stint is rounded up. This requires some fuel consciousness, though usually due to traffic and tire wear this goes pretty automatically. With the 62 lap race again, on plus one you do 19, 19, 19, and 5 laps
- Plus 2: One more lap per stint than Plus 1. In the example: 20, 20, 20, and 2 laps
- Save: Tries to do the race in one less stint than the push strategy. In the 62 lap race, since push has 4 stints, save divides it into 3: 20, 21, and 21 and gives you the fuel usage required. If some stints require more saving, the first stint will always be shorter, so you can worry about navigating the field instead of needing to save extra fuel. It always tries to give you this option, even if it might be almost impossible to hit the fuel number. Always evaluate the plans before choosing!

Sometimes, there will be overlap. If the race was 57 laps, with the same usage, both Plus One and Save would have you do 19, 19, 19, though they come there in different ways

## Laptimes
You can add your personal best laptimes to the add, to quickly see how far you are off the reference times. You can add a separate PB for race, qualifying, and practice. In the settings you can choose to split practice up into race practice and qualifying practice.

Reference laptimes are collected from GO Setups at https://gosetups.gg/laptimes-sheet/. 
By default, these will sync the first time you start the app on a given day. This can be turned off in the settings. You can refresh them manually on the reference times page. 
A small multiplier (default: 0.5%) is added to make these perfect hotlaps resemble qualifying laps. This can be adjusted in the settings.

## Cars & Tracks
All cars and tracks from 1.4 are seeded automatically. 
New tracks will be collected from the laptime sheet automatically. New cars will need to be added manually, or you wait for an update from me. You'll get a popup when syncing reference times to identify any new cars or tracks. You can give them your own preferred display name.

## Future
These are some plans for the future, which I'm pretty sure I will implement at some point:
- Tire changes
- Custom plan builder: allowing you to make stints yourself (or copy from a preset and edit) and have the resulting fuel numbers
- Adding more strategy presets (suggestions welcome)
- Refining the lap count calculations

## Disclaimer of AI Use
All code in this app was written by myself. AI was used during development for the following purposes:
- Organize what modules I needed to write and what they need to accomplish
- Check my code for potential mistakes/bugs/issues
- Suggest possible approaches (conceptual) for implementing specific things
