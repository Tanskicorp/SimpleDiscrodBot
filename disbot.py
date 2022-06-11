import discord
from discord import Member
from discord.ext import commands
from discord import utils
from discord.ext.commands import has_permissions, MissingPermissions
import random
config = {
    'token': 'token',
    'prefix': '!',
    'general_ch': value,
}

intents = discord.Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=config['prefix'], intentse = intents)

rolemsg = {
    'message_id': value,
    '🟨': value,
    '🟧': value,
    '🟩': value,    
}

excroles = ['value']

@bot.event# выдача роли по реакции
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)# получаем канал где была поставлена реакция
    message = await channel.fetch_message(payload.message_id)# вытягиваем сообщение из этого канала
    guild = bot.get_guild(payload.guild_id)# получаем информацию о сервере
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)# получаем какое емоджи было поставлено
    if payload.member.id == bot.user.id:
        return
    if payload.message_id == rolemsg['message_id']:#если айди сообщения совпадает
        role = discord.utils.get(guild.roles, id=rolemsg[reaction.emoji])#записываем роль которая соответсвует смайлику
        if str(rolemsg[reaction.emoji]) in str(payload.member.roles):#если эта роль уже есть то удаляем ее и реакцию
            await payload.member.remove_roles(role)
            await reaction.remove(payload.member)
        else:#иначе если есть то выдаём
            await payload.member.add_roles(role)
            await reaction.remove(payload.member)

#--------ban------
@bot.command()
@commands.has_role('Admin')
async def ban(ctx, member: discord.Member, *, reason = None):
    if reason == None:
        reason = "Причина не указана"
    await ctx.guild.ban(member, reason = reason)
    await ctx.reply(f'{member.mention} был забанен на сервере по причине: {reason}')
@ban.error
async def ban_error(error, ctx):
    await bot.get_channel(config['general_ch']).send("У вас недостаточно прав для выполнения данной комманды")

#----------unban----------
@bot.command()
@commands.has_role('Admin')
async def unban(ctx, *,member):
    banned_user = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_user:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
@unban.error
async def unban_error(error, ctx):
    await bot.get_channel(config['general_ch']).send("У вас недостаточно прав для выполнения данной комманды")

#----------kick--------
@bot.command()
@commands.has_role('Admin')
async def kick(ctx, member: discord.Member, *, reason = None):
    if reason == None:
        reason = "Причина не указана"
    await ctx.guild.kick(member)
    await ctx.reply(f'{member.mention} был выгнан с сервера по причине: {reason}')
@kick.error
async def kick_error(error, ctx):
    await bot.get_channel(config['general_ch']).send("У вас недостаточно прав для выполнения данной комманды")

#---------whoami-------
@bot.command()
@commands.has_role('Admin')
async def whoami(ctx):
    await ctx.reply(f'Ваша роль {ctx.message.author.top_role.mention}')
@whoami.error
async def whoami_error(error, ctx):
    await bot.get_channel(config['general_ch']).send("У вас недостаточно прав для выполнения данной комманды")

#----- Команда выдачи роли ------
@bot.command()
@commands.has_role('Admin')
async def role_add(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.reply(f'Пользователю {member.mention} была выдана роль {role.mention}')
@role_add.error
async def role_add_error(error, ctx):
    await bot.get_channel(config['general_ch']).send("У вас недостаточно прав для выполнения данной комманды")

#----- Команда удаления роли ------
@bot.command()
@commands.has_role('Admin')
async def role_remove(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.reply(f'Пользователь {member.mention} был лишён роли {role.mention} + {member} + {role}')
@role_remove.error
async def role_remove_error(error, ctx):
    await bot.get_channel(config['general_ch']).send("У вас недостаточно прав для выполнения данной комманды")

#-------random------
@bot.command()
async def rand(ctx, arg):#стх это сама команда а дальше аргументы
    rang = []
    a = str(arg)
    rang.append(str(arg[:a.find('-')]))
    rang.append(str(arg[a.find('-') + 1:]))
    await ctx.reply(random.randint(int(rang[0]), int(rang[1])))
    #await ctx.reply(ctx)
#------------------------------------------------------------------------------------

bot.run(config['token'])