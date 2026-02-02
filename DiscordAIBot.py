import discord
import asyncio
from langchain_community.llms import Ollama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os

load_dotenv()
discord_token = os.getenv("discord_token")
ollama = 'llama3' #insert the local ollama model
prefix = '$' #prefix that initiates the bot. like "m!" for deezer music bot

#Ollama is running inside another docker container
llm = Ollama(
    model=ollama,
    base_url = 'http://host.docker.internal:11434')

system_prompt = """
You are a conversational chatbot who is friendly but stoic. Prioritize brevity in your responses. Do not ask personal questions nor inquire about user preferences, interests, or feelings.
"""
conversation_history = []
memory_limit = 30 #keeps the preview 30 messages. 50/50 bot and user allocation

def run_llm(user_message):
    conversation_history.append(HumanMessage(content=user_message))
    
    if len(conversation_history) > memory_limit: #trims the conversation history according to the set memory limit
        conversation_history.pop(0)

    messages = [SystemMessage(content=system_prompt)] + conversation_history
    response = llm.invoke(messages)
    conversation_history.append(AIMessage(content=response))
    return response


#=================================================DISCORD STUFF============================================================

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    content = message.content.strip()

    #triggering the bot
    if content.startswith(prefix):
        user_prompt = content.lstrip(prefix).strip()

        thinking_confirm = await message.channel.send("Thinking...")

        loop = asyncio.get_event_loop()
        reply = await loop.run_in_executor(None,run_llm,user_prompt)

        await thinking_confirm.edit(content=reply)

client.run(discord_token)
