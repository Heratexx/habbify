
# Habbify

## The Idea
Habbify is a small gamified habit tracking prototype designed to help users build positive habits. It incorporates elements of gamification, such as earning experience points (EXP) and collecting eggs to hatch birds, to motivate users to track and progress their habits consistently.

### Features
- **Create New Habits:** Users can create various types of habits, including everyday habits, habits to be completed a certain number of times per week, per month, or per year.
- **Track Habit Progress:** Users can track the progress of their habits, allowing them to monitor their consistency and improvement over time.
- **Earn EXP:** Users earn experience points (EXP) for progressing and completing their habits. EXP serves as a measure of their overall progress and commitment.
- **Level Up:** As users accumulate EXP, they level up, unlocking new features and rewards.
- **Grow Your Own Forest:** Users can grow their own virtual forest by hatching birds from collected eggs. Each bird represents a milestone in the user's habit journey.

### Completed To-Dos
- **Habit System Implementation**
  - Created a habit tracking system
  - Implemented habit progression tracking
- **Enhancements in Completion Tracking**
  - Adjusted to track the timespan according to the selected frequency
  - Eliminated the need to clear current habits for re-tracking
- **Experience Points (EXP) Display**
  - Displayed the total EXP number
  - Showed EXP earned from habit progression
  - Showed EXP earned from creating new habits
- **Basic Features for Birds and Egg Collection**
  - Enabled egg collection upon completing a habit
  - Linked egg leveling to EXP gains
  - Implemented bird hatching upon reaching EXP thresholds
- **Modifications to Eggs and Birds Mechanics**
  - Initialized users with a random Stage one Bird
  - Allowed feeding birds to gain stages until fully grown at Stage 3, then left in the user's Forest
    - Provided 3 egg options from fully grown birds
    - Continued egg progression with EXP gains
    - Introduced alternative methods to gain new Eggs (e.g., Daily Streaks, completing multiple habits in one day)
- **Improved Egg Acquisition with User Level**
  - Required additional eggs for diverse bird collection
  - Added more egg and bird icons and images
  - Developed a function for selecting eggs with probabilities scaling with user level
  - Adjusted egg model for level-based unlocking

### To-Do Cleanup
- **Forest and Egg Template Enhancements**
  - Design a dedicated forest template
    - Make birds non-clickable
    - Ignore stage in the forest view
    - Consider adding popup descriptions
  - Upgrade egg template for better presentation
    - Avoid list elements; display eggs side-by-side
    - Use a progress bar showing percentage rather than numbers
- **New Habits Creation Template Improvement**
  - Apply pastel colors to match the overall theme
- **Additional User Guidance**
  - Potentially add more informational modals about EXP and rewards
- **Deployment and Final Setup**
  - Successfully deployed to a test environment
  - Prepare for final launch
    - Create 3 demo users with initial resources (a start bird and 1 food)
    - Include some historical data to enhance completion stats visualization

## Adam's Code Jam
This code was created in early 2024 for [Adam's Code Jam](https://jam.adamlearns.com/).
