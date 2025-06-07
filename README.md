# Movie Recommendation Telegram Bot

A simple and interactive Telegram bot that recommends movies or series based on user input. The bot uses **OpenAI's GPT-4** to suggest movies according to user mood and preferences. It also tracks the active users and can show the number of users who have interacted with the bot.

---

## Features

* 🎬 **Movie Recommendations**: Users can request movie suggestions based on their mood or preferences.
* 🔁 **No Duplicate Suggestions**: The bot ensures that the same movie is not recommended twice in a session.
* 🧑‍🤝‍🧑 **User Count Tracking**: The bot keeps track of the number of active users interacting with it.
* ❓ **Help Commands**: The bot provides help messages for users, including basic commands and subscription info.
* ⚠️ **Handles Unrelated Queries**: The bot will politely ask the user to provide a movie request if they send an unrelated message.
* 🧠 **Smart Conversation Memory**: The bot keeps track of the conversation history to understand requests better and provide more accurate recommendations.

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/hamy-rah/Cinphile.git
   cd Cinphile
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:

   On Windows:

   ```bash
   .\.venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` does not exist, you can manually install the dependencies:

   ```bash
   pip install openai python-telegram-bot httpx
   ```

5. **Set up your environment variables**:

   * Create a `.env` file in the root directory of the project and add your **Telegram Bot API token** and **OpenAI API key**:

   ```bash
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   OPENAI_API_KEY=your_openai_api_key
   ```

   Or directly in the code (but be sure to keep your keys safe).

---

## Usage

1. **Run the bot**:

   After setting up the environment, you can run the bot with:

   ```bash
   python bot.py
   ```

2. **Commands**:

   * `/start`: Starts the conversation and greets the user.
   * `/user_count`: Displays the number of active users who have interacted with the bot.
   * **User interaction**: The user will be prompted to enter their movie preferences, and the bot will recommend movies based on the input.

---

## How it Works

1. **Movie Recommendation**: The bot uses **OpenAI GPT-4** to generate movie suggestions based on user input. The model is designed to interpret various user moods and preferences, offering recommendations accordingly.

2. **Tracking Active Users**: The bot tracks users who have interacted with it and saves their user IDs in a JSON file. This allows the bot to provide a count of the total active users.

3. **Preventing Duplicate Suggestions**: Each user has a history of recommended movies. The bot ensures that the same movie isn't suggested twice in a single session.

4. **Conversation Memory**: The bot keeps a short-term memory of the conversation to offer better recommendations and adjust to user requests (e.g., "I've seen that movie" or "Suggest something else").

---

## Contributing

1. **Fork the repository**: Create a personal copy of the project by forking this repository.
2. **Clone the repository**: Clone your fork to your local machine.
3. **Create a new branch**: Create a branch for your changes (e.g., `git checkout -b feature-name`).
4. **Make your changes**: Modify the code or add new features.
5. **Commit your changes**: Commit the changes with a clear message (`git commit -m "Add new feature"`).
6. **Push your changes**: Push the changes to your fork (`git push origin feature-name`).
7. **Create a pull request**: Submit a pull request to the main repository with a description of your changes.




