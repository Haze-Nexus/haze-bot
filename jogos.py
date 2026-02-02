import asyncio
import discord
import random
from datetime import datetime, timedelta
from database import db


class Jogos:

    @staticmethod
    async def pedra_papel_tesoura(ctx, bot):

        opcoes = ["pedra", "papel", "tesoura"]
        escolha_bot = random.choice(opcoes)

        membros = [m for m in ctx.guild.members if not m.bot]
        user_aleatorio = random.choice(membros).display_name if membros else "alguém"

        await ctx.send(
            f"🎮 **{ctx.author.name}**, digite sua escolha: **Pedra, Papel ou Tesoura**?"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await bot.wait_for("message", check=check, timeout=30.0)
            escolha_user = msg.content.lower().strip()

            if escolha_user not in opcoes:
                await ctx.send(
                    "❌ Opção inválida! Escolha entre: Pedra, Papel ou Tesoura."
                )
                return

            resultado = Jogos._calcular_vencedor(
                escolha_user, escolha_bot, user_aleatorio
            )

            # Lógica de Cores e Recompensas/Castigos
            if "Ganhei" in resultado:
                db.alterar_hazium(ctx.author.id, -2)
                cor = discord.Color.red()
                texto_extra = "\n*Tu perdeu os seus Hazium!* 🤫"
            elif "Empate" in resultado:
                cor = discord.Color.gold()
                texto_extra = "\n*Nada mudou.*"
            else:
                cor = discord.Color.green()
                db.alterar_hazium(ctx.author.id, 2)
                texto_extra = "\n*Ganhou +2 Hazium!* 💰"

            embed = discord.Embed(
                title="🕹️ Resultado do Desafio",
                description=f"Você: **{escolha_user.capitalize()}** vs Eu: **{escolha_bot.capitalize()}**\n\n**{resultado}**{texto_extra}",
                color=cor,
                timestamp=datetime.now(),
            )
            embed.set_footer(text="Haze Nexus • Python Edition")
            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send(
                f"⏰ {ctx.author.mention}, tu demorou demais e eu cansei de esperar!"
            )

    @staticmethod
    async def roleta_russa(ctx):
        tiro = random.randint(1, 6)
        await ctx.send(f"**{ctx.author.display_name}** coloca a arma na cabeça... 🔫")
        await asyncio.sleep(2)

        if tiro == 1 or tiro == 5:
            db.alterar_hazium(ctx.author.id, -1)
            try:
                await ctx.author.timeout(
                    timedelta(minutes=1), reason="Perdeu na Roleta Russa"
                )
                await ctx.send(
                    f"BOOM! 💥 {ctx.author.mention} morreu, perdeu os Hazium e tá mutado por 1 min!"
                )
            except:
                await ctx.send(
                    f"BOOM! 💥 Tu morreu e perdeu os Hazium, mas não consegui te mutar!"
                )
        else:
            db.alterar_hazium(ctx.author.id, 1)
            respostas_vitoria = [
                f"Câmara vazia! {ctx.author.mention} ganhou +1 Hazium por ser corajoso! 💰",
                f"*Click*... Você sobreviveu! Ganhou +1 Hazium. 🍀",
            ]
            await ctx.send(random.choice(respostas_vitoria))

    @staticmethod
    def _calcular_vencedor(user, bot_choice, vitima):
        if user == bot_choice:
            return "Empate! 🤝"
        vitorias = {"pedra": "tesoura", "papel": "pedra", "tesoura": "papel"}
        if vitorias[user] == bot_choice:
            return "Você venceu... por enquanto. 😒"
        return f"Ganhei! Mais fácil do que molestar o **{vitima}**. 💀"
