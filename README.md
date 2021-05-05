# TODO

## 布局

### 控件

- [ ] 鼠标悬浮翻转卡片

# FUNCTIONS

* request.session
* 数据标注，即工作台
  * 是否已经三人标记
  * 该处理时是否到第一个，最后一个的提醒
  * 下次登录从上一次退出的地方继续编辑
  * 计算列，即对象的方法，写在model里的def
* stanford-corenlp简单标注,table呈现，root white-space: pre-wrap呈现
* wordcloud 词云
* snownlp sentiments

# CHANGES

## name

* stanford-corenlp-4.2.0   --->   stanford-corenlp
* 修改了wordcloud的字体以解决中文乱码

# TIPS

* 判断是不是int/str ==isinstance(request.POST['docitemid'], int)==