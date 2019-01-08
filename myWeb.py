from wsgiref.simple_server import make_server
import time


def fun1(req):
    with open("index1.html","rb")as f:
        data = f.read()
        return data

def fun2(req):
    with open("index2.html","rb")as f:
        data = f.read()
        return data


###################第1种##################
# def application(environ, start_response):
#     #响应头
#     start_response('200 OK', [('Content-Type','text/html')])
#
#     # print(environ)
#     path = environ['PATH_INFO'] #取出路由
#
#     if path == '/Aarom':
#         # return [b'<h1>Hello, Aarom!</h1>']
#         return [fun1()]
#     elif path == '/Ping':
#         # return [b'<h1>Hello, Peng!</h1>']
#         return [fun2()]
#     else:
#         return [b'<h1>404</h1>']
#
#     # 响应体
#     # return  [b'<h1>Hello, web!</h1>']

###################路由分发#################################

def login(req):
    # print("req:", req['QUERY_STRING'])  # req: user=2434&pwd=2233
    return b'welcome!'

def signup(req):
    pass

#增加一个时间显示
def show_time(req):
    times = time.ctime()

    #静态方法
    # return ("<h1>time:%s</h1>" %str(times)).encode("utf-8")
    # 动态加载html方法
    with open("show_time.html", "rb") as f:
        data = f.read()
        data = data.decode("utf8")
        data = data.replace("{{time}}",str(times))

        return data.encode("utf8")


def router():
    url_patterns=[

        ("/login",login),
        ("/signup",signup),
        ("/Aarom",fun1),
        ("/Ping",fun2),
        ("/show_time", show_time),

    ]
    return url_patterns;


def application(environ, start_response):
    #响应头
    start_response('200 OK', [('Content-Type','text/html')])
    path = environ['PATH_INFO']  # 取出路由

    # print(environ)
    patterns = router();

    func = None
    for item in patterns:
        if item[0] == path:
            func = item[1]
            break
    if func:
        return [func(environ)]
    else:
        return [b'<h1>404</h1>']


if __name__ == '__main__':

    httpd = make_server('', 8080, application)

    print('Serving HTTP on port 8080....')

    httpd.serve_forever()