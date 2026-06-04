# 👾 Homeworkimon

> **Transform your homework into monster-evolving power!** 
> Homeworkimon is a gamified educational web application built with Streamlit. Submit your school assignments, earn XP evaluated by an AI, and evolve your subject-specific avatars while tracking your real-life skills.

## ✨ Key Features

This MVP was built following a comprehensive 5-Sprint Agile methodology, encompassing over 70 User Stories.

*   **🏠 Dashboard:** Get a quick overview of your top 3 active subjects (your "Team") with dynamic progress bars[cite: 5]. Track your daily login Streaks[cite: 5] and complete randomly generated Daily Quests[cite: 5].
*   **📝 Habit Hub:** The core submission engine. Select a subject, set a perceived difficulty[cite: 5], paste your teacher's instructions, and upload your work (PDF/TXT)[cite: 5]. The AI evaluates your effort, grants XP, and distributes skill points[cite: 5].
*   **🐉 Homidex & Profile:** A complete collection gallery. Discover your unlocked monsters, view mysterious silhouettes of unworked subjects[cite: 5], and unlock achievements/badges based on your milestones[cite: 5]. You can also export your Player Card and data[cite: 5].
*   **🌳 Skill Tree:** An interactive Business Intelligence dashboard featuring a Plotly Spider/Radar chart[cite: 5] that dynamically deforms based on 8 core skills (Logic, Creativity, Structure, etc.). It includes infinite polynomial leveling and a timeline of your recent activity[cite: 5].

## 🛠️ Tech Stack

*   **Frontend & UI:** Streamlit (Python) - Utilizing the native multi-page navigation architecture[cite: 5].
*   **Data Visualization:** Plotly & Pandas.
*   **Database:** Local JSON file (`database.json`) managed via native Python dictionaries.
*   **AI Engine:** Currently mocked for the MVP, ready to be plugged into OpenAI/Gemini APIs.

## 🚀 Installation & Setup

Follow these steps to run Homeworkimon on your local machine.

**1. Clone the repository**
```bash
git clone [https://github.com/ranelden/homeworkimon.git](https://github.com/ranelden/homeworkimon.git)
cd homeworkimon