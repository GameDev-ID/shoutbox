from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import channel
from django.utils import simplejson
import re
import pythontwitter
import datetime
import string
import oauth

application_key = "WLdDqBExrTh7QRrbRNSBvA" 
application_secret = "mjcpGlsArr1oqd0GxNeh1kQuzyBn3I7GwPmHIME"
user_token = "FILL_IN"  
user_secret = "FILL_IN"
#host = "http://localhost:8087"
host = "http://gdishoutbox.appspot.com"

callback = "%s/verify" % host

#todo: setiap ping, atau buat ping baru dengan interval yg lebih besar (tiap 5 menit misalnya)
#di tiap ping tsb, cek new thread/reply di gdi, dari rss mungkin, klo ada yg baru, broadcast

#pindah ke latest oauth
#support login via yahoo, gdi-acc, (fb?)
#di db ActiveUsers tambah field "acc_type" (twitter, yahoo, etc)
#di tiap msg chatlist, kasih icon disebelah username, icon acc_type (twitter,yahoo, etc)
#di daftar online user, kasih icon acc_type jg
#kasih command untuk ngepost status ke twit/yahoo/etc
#commandnya satu aja, /post "text here", yg nanti bakal detect acc_type dan ngepost ke service yg tersedia

#dropdown buat pengganti msg textfield, jadi past chat bisa dipilih lagi

#public todo:
#tiap ada reply/post baru di gdi, broadcast linknya ke chat (kayak fb newsfeed)
#bisa login pake yahoo,fb(?), dan gdi-account.appspot.com,tiap ngechat bisa keliatan loginnya pakai apa (ada icon service, kecil disebelah kiri/kanan username)
#bisa ngepost ke status (yahoo,twitter,fb(?)) pake command /post

arr_emo = []
arr_emo_secret = []
def addEmo(c,i,ext='.gif',secret = False):
    if secret == False:
        arr_emo.append({'c':c,'i':i + ext})
    else:
        arr_emo_secret.append({'c':c,'i':i + ext})
addEmo(':confused:','icon_confused')
addEmo(':demit:','skeleton')
addEmo(':D','icon_biggrin')
addEmo(':GPI:','icon_gpitm')
addEmo(':twisted:','icon_twisted')
addEmo(':thumb-up:','new_thumbup')
addEmo(':-D','icon_biggrin')
addEmo(':clap:','eusa_clap')
addEmo(':mrgreen:','icon_mrgreen')
addEmo('8)','icon_cool')
addEmo(':mario:','mario')
addEmo(':o','icon_surprised')
addEmo('](*,)','eusa_wall')
addEmo(':roll:','icon_rolleyes')
addEmo(':thumb-down:','new_thumbdn')
addEmo(':grin:','icon_biggrin')
addEmo('=D>','eusa_clap')
addEmo(':=D)','eusa_clap')
addEmo('8-)','icon_cool')
addEmo(':-E','gigi')
addEmo(':)','icon_smile')
addEmo(':siul:','eusa_whistle')
addEmo(':wink:','icon_wink')
addEmo(':blow-up:','new_blowingup')
addEmo(':-)','icon_smile')
addEmo(':(','icon_sad')
addEmo('#-o','eusa_doh')
addEmo(':lol:','icon_lol')
addEmo(':-p','y_10')
addEmo(':angel:','eusa_angel')
addEmo(';-)','icon_wink')
addEmo(':bad-words:','new_cussing')
addEmo(':smile:','icon_smile')
addEmo(':nangis:','nangis')
addEmo('=P~','eusa_drool')
addEmo(':x','icon_mad')
addEmo(':-p','y_10')
addEmo('=;','eusa_hand')
addEmo(':!:','icon_exclaim')
addEmo(':-\"','siul')
addEmo(':crazyeyes:','new_Eyecrazy')
addEmo(':-(','icon_sad')
addEmo(':^o','eusa_liar')
addEmo(':-x','icon_mad')
addEmo(':udut:','udut')
addEmo(':-&','eusa_sick')
addEmo(':question','icon_question')
addEmo(':n00b:','new_newbie')
addEmo(':sad:','icon_sad')
addEmo(':mad:','icon_mad')
addEmo(':---)','eusa_liar')
addEmo(':udud:','smoke','.png')
addEmo(':boohoo','eusa_boohoo')
addEmo(':idea:','icon_idea')
addEmo(':flower:','bloem12')
addEmo(':rofl:','new_rofl')
addEmo(':-o','icon_surprised')
addEmo(':kabur:','penguinkabur')
addEmo('[-X','eusa_naughty')
addEmo(':menyan:','menyan')
addEmo(':-$','eusa_shhh')
addEmo(':arrow:','icon_arrow')
addEmo(':scatter:','new_scatter')
addEmo(':shock:','icon_eek')
addEmo(':fy:','fyou')
addEmo('[-o<','eusa_pray')
addEmo(':kopi:','kopi')
addEmo(':banana:','banana')
addEmo(':-s','eusa_eh')
addEmo(':|','icon_neutral')
addEmo(':scrambleup:','new_scrambles')
addEmo(':?','icon_confused')
addEmo('!peb','alienpeb')
addEmo('=))','muahaha')
addEmo('8-[','eusa_shifty')
addEmo(':cry:','icon_cry')
addEmo(':swt:','sweat')
addEmo('\\:D/','eusa_dance')
addEmo(':-|','icon_neutral')
addEmo(':hugs:','hugs')
addEmo(':sleeping:','new_sleeping')
addEmo(':-?','icon_confused')
addEmo('$2c','2cents')
addEmo(';)','icon_wink')
addEmo('[-(','eusa_snooty')
addEmo(':evil:','icon_evil')
addEmo(':sweat:','sweat')
addEmo(':-#','eusa_silenced')
addEmo(':sembah:','nyembah')
addEmo(':fire:','new_ukliam2')
addEmo(':neutral:','icon_neutral')
addEmo(':rolleyes:','rolleyes')
addEmo(':cool:','icon_cool')
addEmo(':eek:','icon_surprised')
addEmo(':ace:','ace_ani')
addEmo(':aceheart:','aceheart_ani')
addEmo(':cizcuz:','sapi')
addEmo(':exa:','monyet')
addEmo(':heap:','stealth')
addEmo(':youfan:','pinguin')
addEmo(':eins:','puffy')
addEmo(':yinyang:','yinyang_ani')
addEmo(':soy:','soybean')
addEmo(':pompom:','pom-pom-girl')
addEmo(':semangat:','pom-pom-girl2')


#SS Emos
addEmo(':ss_UB','UB','.gif',True)
addEmo(':ss_badut','badut','.gif',True)
addEmo(':ss_bantai','bantai','.gif',True)
addEmo(':ss_bego','bego','.gif',True)
addEmo(':ss_bikingambar','bikingambar','.gif',True)
addEmo(':ss_bropeace','bropeace','.gif',True)
addEmo(':ss_cowcake','cowcake','.gif',True)
addEmo(':ss_dansamesir','dansamesir','.gif',True)
addEmo(':ss_dansa','dansa','.gif',True)
addEmo(':ss_gebukin','gebukin','.gif',True)
addEmo(':ss_hajar','hajar','.gif',True)
addEmo(':ss_jagungletup','jagungletup','.gif',True)
addEmo(':ss_kecebong','kecebong','.gif',True)
addEmo(':ss_kempes','kempes','.gif',True)
addEmo(':ss_kepalapecah','kepalapecah','.gif',True)
addEmo(':ss_ketawagila','ketawagila','.gif',True)
addEmo(':ss_ketawaserem','ketawaserem','.gif',True)
addEmo(':ss_kudabeol','kudabeol','.gif',True)
addEmo(':ss_mandi','mandi','.gif',True)
addEmo(':ss_mules','mules','.gif',True)
addEmo(':ss_ngacay','ngacay','.gif',True)
addEmo(':ss_nguantuk','nguantuk','.gif',True)
addEmo(':ss_sniper','sniper','.gif',True)

##PLEMO emos
addEmo(':plemo_annoyed','pl_icons/annoyed','.gif',True)
addEmo(':plemo_big_eyed','pl_icons/big_eyed','.gif',True)
addEmo(':plemo_brokenheart','pl_icons/brokenheart','.gif',True)
addEmo(':plemo_cool','pl_icons/cool','.gif',True)
addEmo(':plemo_dance','pl_icons/dance','.gif',True)
addEmo(':plemo_defaultsmall','pl_icons/defaultsmall','.gif',True)
addEmo(':plemo_drinking','pl_icons/drinking','.gif',True)
addEmo(':plemo_girlkiss','pl_icons/girlkiss','.gif',True)
addEmo(':plemo_gril_toungue','pl_icons/gril_toungue','.png',True)
addEmo(':plemo_hassle','pl_icons/hassle','.gif',True)
addEmo(':plemo_idiot','pl_icons/idiot','.gif',True)
addEmo(':plemo_laugh','pl_icons/laugh','.gif',True)
addEmo(':plemo_listening_music','pl_icons/listening_music','.gif',True)
addEmo(':plemo_money','pl_icons/money','.gif',True)
addEmo(':plemo_nottalking','pl_icons/nottalking','.gif',True)
addEmo(':plemo_private-lock','pl_icons/private-lock','.png',True)
addEmo(':plemo_sad','pl_icons/sad','.gif',True)
addEmo(':plemo_sick','pl_icons/sick','.gif',True)
addEmo(':plemo_smile','pl_icons/smile','.gif',True)
addEmo(':plemo_tears','pl_icons/tears','.gif',True)
addEmo(':plemo_tongue','pl_icons/tongue','.gif',True)
addEmo(':plemo_wave','pl_icons/wave','.gif',True)
addEmo(':plemo_yupi','pl_icons/yupi','.gif',True)
addEmo(':plemo_applause','pl_icons/applause','.gif',True)
addEmo(':plemo_bringiton','pl_icons/bringiton','.gif',True)
addEmo(':plemo_broken_heart','pl_icons/broken_heart','.gif',True)
addEmo(':plemo_cozy','pl_icons/cozy','.gif',True)
addEmo(':plemo_dancingmoves','pl_icons/dancemoves','.gif',True)
addEmo(':plemo_devil','pl_icons/devil','.gif',True)
addEmo(':plemo_fever','pl_icons/fever','.gif',True)
addEmo(':plemo_girl_kiss','pl_icons/girl_kiss','.gif',True)
addEmo(':plemo_grin','pl_icons/grin','.gif',True)
addEmo(':plemo_heart','pl_icons/heart','.gif',True)
addEmo(':plemo_joyful','pl_icons/joyful','.gif',True)
addEmo(':plemo_likefood','pl_icons/likefood','.gif',True)
addEmo(':plemo_lol','pl_icons/lol','.gif',True)
addEmo(':plemo_not_talking','pl_icons/not_talking','.gif',True)
addEmo(':plemo_music','pl_icons/music','.gif',True)
addEmo(':plemo_rock','pl_icons/rock','.gif',True)
addEmo(':plemo_scenic','pl_icons/scenic','.gif',True)
addEmo(':plemo_silly_couple','pl_icons/silly_couple','.gif',True)
addEmo(':plemo_startled','pl_icons/startled','.gif',True)
addEmo(':plemo_thinking','pl_icons/thinking','.gif',True)
addEmo(':plemo_unsure','pl_icons/unsure','.gif',True)
addEmo(':plemo_wink','pl_icons/wink','.gif',True)
addEmo(':plemo_angry','pl_icons/angry','.gif',True)
addEmo(':plemo_bigeyed','pl_icons/bigeyed','.gif',True)
addEmo(':plemo_bring_it_on','pl_icons/bring_it_on','.gif',True)
addEmo(':plemo_bye','pl_icons/bye','.gif',True)
addEmo(':plemo_crying','pl_icons/crying','.gif',True)
addEmo(':plemo_dancing_moves','pl_icons/dance_moves','.gif',True)
addEmo(':plemo_doh','pl_icons/doh','.gif',True)
addEmo(':plemo_fingerscrossed','pl_icons/fingerscrossed','.gif',True)
addEmo(':plemo_griltoungue','pl_icons/griltoungue','.png',True)
addEmo(':plemo_gym','pl_icons/gym','.gif',True)
addEmo(':plemo_hungry','pl_icons/hungry','.gif',True)
addEmo(':plemo_kiss','pl_icons/kiss','.gif',True)
addEmo(':plemo_like_food','pl_icons/like_food','.gif',True)
addEmo(':plemo_lonely','pl_icons/lonely','.gif',True)
addEmo(':plemo_nerd','pl_icons/nerd','.gif',True)
addEmo(':plemo_party','pl_icons/party','.gif',True)
addEmo(':plemo_metal','pl_icons/rock_n_roll','.gif',True)
addEmo(':plemo_scouple','pl_icons/scouple','.gif',True)
addEmo(':plemo_sleeping','pl_icons/sleeping','.gif',True)
addEmo(':plemo_surprised','pl_icons/surprised','.gif',True)
addEmo(':plemo_tired','pl_icons/tired','.gif',True)
addEmo(':plemo_w00t','pl_icons/w00t','.gif',True)
addEmo(':plemo_worship','pl_icons/worship','.gif',True)

class ActiveUsers(db.Model):
    username = db.StringProperty(multiline=True)
    token = db.StringProperty(multiline=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_updated = db.DateTimeProperty(auto_now_add=True)
    diff_sec = db.IntegerProperty()
    
class ChatData(db.Model):
    usr = db.TextProperty()
    msg = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class ping(webapp.RequestHandler):
    def updatePingData(self):
        #delete zombie channel, update non zombie channel 
        users = db.GqlQuery("SELECT * FROM ActiveUsers")
        for user in users:
            user.diff_sec = (datetime.datetime.now() - user.last_updated).seconds
            if user.diff_sec > 60 * 3: #3 mins               
                usr_ch_count = db.GqlQuery("SELECT * FROM ActiveUsers WHERE username='" + user.username + "'").count(1000)
                if user.username != "__anonymous":
                    if usr_ch_count == 1:
                        chat = ChatData()
                        chat.usr = ''
                        chat.msg = user.username + " left the chat (request timed out)"
                        chat.date = user.last_updated
                        chat.put()                    
                        cp = ChatPost()
                        cp.chatlist()
                user.delete()
            else:
                user.put()
    def post(self):
        token = self.request.get('token')        
        users = db.GqlQuery("SELECT * FROM ActiveUsers WHERE token='" + token + "'")
        username = ''
        created = ''
        for user in users:
            if username == '':
                username = user.username
                created = str(user.created)             
            user.last_updated = datetime.datetime.now()
            user.put()
        
        #delete zombie channel, update non zombie channel 
        self.updatePingData()
        
        #show online users
        users = db.GqlQuery("SELECT * FROM ActiveUsers")
        arr_users = []
        for user in users:
            found = False
            tmp_username = user.username
            if tmp_username == "__anonymous":
                tmp_username = "(Anonymous)"
            for a in arr_users:
                if a['usr'] == tmp_username:
                    a['ch']+=1
                    found = True
            if found==False:
                arr_users.append({'usr':tmp_username,'ch':1})
            
        output = template.render('userlist.html', {'users' : arr_users})        
        
        output_users = {
                        'return_type' : 'userlist',
                        'data' : output
                        }
        users_json = simplejson.dumps(output_users)
        try:
            channel.send_message(username + created, users_json)
        except channel.InvalidChannelClientIdError:
            pass
        
            
class ChatPost(webapp.RequestHandler):
    def processMsg(self,usr,msg,fdate):
        msg += " "
        
        #html escape
        msg = msg.replace("<","&lt;")
        msg = msg.replace("<","&gt;")
        
        
        arr_msg = msg.split(' ',1)        
        
        #all first command action (/me, /tweet, etc)
        if arr_msg[0] == "/me":  
            msg = "<b><span class='me'>*" + usr + " " + arr_msg[1] + "*</span></b>"
            usr = " "
        elif arr_msg[0] == "/fake": # ~username: msg (real username) (pdate style)
            if len(msg.split(' ',2)) >= 3:
                arr_fake = msg.split(' ',2)
                fake_usr = arr_fake[1]
                fake_msg = arr_fake[2]
                real_usr = usr
                
                usr = fake_usr
                msg = fake_msg + "<span class='pdate'>(" + real_usr + ")</span>"
                
        
        if usr !="" and usr !=" ": #if this is not chat sys message
            msg = " : " + msg
        
        #all middle command (:imgbin_xxx:)
        arr_msg = msg.split(' ')
        msg = ""
        for m in arr_msg:            
            raw_cmd = m.split(':')
            if len(raw_cmd) == 3: # this is a valid command, having no spaces and 2 ":"
                cmd = raw_cmd[1]
                raw_cmd2 = cmd.split('_')
                if len(raw_cmd2) == 2: # this is a valid command, having 1 "_"
                    cmd_name = raw_cmd2[0]
                    cmd_param = raw_cmd2[1]
                    if cmd_name == "imgbin":
                        if cmd_param !="":
                            msg += " " + "<a href='http://imgbin.gamedevid.org/view/" + cmd_param + "/'><img src='http://imgbin.gamedevid.org/i/" + cmd_param + "_tn' border='0' align='none' alt='" + cmd_param + "' title='" + cmd_param + "'/></a>"
                        else:
                            msg += " " + m
                else: # this is not a valid command, treat it as normal message
                    msg += " " + m
            else: # this is not a valid command, treat it as normal message
                msg += " " + m
        #emoticons (:penguin:), dan hidden (:kabur:)
        #cuman yg hidden nggak ditampilin di emo list, dan di db tagnya harus beda sama nama filenya
        #contoh untuk tag kabur, nama filenya penguinlari.gif
                
        for emo in arr_emo:
            msg = msg.replace(emo['c'],"<img src='/res/" + emo['i'] + "' title='" + emo['c'] +"' alt='" + emo['c'] +"'>")
        for emo in arr_emo_secret:
            msg = msg.replace(emo['c'],"<img src='/res/" + emo['i'] + "' title='Emoticon rahasia' alt='Emoticon rahasia'>")
        
        mention = re.compile(r"""\B@([0-9a-zA-Z_]+)""")
        hash = re.compile(r"""\B#([0-9a-zA-Z_]+)""")
        msg = mention.sub(r'@<a href="http://twitter.com/#!/\1"><b>\1</b></a>', msg)
        msg = hash.sub(r'<a href="http://twitter.com/#!/search?q=%23\1"><b>#\1</b></a>', msg)
        
        """
        #mention tweet @username
        arr_msg = msg.split(' ')
        msg = ""
        for m in arr_msg:
            raw_code = m.split('@')
            valid = False
            if len(raw_code)==2:
                if raw_code[0]=='':
                    if raw_code[1]!='': #valid mention
                        valid = True
                        tweet_username = raw_code[1]
                        msg += " " + "@<a href='http://twitter.com/#!/" + tweet_username + "'><b>" + tweet_username + "</b></a>"
            if valid == False:
                msg += " " + m
        
        #mention hashtag #hashtag
        arr_msg = msg.split(' ')
        msg = ""
        for m in arr_msg:
            raw_code = m.split('#')
            valid = False
            if len(raw_code)==2:
                if raw_code[0]=='':
                    if raw_code[1]!='': #valid mention
                        valid = True
                        tweet_username = raw_code[1]
                        msg += " " + "<a href='http://twitter.com/#!/search?q=%23" + tweet_username + "'><b>#" + tweet_username + "</b></a>"
            if valid == False:
                msg += " " + m
        """
        
        #parse url
        #http://
        #if only www., then automatically add http://
        arr_msg = msg.split(' ')
        msg = ""
        for m in arr_msg:
            raw_code = m.split('www.')
            if len(raw_code) == 2:
                if raw_code[0] == '':
                    if raw_code[1]!='': #a valid www.
                        m = 'http://' + m
            
            raw_code = m.split('http://')
            valid = False
            if len(raw_code) == 2:
                if raw_code[0] == '':
                    if raw_code[1] != '': # a valid http://
                        valid = True
                        url = raw_code[1]
                        msg += " " + "<a href='" + m + "'>" + raw_code[1] + "</a>"
            
            if valid == False:
                msg += " " + m
                
        return {'usr':usr,'msg':msg,'date':fdate}
    def chatlist(self,archive=False):
        limit = 30
        if archive == True:
            limit = 9999
        chats_data = db.GqlQuery("SELECT * FROM ChatData ORDER BY date DESC LIMIT 0," + str(limit)).fetch(limit,0)
        chats = [];
        for c in chats_data:
            fdate = c.date.strftime("%m %d,%Y %H:%M:%S")
            chats.append(self.processMsg(c.usr,c.msg,fdate))
            
        output = template.render('chatlist.html', {'chats' : chats})
        if archive == True:
            return output
        chatUpdate = {
                      'return_type' : 'chatlist',
                      'data' : output
                      }
        chats_json = simplejson.dumps(chatUpdate)
        
        userlist = db.GqlQuery("SELECT * FROM ActiveUsers")
        for user in userlist:     
            channel.send_message(user.username + str(user.created), chats_json)
        return 0
    def post(self):        
        client = oauth.GDIClient(application_key, application_secret, callback,self)
        if client.get_cookie():
            if self.request.get('message')!="":                
                username = client.get_cookie_username()
                chat = ChatData()
                chat.usr = username
                chat.msg = self.request.get('message')        
                chat.put()
        self.chatlist()
        
class ChatArchive(webapp.RequestHandler):
    def get(self):        
        cp = ChatPost()
        self.response.out.write(cp.chatlist(True))
        
class ChatExit(webapp.RequestHandler):
    def get(self):
        client = oauth.GDIClient(application_key, application_secret, callback,self)
        
        username = client.get_cookie_username()
        user_ch = db.GqlQuery("SELECT * FROM ActiveUsers WHERE username='" + username + "'")
        for user in user_ch:
            user.delete()
        chat = ChatData()
        chat.usr = ''
        chat.msg = username + " left the chat (log out via GDI Account)" 
        chat.put()
        cp = ChatPost()
        cp.chatlist()                
        client.expire_cookie()
        return self.redirect("/")  
class MainPage(webapp.RequestHandler):
    def get(self,mode=""):
        
        #client = pythontwitter.OAuthClient('twitter', self)       
        client = oauth.GDIClient(application_key, application_secret, callback,self)
        if mode == "login":
            return self.redirect(client.get_authorization_url())        
        if mode == "verify":
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            user_info = client.get_user_info(auth_token, auth_verifier=auth_verifier)
            return self.redirect("/")
            
        nickname = ""
        new_token = ""
        if client.get_cookie():
            #info = client.get('/account/verify_credentials')
            #nickname = info['screen_name']
            nickname = client.get_cookie_username()
        else:
            nickname = "__anonymous"
        
        user = ActiveUsers()
        user.username = nickname
        user.created = datetime.datetime.now()
        user.token = channel.create_channel(nickname + str(user.created))
        user.diff_sec = 0     
        new_token = user.token
        user.put()
        
        #case: gw close tab, 3 menit lalu RTO, trus buka lagi, nggak ada message " has joined the chat"
        #harusnya ada message "gw has left the chat (last_updated)"
        #trus dibawahnya ada message "gw has joined the chat (waktu sekarang)"
        #penyebab: karna region dibawah ini dipanggil duluan sebelum ping
        #jadi sementara channel gw yg harusnya RTO masih ada di db, MainPage jg nambah 1 row
        #baru yaitu channel baru gw. dengan total lebih dari 1 channel, conditional statetement dibawah
        #gak bakal dieksekusi
        
        #gimana caranya mekanisme ping dibagian ngedelete zombie channel bisa di eksekusi lebih dulu
        #sebelum region dibawah ini jalan. solusi: pisahkan fungsi delete zombie channel di kelas ping
        #lalu panggil disini
        
        p = ping()
        p.updatePingData()
        
        if nickname != "__anonymous":
            usr_ch_count = db.GqlQuery("SELECT * FROM ActiveUsers WHERE username='" + nickname + "'").count(1000)        
            if usr_ch_count == 1:
                chat = ChatData()
                chat.usr = ''
                chat.msg = nickname + " has joined the chat"
                chat.put()
    
        
        cp = ChatPost()
        cp.chatlist()    
         
        output = template.render('index.html', {'new_nickname' : nickname, 'new_token' : new_token, 'arr_emo' : arr_emo})
        self.response.out.write(output)
        
application = webapp.WSGIApplication(
                                     [
                                      ('/oauth/(.*)/(.*)', pythontwitter.OAuthHandler),
                                      ('/ping', ping),
                                      ('/archive', ChatArchive),                                      
                                      ('/logout', ChatExit),                                 
                                      ('/chatpost',ChatPost),                                      
                                      ('/(.*)', MainPage)],                                      
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()