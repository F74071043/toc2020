from transitions.extensions import GraphMachine

from utils import send_text_message

import random
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    def is_going_to_retype(self, event):
        text = event.message.text
        return text.lower() == "重新"
    def on_enter_retype(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入笑話 或者 撩妹 決定類型") 
        self.go_back()
    def is_going_to_joke(self, event):
        text = event.message.text
        return text.lower() == "笑話"
    def is_going_to_oil(self, event):
        text = event.message.text
        return text.lower() == "撩妹"

    def on_enter_joke(self, event):
        print("I'm entering joke")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入抽卡來開始抽笑話")

    def on_enter_oil(self, event):
        print("I'm entering oil")
        reply_token = event.reply_token
        send_text_message(reply_token, "請輸入抽卡來開始抽撩妹")    
    def is_going_to_jokedraw(self, event):
        text = event.message.text
        return text.lower() == "抽卡"

    def on_enter_jokedraw(self, event):
        print(event.message.text)
        reply_token = event.reply_token
        reply_arr=["有一天，周杰倫去唱尾牙\n一上台便說：哎呦，尾牙\n","老師：小明，麻煩你過來一下\n從此小明就變成了\n過來人\n","從前有一棵千年神木\n村裡的人都稱之為\n超齡老木\n","從前從前有一個人叫小明\n但是小明沒聽到\n","請問避孕藥的成分是什麼？？\n抗生素\n","栗子掉到地上會變成什麼？\n血淋淋的栗子\n","有兩根香蕉一起走在路上\n前面那根香蕉說：好熱喔我把衣服脫掉好了\n後面那根香蕉就跌倒惹\n"
    ,"為什麼濁水溪跟曾文溪不能在一起？\n因為他們不是河\n","太陽爸跟太陽媽生了一個小孩\n該說什麼祝賀詞？\n生日快樂\n","其實每個男人都有十二粒\n只是我們\n隱藏十粒\n","有一個脾氣很差的人\n去簽了賣身契\n從此以後他就不再生氣了","有一天，排汗衫對綿Ｔ說\n哼！我才不希罕勒～",
    "為什麼不能一邊騎馬一邊烤肉？\n因為騎中烤太難了","Ｌ的過去式是什麼？\nＬＥＤ","你侮辱我可以\n烏魯木齊就不行","從二樓跟二十樓跳樓差別在哪？\n一個是 碰！啊啊啊啊啊啊啊～～\n一個是 啊啊啊啊啊啊～～碰！",
    "小明生日，她許了三個願望\n第一個願望祝家人身體健康\n第二個願望祝我學業進步\n第三個願望不能說\n隔天小明就變成啞巴了","胖子生病最不喜歡聽到什麼話？\n保重","有一對蜈蚣夫婦他們走在路上\n手牽著手手牽著手手牽著手手牽著手\n手牽著手手牽著手手牽著手手牽著手\n手牽著手手牽著手手牽著手手牽著手\n手牽著手手牽著手手牽著手手牽著手·······",
    "沈默是金的下一句是什麼？\n晚的康橋","哪一位古代人物最會做珍珠奶茶？\n諸葛亮\n因為劉備曾對他說：先生真乃神人也","什麼東西可以同時賞大家巴掌？\n唐宋古文",
    "有一天小明撞到一位外國人\n小明：I am sorry.\n外國人：I am sorry ,too.\n小明：I am sorry three.\n外國人：What are you sorry for?\n小明：I am sorry five….","我爺爺昨天去買了一本如何改善老人痴呆症的書\n然後他今天又去買了一本",
    "什麼職業比大學生厲害？\n鎖匠\n他是研究鎖的","什麼職業最安全？\n零售商","誰的精子裡面有人\n毛利小五郎"]
        index = random.randint(0,len(reply_arr))
        ans =reply_arr[index]
        send_text_message(reply_token, ans)
        self.go_back()    

    def is_going_to_oildraw(self, event):
        text = event.message.text
        return text.lower() == "抽卡"

    def on_enter_oildraw(self, event):
        print(event.message.text)
        reply_token = event.reply_token
        reply_arr=["「猜猜我的心臟在哪邊？」\n「左邊啊！」\n「在你那邊。」","「你有兩個可愛之處。」\n「哪兩個？」\n「1.你很可愛2.我可愛你了。」","「我看人很準的。」\n「那我是什麼樣的人呢？」\n「你是...我的人。」",
        "「我可以走在你身後嗎？」\n「為什麼？」\n「因為我想做你背後的女人。」","「我其實是個不好親近的人。」\n「為什麼？」\n「不信你親親看。」","「我向來做事十拿九穩。」\n「所以呢？」\n「現在差一穩，你的吻。」",
        "你喜歡靠窗還靠走道?\n我喜歡靠著你","：我必須要來跟你說我喜歡你 \n因為我玩真心話大冒險輸了 \n：可是我選的是真心話","妳是什麼血型？\nA型，你呢\n：我是妳的理想型",
        "：欸你跑的很快嗎\n還好欸\n：那我追的到你嗎","：木頭做的門叫什麼門\n木門啊\n：那最幸福的門是什麼門\n？\n：我們","：你爸媽一定被課很多稅\n為什麼?\n：因為你笑容太奢侈","：你知道我姓什麼嗎？\n李啊不然勒\n：原本姓李 但遇見你之後姓福",
        "現在幾點了啊？\n：愛我多一點","沒有水的地方叫沙漠\n沒有妳的地方叫寂寞","「你知道我喜歡穿什麼衣服嗎？」\n「漂亮的衣服。」\n「不，是被我征服。」"]
        index = random.randint(0,len(reply_arr))
        ans =reply_arr[index]
        send_text_message(reply_token, ans)
        self.go_back()           
        



