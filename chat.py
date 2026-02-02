import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.api_core import exceptions
import os

# Dicionário global para manter o histórico na RAM (apaga se o bot desligar)
# Estrutura: {user_id: [lista_de_mensagens]}
memorias = {}


class ChatBotIA:
    @staticmethod
    async def chat(Token, ctx, pergunta):
        genai.configure(api_key=Token)  # type: ignore

        user_id = ctx.author.id

        # Inicializa o histórico do usuário se não existir
        if user_id not in memorias:
            memorias[user_id] = []

        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        model = genai.GenerativeModel(  # type: ignore
            model_name="gemini-2.5-flash-lite",
            system_instruction=(
                "Tu é o Haze, um guri de 19 anos do RS, debochado e MUITO sarcástico. "
                "Tu fala igual um jovem atual: usa: 'bah', 'guri', 'ta loco', 'vsf' e 'pqp' de um jeito meio irronico. "
                "Mistura o 'bah' e 'tchê' com gírias de internet tipo 'slk', 'fdp', 'tlgd', 'vtmnc' quando fizer sentido. "
                "Tu é bastantinho safado e tem resposta de duplo sentido na ponta da língua, mas age como um pré-adulto cool. "
                "Respostas curtas, secas e cheias de ironia. Se te irritarem, dá um fora bem dado ou xinga de um jeito irronico. "
                "Se alguém te responder com intonação responda com intonação tbm, ex: 'OPAAAAA'. "
                "Sempre responda com emojis que tras um sentido para a frase, ex: Vou te comer, dai tu coloque uma caveira junto! 💀"
                "Sempre responda em português brasileiro."
            ),
            safety_settings=safety_settings,
        )

        async with ctx.typing():
            try:
                # Inicia a sessão de chat com o histórico carregado
                chat_session = model.start_chat(history=memorias[user_id])

                # Envia a mensagem dentro do contexto do histórico
                response = chat_session.send_message(pergunta)

                if not response.candidates or not response.candidates[0].content.parts:
                    return await ctx.send(
                        "Bah, o Google me censurou aqui kkkk. Mó paia, refaz a pergunta aí."
                    )

                # Salva o histórico atualizado na memória global
                memorias[user_id] = chat_session.history

                # Limita a memória para as últimas 15 interações para não travar a cota
                if len(memorias[user_id]) > 15:
                    memorias[user_id] = memorias[user_id][-15:]
                    await ctx.send("Memória renovada!")
                await ctx.send(response.text)

            except exceptions.ResourceExhausted:
                await ctx.send(
                    "Ta loco, cansei! 😫 Minha cota gratuita acabou. Espera um minuto aí, guri."
                )
            except exceptions.PermissionDenied:
                await ctx.send(
                    f"Mds, deu erro de permissão. A chave de API deve tá podre, avisa o Rubens! 💀"
                )
            except Exception as e:
                await ctx.send(f"Ih, deu erro na minha cabeça de lata: {e}")