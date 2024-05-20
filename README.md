# MongoDB Aggregation Bot

This repository contains a Telegram bot that performs aggregation of salary data stored in a MongoDB database. The bot uses the `aiogram` library for handling Telegram messages and `motor` for asynchronous interaction with MongoDB.

## Folder Structure

- `dump/sampleDB`: Contains the MongoDB sample database.

## Files

### aggregator.py

This script handles the aggregation of salary data.

#### Functions

- **generate_intervals(dt_from, dt_upto, group_type)**:

  - Generates time intervals based on the provided `group_type` (`hour`, `day`, `month`).

- **aggregate_salaries(dt_from, dt_upto, group_type)**:
  - Aggregates salaries within the specified date range and groups them by the specified `group_type`.

### bot.py

This script contains the Telegram bot implementation.

#### Handlers

- **command_start_handler(message: Message)**:

  - Responds to the `/start` command with a greeting message.

- **jsons_handler(message: Message)**:
  - Handles incoming JSON messages with aggregation parameters (`dt_from`, `dt_upto`, `group_type`), performs the aggregation, and returns the result.

#### Main Function

- **main()**:
  - Initializes and starts the Telegram bot.

### requirements.txt

Contains the list of dependencies required for the project.

- `aiogram`
- `python-dotenv`
- `motor`
- `python-dateutil`

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/mongodb-aggregation-bot.git
   cd mongodb-aggregation-bot
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Telegram Bot API token:

   ```env
   API_TOKEN=your_telegram_bot_api_token
   ```

5. Import the sample MongoDB database:

   ```bash
   mongorestore --db sampleDB dump/sampleDB
   ```

6. Run the bot:

   ```bash
   python bot.py
   ```

## Usage

1. Start a conversation with your bot on Telegram.

2. Send the `/start` command to the bot.

3. Send a JSON message with the aggregation parameters. Example:

   ```json
   {
     "dt_from": "2023-01-01T00:00:00",
     "dt_upto": "2023-01-31T23:59:59",
     "group_type": "day"
   }
   ```

4. The bot will respond with the aggregated salary data.

## License

This project is licensed under the [MIT License](LICENSE).
