from discord.ext import commands
def setup(bot, voice_clients):
    @bot.command(name="leave")
    async def leave(ctx):
        if ctx.guild.id in voice_clients:
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
            await ctx.send("Disconnected from the voice channel.")
        else:
            await ctx.send("I am not connected to a voice channel.")
