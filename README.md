# @ConstAssembly Twitter Bot

A [twitter bot](https://twitter.com/ConstAssembly) that tweets a sentence from the Indian Constituent Assembly Debates every 10 minutes.

## Development Docs

The bot resides in `bot.py` and uses the Tweepy library to tweet text. The
bot depends on the following files:

1. `data.txt` - This file contains the raw text, which is used by the bot.
2. `last_line.txt` - This file is the memory of the bot. This is used so that the bot can dump its state to disk between each run. The bot currently runs as a cron job. Eg.
```
12
0
```
Where line 0 represents the row and line 1 represents the column in the data.txt file.

3. `.env` - This file contains the secrets required by the bot, such as Twitter API keys.

### Getting Started

You can get started by cloning this repository.

``` sh
git clone git@github.com/rhnvrm/ConstAssemblyBot
```

After this, you can install dependencies using:

``` sh
cd ConstAssemblyBot
pipenv shell
pipenv install
```

You can now, install a cronjob like this:

```cronjob
*/10 * * * * cd $HOME/apps/ConstAssemblyBot && /usr/local/bin/pipenv run python bot.py
```
