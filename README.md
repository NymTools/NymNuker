# NymNuker

A Discord server management tool for educational purposes, fully coded by NymTools.

## Features and Functionality

NymNuker provides a range of functionalities for Discord server management, including:

*   **Channel Management:**
    *   Delete all channels in a server.
    *   Create multiple channels with a specified name.
    *   Rename all channels in a server.
*   **Role Management:**
    *   Delete all roles in a server.
    *   Create multiple roles with a specified name.
    *   Rename all roles in a server.
*   **Member Management:**
    *   Ban all members in a server.
    *   Kick all members in a server.
    *   Unban all members in a server.
    *   Change the nickname of all users in a server.
    *   Remove the nickname of all users in a server.
    *   Direct message all members.
*   **Server Management:**
    *   Change the server name.
    *   Change the server icon.
    *   Remove all emojis.
*   **Spamming:**
    *   Webhook spam in all channels.
    *   Message spam in all channels.
*   **Nuking:**
    *    Comprehensive server destruction, channel and role deletion, spam creation, with renaming functionality.

## Technology Stack

*   Python 3.x
*   `requests` library for making HTTP requests
*   `threading` library for concurrent execution
*   `asyncio` library for asynchronous operations (main function)
*   `datetime` library to print timestamp
*   `json` library to handle JSON data

## Prerequisites

Before running NymNuker, ensure you have the following:

*   Python 3.x installed on your system.
*   The `requests` library installed. You can install it using pip:

    ```bash
    pip install requests
    ```

## Installation Instructions

1.  Clone the repository to your local machine:

    ```bash
    git clone https://github.com/NymTools/NymNuker.git
    cd NymNuker
    ```

2.  Install the required dependencies:

    ```bash
    pip install requests
    ```

## Usage Guide

1.  Run the `NymNuker.py` script:

    ```bash
    python NymNuker.py
    ```

2.  The script will prompt you to enter your Discord bot token:

    *   Enter your bot token when prompted. Make sure the bot has the necessary permissions in the Discord server you intend to manage (e.g., `Administrator` permission).

3.  The script will display a list of available servers (guilds) the bot is a member of. You can select a server by entering its ID or the corresponding number from the list.

4.  After selecting a server, the main menu will be displayed, offering various management options.

5.  Choose an option by entering the corresponding number and following the prompts.

### Example Usage

*   To delete all channels in the selected server, enter `01` and press Enter.
*   To create 10 channels named "test-channel", enter `05`, then enter "test-channel" when prompted for the channel name, and then `10` when prompted for the amount.

### Configuration Details

*   **Bot Token:**  The bot token is essential for authenticating the script with the Discord API. You can obtain a bot token from the Discord Developer Portal.
*  **Image path (for changing guild icon):**  The image file needs to be a PNG image. This path has to be a valid path in your filesystem.

## API Documentation

The script interacts with the Discord API v9.  Key API endpoints used include:

*   `GET /users/@me` : Retrieves the user's information.
*   `GET /users/@me/guilds` : Retrieves the guilds the user is in.
*   `GET /guilds/{guild_id}`: Retrieves guild information.
*   `GET /guilds/{guild_id}/channels` : Retrieves the channels in a guild.
*   `GET /guilds/{guild_id}/roles` : Retrieves the roles in a guild.
*   `GET /guilds/{guild_id}/members` : Retrieves the members in a guild.
*   `GET /guilds/{guild_id}/bans` : Retrieves the banned users in a guild.
*   `DELETE /channels/{channel_id}` : Deletes a channel.
*   `DELETE /guilds/{guild_id}/roles/{role_id}` : Deletes a role.
*   `PUT /guilds/{guild_id}/bans/{user_id}` : Bans a user.
*   `DELETE /guilds/{guild_id}/members/{user_id}` : Kicks a user.
*   `POST /guilds/{guild_id}/channels` : Creates a channel.
*   `POST /guilds/{guild_id}/roles` : Creates a role.
*   `DELETE /guilds/{guild_id}/bans/{user_id}` : Unbans a user.
*   `POST /channels/{channel_id}/webhooks` : Creates a webhook.
*   `POST /channels/{channel_id}/messages` : Sends a message to a channel.
*   `PATCH /channels/{channel_id}` : Modifies a channel.
*   `PATCH /guilds/{guild_id}/roles/{role_id}` : Modifies a role.
*   `PATCH /guilds/{guild_id}/members/{user_id}` : Modifies a member (nickname).
*   `PATCH /guilds/{guild_id}` : Modifies a guild.
*   `DELETE /guilds/{guild_id}/emojis/{emoji_id}`: Deletes an emoji.
*   `POST /users/@me/channels`: Creates a direct message channel with a user.

## Contributing Guidelines

This project is for educational purposes and was fully coded by NymTools. Contributions are not expected at this time.  However, if you have suggestions or improvements, you can open an issue on the GitHub repository.

## License Information

No license is specified for this project. All rights are reserved by NymTools.

## Contact/Support Information

This project was fully coded by NymTools. For any inquiries, please open an issue on the [GitHub repository](https://github.com/NymTools/NymNuker).