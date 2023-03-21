import discord
from discord.ext import tasks
from discord.ext import commands
from discord.channel import VoiceChannel
from datetime import datetime
import random
import re

TOKEN = "OTY1OTU3OTg4MDg1MDE4NjY2.Yl6weg.hpHjdmJtGq7--GcMm9_11O98ZVs"
CHANNEL_ID = 910758813567709185
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
voiceChannel: VoiceChannel
voiceChannel = "null"

alert = [0]
subj = ["おかけ", "うどん", "わこう", "P"]
nono = ["バカ", "アホ", "ウンコ", "ポンコツ", "雑魚", "最強"]
yn = ["だ", "です", "らしい", "じゃない"]
pred = ["よ<:tuintabo:908360774844563516>", "よん♡", "よ<:agunesudezirtaru:908384391884050512>", "よ！"]
reply = ["ちがうよ", "しらないよ", "だめだよ", "そんなことないよ" ,"たしかに"]
reply2 = ["連投するな", "さみしいの？", "かわいそう...", "あわれんであげる", "あわれあわれ！",
          "恥ずかしくないの？", "なんかかわいそうになってきた", "...", "ちゃんと反応してあげる"]
reply3 = ["<:kirei:934092868430221432>","<:erai:935506940124098620>","<:yuunou:877487458634309643>","<:haato:909105220074741790>",
          "<:tuintabo:908360774844563516>","<:agunesudezirtaru:908384391884050512>","<:kimo:909433365713805384>"]
before_author = [""]
before_author_counter = [0]
emoji = ["<:agunesudezirtaru:908384391884050512>"]
emoji2 = ["<:neruwa:877567765555322920>","<:no:909242976029524040>",
          "<:zikan:909243106711449670>","<:dayo:909100739907973130>"]
title_name = ["__寝る時間だよ__"]
des = ["**早く寝ろ！！！！**"]
BLOCKUSER = ["囚われのおかけ"]
syazaibun = ["ええわ、ゆるしたる","やだよ","ゆるさないよ","もっと謝れ！","どーしよっかな～"]

#通話機能の変数
caller = ["誰か"]
caller_menbers = [""]
caller_message = [""]
date_bef = [""]
hour_bef = [""]
minu_bef = [""]
seco_bef = [""]
date_aft = [""]
hour_aft = [""]
minu_aft = [""]
seco_aft = [""]

#時報の変数
call_checker = [0]
call_time = ["23:00","23:30"]
call_reset = ["23:01","23:31"]
call_comment = ["いい子は寝るじかんだよ。","まだ寝てないの？"]

#ログイン情報
@client.event
async def on_ready():
    print('ログイン成功')

#つげぐちでじたる
@client.event
async def on_message(message):
    global voiceChannel


#自身の補助機能
#時報補助（自身が自身にメンションした場合のみ）
    if client.user in message.mentions and message.author == client.user:
        channel = client.get_channel(CHANNEL_ID)
        embed = discord.Embed(title=title_name[0],description=des[0],color=discord.Colour.blue())
        vote = await message.channel.send(embed=embed)
        for i in emoji2:
            await vote.add_reaction(i)
#以降自身の発言を無視
    if message.author == client.user:
        return


#特定ユーザーへの対応（連投リセあり）
#投獄されたとき
    for ign in range(len(BLOCKUSER)):
        if message.author.display_name == BLOCKUSER[ign]:
            before_author_counter[0] = 0
#謝罪すると確率で許す
            if "ゆるして" in message.content or "ごめん" in message.content:
                syazai = random.randint(0, len(syazaibun) - 1)
                await message.channel.send(syazaibun[syazai])
                if syazai == 0:
                    BLOCKUSER.remove(message.author.display_name)
                    return
#黙らせモード時
            await message.channel.send(message.author.display_name + "はしゃべんな")
            return


#絵文字（メンション無し）
    await message.add_reaction(emoji[0])


#投獄するとき
    if client.user in message.mentions and message.content.endswith("を黙らせて"):
        before_author_counter[0] = 0
#名前サーチ
        pattern = '(?<= ).*(?=を)'
        search = re.search(pattern, message.content)
#既にブロック済みの場合
        for ign in range(len(BLOCKUSER)):
            if search.group() == BLOCKUSER[ign]:
                await message.channel.send(search.group() + "は今黙らせてる最中だから")
                return
#まだブロックしていない場合
        await message.channel.send(search.group() + "を黙らせればいいのね？")
        BLOCKUSER.append(search.group())
        return

#リプライ機能（メンション＋特定言語で終わる）
#見せて
    if client.user in message.mentions and message.content.endswith("見せて"):
        before_author_counter[0] = 0
        pattern = '(?<= ).*(?=見)'
        search = re.search(pattern, message.content)
#黙らせリスト
        if search.group() == "黙らせリスト":
            if not BLOCKUSER:
                await message.channel.send("誰も黙らせてないよ")
            else:
                for i in range(len(BLOCKUSER)):
                  await message.channel.send(BLOCKUSER[i])
                await message.channel.send("の" + str(len(BLOCKUSER)) + "人黙らせてるよ")
                await message.channel.send("謝ったら許すかもよ")
            return
        else:
            await message.channel.send(search.group() + "見せないよ")
            return
#ゆるしてあげて
    if client.user in message.mentions and message.content.endswith("をゆるしてあげて"):
        before_author_counter[0] = 0
        pattern = '(?<= ).*(?=を)'
        search = re.search(pattern, message.content)
        if not BLOCKUSER:
            await message.channel.send("誰も黙らせてないよ")
            return
        elif search.group() == "みんな":
            for i in range(len(BLOCKUSER)):
                await message.channel.send(BLOCKUSER[i])
            await message.channel.send("ゆるしてあげる。よかったね。")
            BLOCKUSER.clear()
            return
        else:
            for i in range(len(BLOCKUSER)):
                if search.group() == BLOCKUSER[i]:
                    await message.channel.send(search.group() + "をゆるしてあげる。よかったね。")
                    BLOCKUSER.remove(search.group())
                    return
            await message.channel.send(search.group() + "？そんな人知らないよ。")
            return



#連投禁止（メンション無し）
#3連投禁止
    if message.author == before_author[0] and before_author_counter[0] < 10:
        before_author_counter[0] += 1
        if before_author_counter[0] > 1:
            await message.channel.send(reply2[before_author_counter[0] - 2])
            return
        before_author_counter[0] = 1
    if message.author != before_author[0]:
        before_author[0] = message.author
        before_author_counter[0] = 0
#10連投後はスタンプ反応
    if message.author == before_author[0] and before_author_counter[0] > 8:
        random_reply = random.randint(0, len(reply3) - 1)
        await message.channel.send(reply3[random_reply])
        return


#特定言語に反応（メンション無し）
#おかけに反応
    if "おかけ" in message.content:
        member_mention = "<@523738501070454785>"
        await message.channel.send(member_mention)
        number01 = random.randint(0, len(nono) - 1)
        number02 = random.randint(0, len(yn) - 1)
        number03 = random.randint(0, len(pred) - 1)
        okake = subj[0] + nono[number01] + yn[number02] + pred[number03] + "って" + message.author.display_name + "が言ってたよ"
        await message.channel.send(okake)
#うどんに反応
    if "うどん" in message.content:
        member_mention = "<@346271580885876747>"
        await message.channel.send(member_mention)
        number01 = random.randint(0, len(nono) - 1)
        number02 = random.randint(0, len(yn) - 1)
        number03 = random.randint(0, len(pred) - 1)
        udon = subj[1] + nono[number01] + yn[number02] + pred[number03] + "って" + message.author.display_name + "が言ってたよ"
        await message.channel.send(udon)
#わこうに反応
    if "わこう" in message.content:
        member_mention = "<@428308331309039617>"
        await message.channel.send(member_mention)
        number01 = random.randint(0, len(nono) - 1)
        number02 = random.randint(0, len(yn) - 1)
        number03 = random.randint(0, len(pred) - 1)
        wako = subj[2] + nono[number01] + yn[number02] + pred[number03] + "って" + message.author.display_name + "が言ってたよ"
        await message.channel.send(wako)
#Pに反応
    if "P" in message.content:
        member_mention = "<@497764238815789057>"
        await message.channel.send(member_mention)
        number01 = random.randint(0, len(nono) - 1)
        number02 = random.randint(0, len(yn) - 1)
        number03 = random.randint(0, len(pred) - 1)
        pp = subj[3] + nono[number01] + yn[number02] + pred[number03] + "って" + message.author.display_name + "が言ってたよ"
        await message.channel.send(pp)


#通話参加
    if client.user in message.mentions and "通話来て" in message.content:
        before_author_counter[0] = 0
#通話参加時のアクション
        if voiceChannel == "null":
            await message.channel.send("いいよ！" + message.author.voice.channel.name + "ね！")
            voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
#時間チェッカー(入場)
            date = datetime.now()
            date_bef[0] = date.day
            hour_bef[0] = date.hour
            minu_bef[0] = date.minute
            seco_bef[0] = date.second
            caller[0] = message.author.display_name
            return
        else:
            await message.channel.send("もう" + message.author.voice.channel.name + "にいるよ")
            return
#通話退出
    if client.user in message.mentions and "またね" in message.content:
        before_author_counter[0] = 0
#時間チェッカー(退出)
        date = datetime.now()
#時間
        if date_bef[0] == date.day:
            hour_aft[0] = date.hour - hour_bef[0]
        else:
            hour_aft[0] = date.hour + 24 - hour_bef[0]
#分
        if date.minute < minu_bef[0]:
            hour_aft[0] = hour_aft[0] - 1
            minu_aft[0] = 60 - minu_bef[0] + date.minute
        else:
            minu_aft[0] = date.minute - minu_bef[0]
#秒
        if date.second < seco_bef[0]:
            minu_aft[0] = minu_aft[0] - 1
            seco_aft[0] = 60 - seco_bef[0] + date.second
        else:
            seco_aft[0] = date.second - seco_bef[0]
#退出時のメンバー取得
        member_names = [i.display_name for i in message.author.voice.channel.members]
        caller_menbers[0] = ""
        for i in range(len(member_names)):
            if member_names[i] != caller[0] and member_names[i] != client.user.display_name:
                caller_menbers[0] += member_names[i] + "と"
        if caller_menbers[0] == "":
            caller_message[0] = "二人で"
        else:
            caller_message[0] = caller_menbers[0]
#セリフ
        comment = str(hour_aft[0]) + "時間" + str(minu_aft[0]) + "分" + str(seco_aft[0]) + "秒"
        if hour_aft[0] == 0:
            comment = str(minu_aft[0]) + "分" + str(seco_aft[0]) + "秒"
            if minu_aft[0] == 0:
                comment =str(seco_aft[0]) + "秒"
        await message.channel.send(caller[0] + "に呼ばれて、" + caller[0] + "と" + caller_message[0] + comment + "話したよ！またね！")
        await voiceChannel.disconnect()
        voiceChannel = "null"
        return


#自身へのメンションに反応（特定言語で終わらない場合）
    if client.user in message.mentions:
        number10 = random.randint(0, len(reply) - 1)
        await message.channel.send(message.author.mention + reply[number10])


#時報BOT
@tasks.loop(seconds=10)
async def loop():

#00:00は投票型
    now = datetime.now().strftime('%H:%M')
    if now == '00:00':
        if(alert[0] == 0):
            channel = client.get_channel(CHANNEL_ID)
            member_mention = "<@965957988085018666>"
            await channel.send(member_mention)
            alert[0] = 1

#その他時報呼び出し
    for num in range(len(call_time)):
        if now == call_time[num] and call_checker[0] == 0:
            call_checker[0] = 1
            channel = client.get_channel(CHANNEL_ID)
            await channel.send("今" + now + "だよ。" + call_comment[num])

#その他時報チェッカーリセット
    for num in range(len(call_time)):
        if now == call_reset[num] and call_checker[0] == 1:
            call_checker[0] = 0

loop.start()
client.run(TOKEN)