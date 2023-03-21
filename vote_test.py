import discord
from discord.ext import tasks
from discord.ext import commands
from datetime import datetime 
import random


TOKEN = "OTY1OTU4NTQ2MjcxMzk1OTEw.Yl6xAA.9BDQozRMsldqSnbkXdrQ31kioBU" #トークン
CHANNEL_ID = 910758813567709185 #チャンネルID
# 接続に必要なオブジェクトを生成
client = discord.Client()

times = []
message_list = []
vote_list = []
choice_list = []
num_list = ['0','1','2','3','4','5','6','7','8','9']
com_list = ['予定一覧','リセット','予定追加','予定削除','おっぱい音頭','スーパーだじゃれモード']

list_yesno = ['🙆‍♂️', '🙅‍♂️']
list_vote = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
dajare_list = ['布団がふっとんだ','イクラはいくら？','カレーはかれー','トイレにいっといれ',
			'カエルが帰る','ラクダに乗るとらくだ','ネコがねころんだ','イルカはいるか？',
			'パンダのパンだ','箱をはこぶ','虫はむし','パンダのパンだ','栗のクリーム',
			'君は黄身が好き？','ソーダはうまそうだ','アイスを愛す','ダジャレを言ったのは誰じゃ',
			'電話に、でんわ','トマトが止まっとる','タレがたれた','スイカはやすいか？',
			'焼肉は焼きにくい','廊下にすわろうか','このタイヤ固いや','内臓がないぞう',
			'ホットケーキはほっとけー','鼻毛はなげー','ワニが輪になった','草がくさい',
			'教会にいくのは今日かい？','コンドルが口にめりこんどる','メガネをはずしたら眼がねー！',
			'庭には2羽ニワトリがいる','お金はおっかねー','言い訳をしていい訳？','漢字っていい感じ',
			'暗黒の中であんこ食う','この問題、どんなもんだい','和食がなくてわーショック',
			'飛行機の副操縦士は服装重視','アルミ缶の上にあるみかん','秋田県に住むのは飽きたけん',
			'海老の血液型はAB型','豚がぶっ倒れた','白菜はくさい',
			'隠し事を各誌ごとに書く仕事','ですます口調ですます区長','ねっとり容赦なくてネット利用者泣く',
			'佐賀市に有るか無いか探しに歩かないか？','太陽が転んで痛いよう','野口英世のグチ、ひでーよ！',
			'蟹がいる！たしかに','マイケルジョーダンがいうジョーダンはまぁいけるジョーダンだ',
			'イケアに行けや','カバが水に浮かばん','パンでパンパンや','大正天皇が鯛、しょってんのー',
			'明治天皇が目、いじってんのー','井伊直弼の名前、言い直す','朝食がまずくて超ショック',
			'コーディネートはこーでねーと','オオカミがトイレに入ったけど、おお、紙がない！',
			'クッションにくしゃみをしてハックション！','小学生は生姜くせぇ','中学生はチューがくせぇ',
			'高校生は孝行せい！','大学生は大（便）がくせぇ','平和タクシーの運転手は誰？へい！わたくしー！',
			'チキンはキチンとたべよう','ドイツが好きなのはどいつだ？','父さんが言った。ここはとうさん！',
			'父さんの会社が倒産した','この銅像ください。どうぞー','歯に詰まった鶏肉がとりにくい',
			'前髪が邪魔で前が見えん','モノレールにも乗れーる','妖怪が言った。なんか用かい？',
			'ラブレターが破れたー','バナナをたべた？そんなバナナ（ばかな）',
			'明智光秀がみかんを三つ食べた。あー！ケチ！3つ、ひでぇ！','台湾でこけて痛いわん','北海道はでっかいどー！',
			'校長先生が絶好調！','国道で屁、こくどー！','良い肉とは言いにくい']

def emphasize(text):
	return "**" + text + "**"


def underline(text):
	return "__" + text + "__"


def isContainedNoInput(command):
	for i in command:
		if i == "":
			return True
	return False

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
		com = message.content.split(" ")
		if com[1] == com_list[0]:
			await message.channel.send("現在の予定一覧")
			res = ''
			if len(times) == 0:await message.channel.send("予定...無し！w")
			for i in range(len(times)):
				res += times[i]+' '+message_list[i]+'\n'
			await message.channel.send(res)
		elif com[1] == com_list[1]:
			times.clear()
			message_list.clear()
			await message.channel.send("リセットしたよ")
		elif com[1] == com_list[2]:
			f = time_chech(com[2])
			if f == 0:await message.channel.send("「時時:分分 内容」の形式で入力してね")
			else:
				times.append(com[2])
				message_list.append(com[3])
				kosuu = 0
				if len(com) >= 5:kosuu = 1
				if kosuu == 1:
					vote_list.append(1)
					tmp_list = []
					for k in range(5,len(com)):tmp_list.append(com[k])
					choice_list.append(tmp_list)
				else:
					vote_list.append(0)
					tmp_list = []
					choice_list.append(tmp_list)
				await message.channel.send(com[2]+'に'+com[3]+'を知らせるよ')
		elif com[1] == com_list[3]:
			if com[2] in message_list:
				await message.channel.send(com[2]+'の予定を削除するよ')
				pos = 0
				for i in range(len(message_list)):
					if com[2] == message_list[i]:pos = i
				del times[pos]
				del message_list[pos]
			else:await message.channel.send('あれれ？（笑）そんな予定はないみたい')
		elif com[1] == com_list[4]:
			await message.channel.send('あそれ♪おっぱい音頭だ♪わっしょいわっしょい(^^♪\n乳輪の周りで踊りましょ♪おっぱい音頭だ♪わっしょいわっしょい♪\nでっかい乳首をしゃぶりましょ♪あそれ♪おっぱい音頭だわっしょいわっしょい♪')
		elif com[1] == com_list[5]:
			nums = []
			for i in range(len(dajare_list)):nums.append(i)
			random.shuffle(nums)
			num = random.randint(1,100)
			if num > 30:await message.channel.send('ちょっと今そういう気分じゃないんで^^;')
			else:
				for i in range(num):await message.channel.send(dajare_list[nums[i]])
		else:
			res = 'コマンド一覧'+'\n'
			for i in range(len(com_list)):res += com_list[i]+'\n'
			await message.channel.send(res)


# 60秒に一回ループ
@tasks.loop(seconds=60)
async def loop():
	# 現在の時刻
	now = datetime.now().strftime('%H:%M')
	channel = client.get_channel(CHANNEL_ID)
	for i in range(len(times)):
		if now == times[i]:
			m = times[i] +'になったよ。'+ message_list[i]+'の時間だよ。'
			await channel.send(m)
			
			if vote_list[i] == 1:
				c_siz = len(choice_list[i])
				embed = discord.Embed(title=message_list[i], description="", color=discord.Colour.green())
				for j in range(c_siz):embed.description = embed.description + list_vote[j] + ' ' + choice_list[i][j] + "\n"
				voting_msg = await channel.send(embed=embed)
				for j in range(c_siz):await voting_msg.add_reaction(list_vote[j])


#ループ処理実行
loop.start()
# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)