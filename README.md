**Introduction**

# NexxClone Documentation

Welcome to the documentation for NexxClone, a Python library for Discord server cloning. This documentation will guide you through the installation, usage, and features of NexxClone.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

**Installation**

# Installation

To get started with NexxClone, you'll need to install it using `pip`. Make sure you have Python 3.6 or higher installed.

```bash
pip install nexxclone
```

**Usage**

# Usage

To use NexxClone, you'll need a Discord bot token and the IDs of the source and destination servers. Follow the example below to get started:

```python
from nexxclone import Clone
import discord

def main():
    # Get user input
    token = input('Your Token > ')
    input_guild_id = input('Your Source Server ID > ')
    output_guild_id = input('Your Destination Server ID > ')

    # Initialize the Discord client
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f"Logged in as: {client.user}")
        print("Cloning Server")

        # Get source and destination guilds
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))

        # Prompt user for cloning options
        all_in_one = input('Do you want to perform an all-in-one clone? [y/n] > ').lower() == 'y'
        
        if all_in_one:
            await Clone.all(guild_from, guild_to)
        else:
            # Perform individual cloning steps
            await Clone.roledelete(guild_to)
            await Clone.chdelete(guild_to)
            await Clone.rolecreate(guild_to, guild_from)
            await Clone.catcreate(guild_to, guild_from)
            await Clone.chcreate(guild_to, guild_from)
            await Clone.guedit(guild_to, guild_from)

        clone_template = input('Do you want to clone the template of the server? [y/n] > ').lower() == 'y'
        if clone_template:
            await Clone.gutemplate(guild_to)

        print("Cloning completed. Exiting in 5 seconds.")
        await asyncio.sleep(5)
        exit()

    # Run the bot with the provided token
    client.run(token, bot=False)

if __name__ == "__main__":
    main()
```

**Examples**

# Examples

Here are some examples to demonstrate the usage of NexxClone:

- **Basic Server Clone**
  ```python
  await Clone.all(guild_from, guild_to)
  ```

- **Customized Clone**
  ```python
  await Clone.roledelete(guild_to)
  await Clone.chdelete(guild_to)
  await Clone.rolecreate(guild_to, guild_from)
  await Clone.catcreate(guild_to, guild_from)
  await Clone.chcreate(guild_to, guild_from)
  await Clone.guedit(guild_to, guild_from)
  ```

**Contributing**

# Contributing

If you want to contribute to NexxClone, feel free to submit issues or pull requests on our [GitHub repository](https://github.com/noritem/nexx_clone). We welcome any improvements, bug fixes, or new features.

**License**

# License

NexxClone is licensed under the MIT License. See the [LICENSE](https://github.com/noritem/nexx_clone/blob/main/LICENSE) file for details.

Thank you for using NexxClone!

Feel free to customize this template according to your project structure and specific details. Also, make sure to replace the placeholder URLs and GitHub repository links with your actual project information.


# Contributing
Feel free to contribute by opening issues or creating pull requests. Your feedback and suggestions are welcome!
