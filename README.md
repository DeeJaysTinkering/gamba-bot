# 🎰 Gamba Bot

A simple Discord bot for playing casino games with friends.

Gamba Bot was built as a quick capstone project to explore Python development and Discord bot functionality. Currently, the bot features **Blackjack**, with more casino games potentially coming in the future.

## 🎮 Features

- **Blackjack** — Play a classic game of blackjack directly through Discord.
- **Future expansion** — Additional casino games may be added in future updates.

## 📋 Prerequisites

Before running Gamba Bot, you'll need:

- [Python](https://www.python.org/downloads/) installed on your machine.
- A Discord account and a server where you have permission to add bots.
- A Discord bot token.
- The required Python dependencies.

## ⚙️ Setup and Installation

### 1. Create a Discord Bot

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and give your application a name.
3. Navigate to the **Bot** section and create your bot user if prompted.
4. Retrieve your bot token from the Bot settings.

**Important:** Keep your bot token private. Never commit it to a public repository or share it with anyone.

For more information, see the [official Discord developer documentation](https://discord.com/developers/docs/intro).

### 2. Clone the Repository

Clone this repository and navigate to the project directory:

```bash
git clone <YOUR_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

Replace the placeholders with your repository URL and directory name.

### 3. Configure Environment Variables

Create a `.env` file in the same directory as the bot's main Python file.

Add your Discord bot token:

```env
DISCORD_TOKEN=your_discord_bot_token
```

Replace `your_discord_bot_token` with your actual token.

Make sure `.env` is included in your `.gitignore` file so your credentials aren't accidentally uploaded to GitHub.

### 4. Install Dependencies

Install the required Python packages:

```bash
python -m pip install discord.py python-dotenv
```

Alternatively, if the repository contains a `requirements.txt` file, install all dependencies with:

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Bot

Once the dependencies and environment variables are configured, start the bot by running its main Python file:

```bash
python main.py
```

Replace `main.py` with the actual filename if your entry point is named differently.

If everything is configured correctly, the bot should connect to Discord and be ready to use.

## ☁️ Hosting and Deployment

Want to keep Gamba Bot running without leaving your computer on? You can deploy it to a cloud hosting service.

- [Heroku](https://www.heroku.com/) — Cloud application hosting.
- [Heroku Python Deployment Guide](https://devcenter.heroku.com/articles/getting-started-with-python) — Official guide to setting up and deploying Python applications.
- [Preparing a Codebase for Heroku Deployment](https://devcenter.heroku.com/articles/preparing-a-codebase-for-heroku-deployment) — Prepare an existing project for deployment.
- [Heroku Procfile Documentation](https://devcenter.heroku.com/articles/procfile) — Learn how to specify the command that starts your bot.

**Note:** A Discord bot typically runs as a persistent background process. For Heroku, you'll need to configure an appropriate process type, such as a worker, and set `DISCORD_TOKEN` as an environment config variable rather than relying on a local `.env` file. Check Heroku's current pricing and runtime options before deploying.

## 🛠️ Built With

- [Python](https://www.python.org/)
- [discord.py](https://discordpy.readthedocs.io/en/stable/) — Discord API wrapper for Python.
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Loads environment variables from a `.env` file.

## 📜 License

This project is licensed under [The Unlicense](https://unlicense.org/).

This software is released into the public domain. Anyone is free to use, modify, distribute, compile, sell, or otherwise share this software for any purpose, commercial or non-commercial, without restriction, to the extent permitted by law.

See the [LICENSE](LICENSE) file for the full license text.
