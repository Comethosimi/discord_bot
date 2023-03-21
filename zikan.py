import discord
from discord.ext import tasks
from datetime import datetime 

TOKEN = "OTY1OTU4NTQ2MjcxMzk1OTEw.Yl6xAA.9BDQozRMsldqSnbkXdrQ31kioBU" #トークン
CHANNEL_ID = 910758813567709185 #チャンネルID
# 接続に必要なオブジェクトを生成
client = discord.Client()
times = ['21:47','21:48','12:00']
message_list = ['朝だよ','昼だよ','夜だよ']
num_list = ['0','1','2','3','4','5','6','7','8','9']

def time_chech(s):
	res = 0
	flag = 1
	if len(s) != 5:flag = 0
	for i in range(len(s)):
		if i == 2:continue
		if s[i] in num_list:continue
		else:flag = 0
	
	return flag



@client.event
async def on_message(message):
	if client.user in message.mentions:
		m = message.content
		startpos = 0
		for i in range(len(m)):
			if m[i] == '>':
				startpos = i
				break
		m = m[startpos+1:]
		tmp_time = m[1:6]
		tmp_content = m[7:]
		if m == ' 予定一覧':
			await message.channel.send("現在の予定一覧")
			res = ''
			if len(times) == 0:await message.channel.send("予定...無し！w")
			for i in range(len(times)):
				res += times[i]+' '+message_list[i]+'\n'
			await message.channel.send(res)
		if tmp_time == 'reset':
			times.clear()
			message_list.clear()
			await message.channel.send("リセットしたよ")
		f = time_chech(tmp_time)
		if f == 0:await message.channel.send("「時時:分分 内容」の形式で入力してね")
		else:
			times.append(tmp_time)
			message_list.append(tmp_content)
			await message.channel.send(tmp_time+'に'+tmp_content+'を知らせるよ')


# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
	# 現在の時刻
	now = datetime.now().strftime('%H:%M')
	channel = client.get_channel(CHANNEL_ID)
	for i in range(len(times)):
		if now == times[i]:
			m = times[i] +'です。'+ message_list[i]
			await channel.send(m)

#ループ処理実行
loop.start()
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)