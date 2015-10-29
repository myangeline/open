# Bottle学习笔记
bottle官方文档：http://bottlepy.org/docs/dev/tutorial.html

## hello world

	from bottle import route, run

	@route('/hello')
	def hello():
		return "Hello World!"
	
	run(host='localhost', port=8080, reload=True, debug=True)

保存为hello.py，然后直接运行这个文件即可。在浏览器中访问 http://localhost:8080/hello ，将会看到 Hello World!，这样就成功啦！

另一种方式的hello world，只是稍作修改

	from bottle import Bottle, run

	app = Bottle()
	
	@app.route('/hello')
	def hello():
		return "Hello World!"
	
	run(app, host='localhost', port=8080)
	# 下面这样也可以运行哦
	# app.run(host='localhost', port=8080, reloader=True)
这样可能会稍微清晰点，反正无所谓了，都是hello world，能工作就好，bottle的源码就一个文件，看看源码就知道这两种方式的了



## Request Routing
在上面的代码中 `@route('/hello')` 就是一个请求路由了，如下：

	@route('/hello')
	def hello():
		return "Hello World!"

其实`route()`是一个装饰器，所以可以给一个方法添加多个路由装饰器，这样就可以有多个方式访问同一个方法
	
	@route('/')
	@route('/hello/<name>')
	def greet(name='Stranger'):
		return template('Hello {{name}}, how are you?', name=name)

上面的例子中，使用了关键字`name`，这个方法中的name是一个参数，也是动态路由的方式，如下：
	
	@route('/wiki/<pagename>')            # matches /wiki/Learning_Python
	def show_wiki_page(pagename):
		...
	
	@route('/<action>/<user>')            # matches /follow/defnull
	def user_api(action, user):
		...

在路由中可以使用`filter`，一个过滤器定义成`<name:filter>`或者`<name:filter:config>`这样，`config`参数依赖`filter`作为可以选项
下面是bottle自带的过滤器：
	
- **:int** 匹配integer类型
- **:float** 匹配float、double、decimal类型
- **:path** matches all characters including the slash character in a non-greedy way and can be used to match more than one path segment.
- **:re** 可以使用自定义正则表达式类进行匹配

下面是几个典型应用：
	
	@route('/object/<id:int>')
	def callback(id):
		assert isinstance(id, int)
	
	@route('/show/<name:re:[a-z]+>')
	def callback(name):
		assert name.isalpha()
	
	@route('/static/<path:path>')
	def callback(path):
		return static_file(path, ...)
		

路由中参数的写法是有变化的，尽量不要使用旧的写法，具体参考[官方文档](http://bottlepy.org/docs/dev/tutorial.html#dynamic-routes)

除了官方内置的`filter`，也可以自定义`filter`，方法如下：
	
	app = Bottle()

	def list_filter(config):
		''' Matches a comma separated list of numbers. '''
		delimiter = config or ','
		regexp = r'\d+(%s\d)*' % re.escape(delimiter)
	
		def to_python(match):
			return map(int, match.split(delimiter))
	
		def to_url(numbers):
			return delimiter.join(map(str, numbers))
	
		return regexp, to_python, to_url
	
	app.router.add_filter('list', list_filter)
	
	@app.route('/follow/<ids:list>')
	def follow_users(ids):
		for id in ids:
			...
	
自定义的`filter`需要具备三个条件：
1. a regular expression string
2. a callable to convert the URL fragment to a python value
3. a callable that does the opposite

最后，路由装饰器也可以被当做方法直接调用，这样可以更加灵活的应用

	def index():
		return 'hello world'
		
	
	def setup_routing(app):
		app.route('/index', 'GET', index)
		app.route('/edit', ['GET', 'POST'], form_edit)

	app = Bottle()
	setup_routing(app)
	app.run(host='localhost', port=8080, reloader=True)
实际上，任何的`Bottle`实例的路由都可以使用这种方式初始化，这种方式在python的其他框架中都是很常见的，例如 `web.py`、`tornado`等都是可以这样配置路由


## response

Bottle中的response，对应于每个请求，可以设置header、cookies等

返回一个json格式的数据：
	
	@route('/json')
	def get_json():
		# response.set_header('Content-Type', 'application/json')
		# return json.dumps({'name': 'aaa', 'age': 20})		
		return {'name': 'aaa', 'age': 20}
		
上面的方法可以返回一个json格式的数据，如果return的是一个dict或者dict的子类，Bottle会默认的将 `Content-Type` 设置成 `application/json`，
也可以自己转换成json格式的字符串返回


## request

pass


## Templates

Bottle自带一个模版系统 `SimpleTemplate Engine`，可以使用 `template()` 方法或者 `view()` 装饰器来渲染一个模版页面
	
	