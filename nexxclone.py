import discord
from colorama import Fore, init, Style
import os
from time import sleep
import pyperclip

# Initialize colorama for colored console output
init(autoreset=True)

# Helper functions for printing messages with specific formatting
def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} {message}')

def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')


# Class definition for the Clone operations
class Clone:
    # Method to delete roles in a guild
    @staticmethod
    async def roledelete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Deleted Role: {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Delete Role: {role.name}")

    # Method to create roles in a guild based on another guild's roles
    @staticmethod
    async def rolecreate(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        # Collect roles from the source guild (excluding "@everyone")
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]  # Reverse roles to maintain order
        # Create roles in the destination guild
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Created Role {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Role: {role.name}")

    # Method to delete channels in a guild
    @staticmethod
    async def chdelete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted Channel: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Channel: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable To Delete Channel: {channel.name}")

    # Method to create categories in a guild based on another guild's categories
    @staticmethod
    async def catcreate(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(f"Created Category: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Category: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable To Delete Category: {channel.name}")

    # Method to create text and voice channels in a guild based on another guild's channels
    @staticmethod
    async def chcreate(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_text.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    # If channel name starts with ticket- or ticket_ or ticket, don't create it
                    if channel_text.name.startswith("ticket-") or channel_text.name.startswith("ticket_") or channel_text.name.startswith("ticket"):
                        pass
                    else:
                        new_channel = await guild_to.create_text_channel(
                            name=channel_text.name,
                            overwrites=overwrites_to,
                            position=channel_text.position,
                            topic=channel_text.topic,
                            slowmode_delay=channel_text.slowmode_delay,
                            nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                if channel_text.name.startswith("ticket-") or channel_text.name.startswith("ticket_") or channel_text.name.startswith("ticket"):
                    print_warning(f"Channel {channel_text.name} is a ticket channel, not creating it")
                else:
                    print_add(f"Created Text Channel: {channel_text.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Text Channel: {channel_text.name}")
            except:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_voice.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Voice Channel: {channel_voice.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Voice Channel: {channel_voice.name}")
            except:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")

    # Method to delete emojis in a guild
    @staticmethod
    async def emodelete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Deleted Emoji: {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Emoji{emoji.name}")
            except discord.HTTPException:
                print_error(f"Error While Deleting Emoji {emoji.name}")

    # Method to create emojis in a guild based on another guild's emojis
    @staticmethod
    async def emocreate(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print_add(f"Created Emoji {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Emoji {emoji.name} ")
            except discord.HTTPException:
                print_error(f"Error While Creating Emoji {emoji.name}")

    # Method to edit the guild information (name and icon) in the destination guild
    @staticmethod
    async def guedit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_image = await guild_from.icon_url.read()
            except discord.errors.DiscordException:
                print_error(f"Can't read icon image from {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=f'{guild_from.name}')
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print_add(f"Guild Icon Changed: {guild_to.name}")
                except:
                    print_error(f"Error While Changing Guild Icon: {guild_to.name}")
        except discord.Forbidden:
            print_error(f"Error While Changing Guild Icon: {guild_to.name}")

    # Method to create a template for the destination guild
    @staticmethod
    async def gutemplate(guild_to: discord.Guild):
        try:
            existing_templates = await guild_to.templates()
            for template in existing_templates:
                await template.delete()
                print_delete(f"Deleted Existing Template: {template.code}")

            template = await guild_to.create_template(name=f"{guild_to.name}")
            print_add(f"Created Template: {template.code}")
            pyperclip.copy(f"https://discord.new/{template.code}")
            print_add(f"Template Link Copied To Clipboard")
            sleep(5)
        except discord.Forbidden:
            print_error(f"Error While Creating Template: {guild_to.name}")
        except discord.HTTPException:
            print_error(f"Error While Creating Template: {guild_to.name}")

    # Method to perform all cloning operations at once
    @staticmethod
    async def all(guild_to: discord.Guild, guild_from: discord.Guild):
        await Clone.roledelete(guild_to)
        await Clone.chdelete(guild_to)
        await Clone.rolecreate(guild_to, guild_from)
        await Clone.catcreate(guild_to, guild_from)
        await Clone.chcreate(guild_to, guild_from)
        await Clone.emodelete(guild_to)
        await Clone.emocreate(guild_to, guild_from)
        await Clone.guedit(guild_to, guild_from)
        await Clone.gutemplate(guild_to)

# Sample usage:
# client = discord.Client()
# destination_guild = client.get_guild(destination_guild_id)
# source_guild = client.get_guild(source_guild_id)
# await Clone.all(destination_guild, source_guild)
