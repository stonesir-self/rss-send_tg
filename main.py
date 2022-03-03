# -*- coding: UTF-8 -*-
import feedparser
import telegram
from apscheduler.schedulers.blocking import BlockingScheduler
# proxy = urllib.request.ProxyHandler({"http":"127.0.0.1:30809"})
# sys.path.append(r'C:\Users\蒙轩Sir\Desktop\python 工作区\salary\salary2')
# os.system('pause')
# code.interact(banner="", local=locals())
import os
# os.environ["http_proxy"] = "http://127.0.0.1:30809"
# os.environ["https_proxy"] = "http://127.0.0.1:30809"
# time.sleep(random.randrange(2, 5))
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

# 生成特定list, 特定
def into_list(list,name,gs):
    result=[]
    for i in list[:gs]:
        result.append(i[name])
    return result

# 发送文字，用\n换行,lx=html,markdown,markdown_v2
def t_text(text,chat_id,token,dl='n',lx=''):
    proxy = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:30808')
    if dl=='y':
        bot=telegram.Bot(token=token,request=proxy)
    else:
        bot=telegram.Bot(token=token)
    if lx=='':
        lx_=''
    else:
        lx_u=lx.upper()
        # lx_=f"telegram.ParseMode.{lx_u}"
        lx_=lx_u
    bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=lx_
    )

# 写入列表到txt
def w_txt(name,list,wj='./'):
    f = open(f'{wj}{name}.txt', 'w', encoding='utf-8-sig', newline='')
    for u in list:
        f.write(u+'\n')
    f.close()
    print('写入txt成功！')
# 读取文件到str
def txt_str_direct(name,wj='./'):
    text=''
    f = open(f'{wj}{name}.txt', 'r', encoding='utf-8-sig', newline='')
    for i in f:
        text=text+i
    f.close()
    return text

# 生成所有数据
def all_sj(list1,list2):
    text=''
    for i in range(len(list1)):
        text=text+'['+str(list1[i]).replace('[','').replace(']','')+']'+'('+str(list2[i])+')'+'\n\n'
    return text
    
# 生成所有数据（list）
def all_sj_l(list1,list2):
    list=[]
    for i in range(len(list1)):
        list.append('['+str(list1[i]).replace('[','').replace(']','')+']'+'('+str(list2[i])+')'+'\n\n')
    return list

# 批量执行函数，特定
def list_zxhs_2(hs,list,gs,first=False):
    for i in list:
        if first:
            hs(i,gs,first=True)
        else:
            hs(i,gs)

# 为每个列表元素执行函数
def list_zxhs(hs,list):
    for i in list:
        hs(i)

# 写入列表到txt(追加),会创建
def a_txt(name,list,wj='./'):
    f = open(f'{wj}{name}.txt', 'a', encoding='utf-8-sig', newline='')
    for u in list:
        f.write(u+'\n')
    f.close()
    print('写入txt成功！')

# 检测没有文件就创建文件
def mk_none_file(name):
    lbwj='./tmp/'+name.split(',')[0]+'.txt'
    if not os.path.exists(lbwj):
        f=open(lbwj, "w")
        f.close()

# 检测是否有不存在的文件
def list_exist_file(list):
    for name in list:
        lbwj='./tmp/'+name.split(',')[0]+'.txt'
        if not os.path.exists(lbwj):
            return False
    return True


# 检查list是否有元素(区分大小写)在str中,返回不在的
def check_list_in_str(list,str):
    list_=[]
    for i in list:
        if i not in str:
            list_.append(i)
    return list_

#txt到list,没有'\n',''
def w_txt_list(name,wj='./'):
    list=[]
    f = open(f'{wj}{name}.txt', 'r', encoding='utf-8-sig', newline='')
    # 不带\n
    for u in f:
        if u == '': continue
        list.append(u.split('\n')[0]+'\n\n')
    f.close()
    print('读取txt成功！')
    return list

#txt到list_原版,没有'\n','',纯文字
def w_txt_list_o(name,wj='./'):
    list=[]
    f = open(f'{wj}{name}.txt', 'r', encoding='utf-8-sig', newline='')
    for u in f:
        if u == '': continue
        list.append(u.split('\n')[0])
    f.close()
    return list

#txt到str原版
def w_txt_str(name,wj='./'):
    str=''
    f = open(f'{wj}{name}.txt', 'r', encoding='utf-8-sig', newline='')
    for u in f:
        if u == '': continue
        str=str+u.split('\n')[0]
    f.close()
    return str

def hqsj(url,gs,first=False):
    # 所有list的item都以'\n\n'结尾
    rss_x = feedparser.parse(url.split(',')[1])
    # 条目
    item = into_list(rss_x['entries'],'title',gs)
    # 条目链接
    item_link = into_list(rss_x['entries'],'link',gs)
    # item_all=all_sj(item,item_link)
    item_all_l=all_sj_l(item,item_link)
    item_original=w_txt_list(url.split(',')[0],wj='./tmp/')
    list3=[i for i in set(item_all_l)-set(item_original)]
    i=0
    if not first:
        day_all_tmp=w_txt_list(url.split(',')[0]+'-day_all',wj='./tmp/')
        if day_all_tmp==[]:
            a_txt(url.split(',')[0]+'-day_all',item_all_l,wj='./tmp/') 
            i=1
    if list3 == [] and not first:
        return
    w_txt(url.split(',')[0],item_all_l,wj='./tmp/')
    if first:
        list3=item_all_l.copy()
        list3.insert(0,url.split(',')[0]+'-目前最新!\n\n')
        list3=list3[:2]
        a_txt('tmp',list3,wj='./tmp/')
        a_txt(url.split(',')[0]+'-day_all',item_all_l,wj='./tmp/')
        a_txt(url.split(',')[0]+'-day',list3[1:],wj='./tmp/')
    else:
        if i==0:
            list3=check_list_in_str(list3,day_all_tmp)
            if list3 == []:
                return
            else: 
                a_txt(url.split(',')[0]+'-day_all',list3,wj='./tmp/')
        if item_all_l.index(list3[0]) !=0:
            return
        list3.insert(0,url.split(',')[0]+'-更新啦!\n\n')
        a_txt('tmp',list3,wj='./tmp/')
        a_txt(url.split(',')[0]+'-day',list3[1:],wj='./tmp/')

# 判断文件是否为空
def file_is_none(name,wj='./'):
    if not os.path.getsize(wj+name+'.txt'):
        return True
    else:
        return False

# 发送通知
def fstz():
    t_text(txt_str_direct('tmp',wj='./tmp/'),lx='markdown',chat_id=tg_info[0].split('=')[1],token=tg_info[1].split('=')[1])
    # 清空tmp
    f=open('./tmp/tmp.txt', "w")
    f.close()

# 今日订阅汇总
def hz_list(list,wj='./'):
    all='今日订阅汇总\n\n'
    for u in list:
        mc=u.split(',')[0]
        if '[' in txt_str_direct(mc+'-day',wj='./tmp/'):
            all=all+f'{mc}\n\n'+txt_str_direct(mc+'-day',wj='./tmp/')
    return all

# 18:00 通知
def time_tz():
    all=hz_list(url,wj='./tmp/')
    t_text(all,chat_id=tg_info[0].split('=')[1],token=tg_info[1].split('=')[1],lx='markdown')
    clear_day(url)

# 删除今日day_tmp,day_all_tmp
def clear_day(url):
    for i in url:
        mc=i.split(',')[0]
        f=open(f'./tmp/{mc}-day.txt', "w")
        f.close()
        f=open(f'./tmp/{mc}-day_all.txt', "w")
        f.close()

# 主运行函数
def main(first=False):
    global url
    url=w_txt_list_o('rss')
    if not list_exist_file(url):
        list_zxhs(mk_none_file,url)
        clear_day(url)
        main(first=True)
        return
    if first:
        list_zxhs_2(hqsj,url,5,first=True)
    else:
        list_zxhs_2(hqsj,url,5)
    if not file_is_none('tmp',wj='./tmp/') and '[' in w_txt_str('tmp',wj='./tmp/'):
        fstz()


if __name__ == '__main__':
    os.chdir(os.getcwd())
    url=w_txt_list_o('rss')
    tg_info=w_txt_list_o('tg')
    lblj='./tmp'
    if not os.path.exists(lblj):
        os.makedirs(lblj)
    # 检测是否存在文件
    list_zxhs(mk_none_file,url)
    # 清空day_tmp
    clear_day(url)
    main(first=True)
    sched = BlockingScheduler(timezone="Asia/Shanghai")

    # sched.add_job(list_zxhs_,'cron',second='*/60',args=[hqsj,url,10])
    sched.add_job(main,'interval',seconds=20)

    # 18:00通知
    # sched.add_job(list_zxhs_,'cron',hour=18,minute=0,second=0,args=[hqsj,url,10])
    sched.add_job(time_tz,'cron',hour=18,minute=0,second=0)

    # 清除每天day_tmp
    sched.add_job(clear_day,'cron',hour=18,minute=1,second=0,args=[url])

    try:
        sched.start()
    except:
        sched.shutdown(wait=False)