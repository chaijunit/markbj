#coding: utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'markbj key'
    # 每次request后数据库自动调用commit
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'markbj.sqlite')

    UPLOADIMG_HOST = ""

    # 图片路径
    IMG_PATH = 'static/img'         # 常规图片存放地方
    AVATAR_IMAGE_PATH = 'static/resource/image/avatar'      # 用户头像路径
    COVER_IMAGE_PATH = 'static/resource/image/cover'        # 用户封面图片路径

    ARTICLE_IMAGE_PATH = 'static/resource/image/article'    # 文章图片路径

    TMP_PATH = 'static/resource/tmp'                        # 临时文件目录

    # 页面内容书
    SEARCH_PAGE = 10
    AUTOSEARCH_TOPIC_PAGE = 20
    # HOME_PAGE = 10
    # TOPIC_ARTICLE_PAGE = 10
    # TOPIC_BOOK_PAGE = 15
    USER_PAGE = 10
    USER_TOPIC_PAGE = 20
    # 文章列表页
    ARTICLE_PAGE = 20

    # 预览专题个数
    # 在文章、书籍列表的头部显示的专题个数
    PREVIEW_TOPIC_NUM = 25

    # 搜索配置
    SEARCH_TOPIC_SIZE = 20  # 搜索索引的排行列表


class DevelopmentConfig(Config):
    DEBUG = True


class DeploymentConfig(Config):
    DEBUG = False


config = {
    "default":DevelopmentConfig,
    "deploy": DeploymentConfig
}


