# markbj
一个开源的知识分享平台 http://www.markbj.com

# 安装说明

## 安装依赖包
	pip install -r requirements.txt

## 初始化数据库
	python manage.py db init
	python manage.py db migrate
	python manage.py db upgrade

## 启动程序
	python manage.py runserver -h 0.0.0.0

# 特点:

- 编写文章
- 优秀的在线编辑器
- 支持markdown
- 使用标签管理文章
- 导入外部数据

## 编辑器

编辑器由四个部分组成：工具栏、状态栏、编辑区、预览区

![编辑器](http://uploadimg.markbj.com/static/resource/image/book/b5047452225111e7affb00163e13356e.png)

## 导入网页内容
用户如果在网络上发现感兴趣的内容，可以将网页内容导入到马克笔记中，方便下次观看；通过点击工具栏上导入按钮，会弹出导入对话框。

![导入内容菜单](http://uploadimg.markbj.com/static/resource/image/book/8b031e80227211e798b600163e13356e.png)

导入的方式分两种：
- 链接导入
- 内容导入

### 链接导入
将浏览页面的链接复制到链接地址中 点击确定后就能自动在编辑区导入页面的内容

![链接导入](http://uploadimg.markbj.com/static/resource/image/book/ec8774cc227111e798b600163e13356e.png)

### 内容导入
用户也可以将页面的HTML代码复制到内容导入的输入框，点击确定后就能自动在编辑区导入页面的内容

![内容导入](http://uploadimg.markbj.com/static/resource/image/book/c89b07fc227311e798b600163e13356e.png)

# 建议反馈

如果您有任何建议和问题，可以通过网站的反馈页面反馈我们，或者通过以下方式联系我们

我们非常感谢您的反馈

- 邮箱： chaijun@markbj.com

