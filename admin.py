import discord
from discord.ext import commands
from worldgen import world

tokenpath = 'config/token'


def main():  # авторизация в лобии
    discord_api = discord_bot()


class discord_bot():  # объект, отвечающий за взаимодействие с дискордом
    def __init__(self):
        global tokenpath
        self.token = get_token(tokenpath)
        self.bot = commands.Bot(command_prefix="!")

        @self.bot.command(pass_context=True)  # разрешаем передавать агрументы
        async def new_world(ctx, size, tile, octaves, seed):  # создаем асинхронную фунцию бота
            size = int(size)
            tile = int(tile)
            octaves = int(octaves)
            if size > 2000 or tile < 1:
                await ctx.send('Sorry, cruel tyranny limits the size of the world for you.')
            else:
                await ctx.send('Generating of world has been started')
                name = world_generator(size, tile, octaves, seed)
                await ctx.send('Generating of world has been done succefull.')
                print(name.save_path)
                await ctx.send(
                    'World has been generated with size = %d, tile size = %d, with %d octaves and "%s" seed.' % (
                    size, tile, octaves, seed))
                await ctx.send('This is your map.', file=discord.File(name.save_path))
                await ctx.send(file=discord.File('log.txt'))

        self.bot.run(self.token)


def get_token(filepath):  # получение токена из файла
    filepath = filepath + '.txt'
    n = open(filepath, 'r')
    return (n.read())


'''
---------------------- Игровые объекты
'''


class world_generator():  # генерация мира
    def __init__(self, size, tile, octaves, seed):
        n = world(size, tile, octaves, seed)
        self.save_path = n.save_path


if __name__ == '__main__':
    main()
