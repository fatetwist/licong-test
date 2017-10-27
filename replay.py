import library as xlib

content = xlib.getcatalog(input('输入关键词：'))
for x in content:
    print(x['xh'],x['book_name'])
    print(x['href'])

xh = input('输入序号以获取详细信息：')
n = int(xh)-1
href = content[n]['href']

print('正在读取',content[n]['book_name'])
