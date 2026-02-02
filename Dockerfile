FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# watchdog is required for hot reload
RUN pip install watchdog

COPY . .

# run the bot with auto-restart on file changes
CMD ["watchmedo", "auto-restart", "--patterns=*.py", "--recursive", "--", "python", "DiscordAIBot.py"]