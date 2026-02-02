import datetime
import discord
from discord.ext import commands
import os
import asyncio

# import sqlite3
from dotenv import load_dotenv
from jogos import Jogos
from chat import ChatBotIA
from database import db

load_dotenv()
TOKEN_DISCORD = os.getenv("DISCORD_TOKEN")
TOKEN_GIMINI = os.getenv("GIMINI_TOKEN")

# Configuração de Intenções (Obrigatório no Python)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="hz!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    print(f"🚀 Haze Nexus iniciado com sucesso! Logado como {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    # Verifica se o erro é por falta de permissão
    if isinstance(error, commands.MissingPermissions):
        msg = await ctx.send(
            f"❌ {ctx.author.mention}, você não tem **aura** suficiente para usar esse comando!"
        )
        await asyncio.sleep(5)
        await msg.delete()
        return  # Finaliza aqui para não executar os outros ifs

    # Verifica se faltou um argumento (ex: esqueceu de botar o número no !clean)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"❓ Está faltando informação, {ctx.author.name}! Verifique como usar o comando."
        )
        return

    # Se o comando não existir, o bot ignora (para não poluir o terminal)
    if isinstance(error, commands.CommandNotFound):
        return

    # Para qualquer outro erro, ele avisa no console para você debugar
    print(f"Erro detectado: {error}")


# --- Comandos Administrativos ---
@bot.command()
@commands.has_permissions(administrator=True)  # Só você/ADMs podem usar
async def doar(ctx, alvo: str, quantidade: int):
    # O MemberConverter tenta transformar a string (@menção, nome ou ID) em um usuário real
    converter = commands.MemberConverter()
    try:
        usuario = await converter.convert(ctx, alvo)

        db.alterar_hazium(usuario.id, quantidade)
        if quantidade > 0:
            await ctx.send(
                f"✅ Feito! **{quantidade} Hazium** foram pra conta de **{usuario.display_name}**. 💰"
            )
        else:
            await ctx.send(
                f"✅ Feito! **{quantidade} Hazium** foram retirado da conta do **{usuario.display_name}**. 💰😂"
            )
    except commands.MemberNotFound:
        await ctx.send(
            f"❌ Bah guri, não achei nenhum '{alvo}' aqui no server. Tu escreveu certo?"
        )
    except Exception as e:
        await ctx.send(f"❌ Deu pau aqui: {e}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, quantidade: int):
    qtd = max(1, min(quantidade, 100))
    await ctx.channel.purge(limit=qtd)
    msg = await ctx.send(
        f"✅ **{qtd}** mensagens incineradas por ordem de **{ctx.author.name}**!"
    )
    await asyncio.sleep(3)
    await msg.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def mention(ctx, repeticao: int, *, nome_alvo: str):
    num_rep = max(1, min(repeticao, 15))

    # Busca membro
    usuario = discord.utils.find(
        lambda m: nome_alvo.lower() in m.display_name.lower(), ctx.guild.members
    )

    if usuario:
        for _ in range(num_rep):
            await ctx.send(
                f"Ei {usuario.mention}, o {ctx.author.name} está te chamando! 📣"
            )
            await asyncio.sleep(0.5)
    else:
        await ctx.send(f"Não encontrei ninguém com o nome `{nome_alvo}`. 🧐")


# --- Comandos Gerais ---
@bot.command()
async def chat(ctx, *, mensagem: str):  
    try:
        await ChatBotIA.chat(TOKEN_GIMINI, ctx, mensagem)
    except Exception as e:
        await ctx.send(f"Ih, deu erro na minha cabeça de lata: {e}")

@bot.command()
async def status(ctx, usuario: discord.Member = None): # type: ignore
    usuario = usuario or ctx.author
    valor = db.ver_saldo(usuario.id)

    if valor < 0:
        await ctx.send(f"Bah {usuario.mention}, tu tem **{valor} Hazium**... Tá devendo até as calça, pqp 💀")
    else:
        await ctx.send(f"💰 {usuario.mention} tem **{valor} Hazium** na conta.")


@bot.command()
async def top(ctx):
    ranking = db.pegar_ranking()
    if not ranking:
        return await ctx.send("Ninguém tem um tostão furado ainda. 💸")

    msg = "🏆 **RANKING DOS MAIS RICOS (HAZIUM)** 🏆\n\n"
    for i, (user_id, saldo) in enumerate(ranking, 1):
        msg += f"{i}º - <@{user_id}>: **{saldo} Hazium**\n"

    await ctx.send(msg)


@bot.command()
async def games(ctx, valor: int):
    if valor == 1:
        await Jogos.mensagem_hazium(ctx, 5, "pedra papel tesoura")
        await Jogos.pedra_papel_tesoura(ctx, bot)
    elif valor == 2:
        await Jogos.mensagem_hazium(ctx, 4, "roleta russa")
        await Jogos.roleta_russa(ctx)
    else:
        await ctx.send("🎮 Jogo não encontrado. Tente `hz!help` para descobrir todos os jogos disponiveis.")

@bot.command()
async def help(ctx):
    bot.help_command = None
    embed = discord.Embed(
        title="📖 Haze Nexus - Manual de Instruções",
        description=f"Olá **{ctx.author.name}**! Aqui está o que eu posso fazer, guri:",
        color=discord.Color.blue(),
        timestamp=datetime.datetime.now(),
    )

    embed.add_field(
        name="🎮 Jogos",
        value="`hz!games 1` - Pedra, Papel ou Tesoura.\n`hz!games 2` - Roleta russa.",
        inline=False,
    )

    embed.add_field(
        name="💰 Economia (Hazium)",
        value="`hz!status` - Vê quanto tu tem no bolso.\n`hz!top` - Ranking dos mais ricos do server.",
        inline=False,
    )

    embed.add_field(
        name="🤖 Inteligência",
        value="`hz!chat [texto]` - Converse comigo (tenho memória, juro).",
        inline=False,
    )

    embed.add_field(
        name="🧹 Moderação & ADM",
        value="`hz!clean [1-100]` - Limpa o chat.\n"
        "`hz!mention [qtd] [nome]` - Spam de menção.\n"
        "`hz!doar [user] [valor]` - Criar/Doar grana.",
        inline=False,
    )

    embed.set_footer(text="Haze Nexus Bot • Python Edition")
    await ctx.send(embed=embed)


bot.run(TOKEN_DISCORD)  # type: ignore
