
# Habbify

## The Idea
Habbify is a small gamified habit tracking prototype designed to help users build positive habits. It incorporates elements of gamification, such as earning experience points (EXP) and collecting eggs to hatch birds, to motivate users to track and progress their habits consistently.

### Features
- **Create New Habits:** Users can create various types of habits, including everyday habits, habits to be completed a certain number of times per week, per month, or per year.
- **Track Habit Progress:** Users can track the progress of their habits, allowing them to monitor their consistency and improvement over time.
- **Earn EXP:** Users earn experience points (EXP) for progressing and completing their habits. EXP serves as a measure of their overall progress and commitment.
- **Level Up:** As users accumulate EXP, they level up, unlocking new features and rewards.
- **Grow Your Own Forest:** Users can grow their own virtual forest by hatching birds from collected eggs. Each bird represents a milestone in the user's habit journey.

### Current To-Dos
- ~~Creating Habit System~~
  - ~~Creating a Habit~~
  - ~~Track the Habit progression~~
- ~~Change is_complete~~
  - ~~Should track the timespan according to the selected frequency~~
  - ~~No need to "clear" current habits after a period of time to be able to track again~~
- ~~Showing the EXP~~
  - ~~The total number~~
  - ~~The amount earned when progressing~~
  - ~~The amount earned when creating a new one~~
- ~~Add Basic Functions for Birds and Egg Collection~~
  - ~~Gain Eggs when completing a habit~~
  - ~~Level all eggs when gaining EXP~~
  - ~~Hatch birds when a threshold is reached~~
- Change the way Eggs and Birds Work
  - You start with a one random Stage one Bird
    - ~~Birds can be feeded to gain a stage~~
    - ~~if a birds reaches stage 3 its "fully grown" and therefore letf in your Forest~~
      - ~~this bird will give 3 options of eggs you can choose from~~ (crrently 2)
      - ~~an Egg still progresses as you gain exp~~
    - There are other ways to gain new Eggs
      - Creating Daily Streaks
      - complete X Habits in one day etc...
- Getting "Better" Eggs with Higher User Level
  - Need at least 2 more eggs to hold different birds to collect
    - Therefore, 2 more egg icons needed
    - And 3-4 more bird images
  - Implement a function that can pick an egg (better egg probability scales with user level)
    - New eggs always start at a 10% chance and increase by 10% per level
  - The egg model needs a level threshold to track unlocking
- Update Habits
  - Classic update view
- Detail Habit View
  - Basic information (name, frequency, target, progression, is_complete)
  - History of completion and earned EXP

**Note:** For this prototype, the main focus is on the EXP as the primary motivator for habit tracking. Other features are designed to complement and enhance the user experience.



## Adam's Code Jam
This code was created in early 2024 for [Adam's Code Jam](https://jam.adamlearns.com/).
