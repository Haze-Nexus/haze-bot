import datetime
import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from jogos import Jogos
from chat import ChatBotIA
from database import db

load_dotenv()
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
TOKEN_GEMINI = os.getenv("GIMINI_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="r!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"🚀 Haze Nexus logado como {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send(
            f"❌ {ctx.author.mention}, você não tem permissão para isso!"
        )
        await asyncio.sleep(5)
        await msg.delete()

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"❓ Falta informação! Use `r!help` para ver como usar o comando."
        )

    elif not isinstance(error, commands.CommandNotFound):
        print(f"Erro: {error}")


# --- COMANDOS ADMINISTRATIVOS ---


@bot.command()
@commands.has_permissions(administrator=True)
async def doar(ctx, membro: discord.Member, quantidade: int):
    try:
        db.alterar_hazium(membro.id, quantidade)
        status = "enviados para" if quantidade > 0 else "retirados de"
        await ctx.send(
            f"✅ **{abs(quantidade)} Hazium** {status} **{membro.display_name}**."
        )
    except Exception as e:
        await ctx.send(f"❌ Erro ao processar transação: {e}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, quantidade: int):
    qtd = max(1, min(quantidade, 100))
    await ctx.channel.purge(limit=qtd)
    msg = await ctx.send(f"🗑️ **{qtd}** mensagens limpas por {ctx.author.name}!")
    await asyncio.sleep(3)
    await msg.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def mention(ctx, repeticao: int, membro: discord.Member):
    num_rep = max(1, min(repeticao, 10))
    for _ in range(num_rep):
        await ctx.send(f"Ei {membro.mention}, o {ctx.author.name} está te chamando! 📣")
        await asyncio.sleep(0.6)


# --- COMANDOS DE ECONOMIA ---
@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)  # Evita spam de cliques
async def receber(ctx):
    sucesso, tempo_restante = db.resgatar_daily(ctx.author.id)

    if sucesso:
        embed = discord.Embed(
            title="💰 Daily Resgatado!",
            description=f"{ctx.author.mention}, você recebeu **20 Hazium**! Volte amanhã para mais.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
    else:
        # Formata o tempo restante de forma bonitinha
        horas = int(tempo_restante.total_seconds() // 3600) # type: ignore
        minutos = int((tempo_restante.total_seconds() % 3600) // 60)  # type: ignore

        await ctx.send(
            f"⏳ Calma aí, guri! Você já resgatou seu prêmio hoje.\n"
            f"Tente novamente em **{horas}h {minutos}min**."
        )


@bot.command()
async def status(ctx, usuario: discord.Member = None):  # type: ignore
    usuario = usuario or ctx.author
    saldo = db.ver_saldo(usuario.id)

    if saldo < 0:
        await ctx.send(
            f"💀 {usuario.mention}, você está devendo! Saldo: **{saldo} Hazium**"
        )
    else:
        await ctx.send(f"💰 {usuario.mention} possui **{saldo} Hazium**.")


@bot.command()
async def top(ctx):
    ranking = db.pegar_ranking()
    if not ranking:
        return await ctx.send("🌵 O ranking está deserto...")

    embed = discord.Embed(
        title="🏆 Top 10 Ricos - Haze Nexus",
        color=discord.Color.gold(),
        timestamp=datetime.datetime.now(),
    )

    for i, (user_id, hazium) in enumerate(ranking, 1):
        usuario = bot.get_user(user_id)
        nome = usuario.name if usuario else f"ID: {user_id}"
        medalha = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, "🔹")
        embed.add_field(
            name=f"{medalha} #{i} {nome}", value=f"**{hazium} Hazium**", inline=False
        )

    await ctx.send(embed=embed)

# --- COMANDOS DE DIVERSÃO ---

@bot.command()
async def chat(ctx, *, mensagem: str):
    await ChatBotIA.chat(TOKEN_GEMINI, ctx, mensagem)


@bot.command()
async def games(ctx, id_jogo: int):
    if id_jogo == 1:
        await Jogos.mensagem_hazium(ctx, 2, "Pedra, Papel e Tesoura")
        await Jogos.pedra_papel_tesoura(ctx, bot)
    elif id_jogo == 2:
        await Jogos.mensagem_hazium(ctx, 1, "Roleta Russa")
        await Jogos.roleta_russa(ctx)
    else:
        await ctx.send("🎮 Jogo inválido! Use `1` para Jokenpô ou `2` para Roleta.")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="📖 Rift - Guia de Comandos",
        description=f"Olá {ctx.author.mention}, aqui estão meus comandos:",
        color=discord.Color.blue(),
    )
    embed.add_field(name="🎮 Jogos", value="`r!games 1` | `r!games 2`", inline=True)
    embed.add_field(name="💰 Economia", value="`r!status` | `r!top`", inline=True)
    embed.add_field(name="🤖 IA", value="`r!chat [texto]`", inline=True)
    embed.add_field(
        name="🛠️ Mod",
        value="`r!clean [1-100]` | `r!doar [user] [qtd]` | `r!receber` | `r!mention [1-15] [user]`",
        inline=False,
    )
    embed.set_footer(text="Haze Nexus v2.0")
    await ctx.send(embed=embed)


bot.run(TOKEN_DISCORD)  # type: ignore
