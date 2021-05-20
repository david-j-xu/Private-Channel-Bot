# Private Channel Bot
*By david*

This creates a Discord bot that creates private text channels for voice channels that currently exists. Allows the creation for one private channel per person, with optional persistency.

---------------------------

## Set Up
Make sure to install the necessary dependencies as listed in the requirements file.

Create a `.env` file in this directory, with the elements as follows:
```
DISCORD_TOKEN={Your Discord Bot Token}
CHANNEL={Channel to listen to}
```
Your bot should be connected to the server you wish to run the bot on, and it should run smoothly provided the bot is set up correctly.

Sufficient permissions are given by the permissions integer `2148007025`

## Commands

| Command | Description |
|---|---|
|`$create_channel`|Creates a private channel. Limit one private channel per user|
`$delete_channel` | deletes your channel |
`$update_channel` | adds people in your current call to the channel |
`$help` | Prints this |

