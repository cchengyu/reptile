import requests, re, os, urllib, time
from bs4 import BeautifulSoup
from collections import deque
url = 'http://www.douban.com/' #设置爬取的URL地址
queue = deque() #创建一个空队列，deque是高效实现插入和删除的双向列表（不同于list通过索引访问元素）
visited = set() #创建一个空集合
queue.append(url) #把URL加到队列里
cnt = 0 #进行计数
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/11.0'} #设置头部，伪装成浏览器
proxies = {"http": "114.115.218.71:8118",} #设置代理
while queue: #当队列不为空时候
	url = queue.popleft() #把队列左边第一个拿出来
	visited.add(url) #拿出来之后新增到已访问的集合中
	print('已经抓取：' + str(cnt) + '正在抓取 <--- ' + url) #打印抓取了几个URL和正在抓取的URL
	print(len(queue),queue)
	print(len(visited),visited)
	cnt += 1 #计数+1
	#抓取URL里的图片
	try: #使用try...except错误处理机制
		response = requests.get(url,headers = headers,proxies = proxies, timeout = 20) #向url发送GET网络请求,返回一个response对象，赋给response变量
		soup = BeautifulSoup(response.text, 'html.parser') #创建BeautifulSoup对象，response.text为源代码字符串，指定html.parser解析器
		miimg = soup.findAll('img') #找到所有名字为img的tag
		for myimg in miimg: #用for进行遍历
			link = myimg.get('src')  #找到含有src的链接
			filepath = os.path.split(link)[1] #os.path.split把link分割成目录和文件名，取出文件名，格式为xxx.xxx
			filename = os.path.splitext(filepath)[0] #分割文件名和拓展名，取文件名，格式为xxx
			filetext = os.path.splitext(filepath)[1]#分割文件名和拓展名，取扩展名，格式为.xxx
			print(link,filename,filetext) #打印链接，文件名，拓展名
			#保存抓取下来的图片
			linker = urllib.request.urlopen(link) #打开link链接，获取响应
			content = linker.read() #读取响应内容
			with open('D:/work11'+'/'+filename+filetext,'wb') as f: #with as语句创建图片文件，存在D:/work11目录下
				f.write(content) #写入图片内容
		time.sleep(3)
	except:
		pass
	#抓取这个页面中不在队列里的URL
	get = re.compile('href="(.+?)"') #将正则表达式编译成Pattern对象，匹配以href=开头的url
	for x in get.findall(response.text): #从返回的源代码字符串匹配正则表达式的字符串，以列表形式返回
		if 'http' in x and x not in visited: #如果字符串中有http，且不再已访问集合中
			queue.append(x) #把这个url加入队列里
			print('加入队列 --->' +x) #打印加入队列信息
