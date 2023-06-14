import yaml
from yaml.loader import SafeLoader
from pathlib import Path
import os
import asyncio
import bot
import UserSession.Session as Session


path = 'config.yml'


def CreateSession():
    config = read_yaml(path)
    # print(config)
    # for key in config:
    #     print(key, '->', dict[key])
    User = Session.Session(config)
    # print(User.GetFullUrl())
    bot_entity = bot.Bot(User)
    bot_entity.possible_letters()


async def main() -> None:
    """Entry async method for starting the bot."""
    CreateSession()


def read_yaml(file: str) -> dict:
    pathYaml = os.path.join(Path.cwd(), file)
    if os.path.isfile(pathYaml):
        with open(pathYaml) as f:
            config = yaml.load(f, Loader=SafeLoader)
        return config
    else:
        return None


if __name__ == "__main__":
    asyncio.run(main())
