# SE_01
软工个人作业

---

[Github链接](https://github.com/bin1161636325/SE_01) 

# 一、PSP表格 

**(2.1)在开始实现程序之前，在附录提供的PSP表格记录下你估计将在程序的各个模块的开发上耗费的时间。（3'） **

**(2.2)在你实现完程序之后，在附录提供的PSP表格记录下你在程序的各个模块上实际花费的时间。 （3'）**

| PSP2.1                               | Personal Software Process Stages        | 预估耗时（分钟） | 实际耗时（分钟） |
| :----------------------------------- | :-------------------------------------- | ---------------- | :--------------- |
| Planning                             | 计划                                    |                  |                  |
| ·Estimate                            | ·估计这个任务需要多少时间               | 2500             | 2100             |
| Development                          | 开发                                    |                  |                  |
| ·Analysis                            | ·需求分析（包括学习新技术）             | 500              | 180              |
| ·Design Spec                         | ·生成设计文档                           | 40               | 80               |
| ·Design Review                       | ·设计复审                               | 10               | 20               |
| ·Coding Standard                     | ·代码规范（为目前的开发制定合适的规范） | 50               | 50               |
| ·Design                              | ·具体设计                               | 600              | 240              |
| ·Coding                              | ·具体编码                               | 1040             | 1200             |
| ·Code Review                         | ·代码复审                               | 60               | 30               |
| ·Test                                | ·测试（自我测试，修改代码，提交修改）   | 200              | 300              |
| Reporting                            | 报告                                    |                  |                  |
| ·Test Repor                          | ·测试报告                               | 60               | 30               |
| ·Size Measurement                    | ·计算工作量                             | 60               | 60               |
| ·Postmortem & Process Improment Plan | ·事后总结，并提出过程改进计划           | 90               | 30               |
|                                      | ·合计                                   | 2710             | 2280             |

# 二、任务要求的实现 

**(3.1)项目设计与技术栈。**从阅读完题目到完成作业，这一次的任务被你拆分成了几个环节？你分别通过什么渠道、使用什么方式方法完成了各个环节？列出你完成本次任务所使用的技术栈。 （5'）

>一、爬虫
>
>>技术栈：
>>
>>>+ Python + Selenium + Pyppeteer 
>>
>>渠道：
>>
>>>+ B站，CSDN， 博客园， GITHUB， 官网API
>>
>>方法：
>>
>>>+ 先用pyppeteer获取网页，然后用BeautifulSoup解析网页，最后将网页的内容进行数据处理
>
>二、数据处理
>
>>技术栈：
>>
>>>+ Python + Excel 
>>
>>渠道：
>>
>>>+ B站，CSDN， 博客园， GITHUB， 官网API
>>
>>方法：
>>
>>>+ 利用正则表达式提取爬虫爬取到的数据，利用python的openpyxl模块对爬取到信息进行分类处理以及写入excel表中
>
>三、数据可视化
>
>>技术栈：
>>
>>>+ Python + Echarts + JavaScript + HTML + CSS
>>
>>渠道：
>>
>>>+ B站，CSDN， 博客园， GITHUB， 官网API
>>
>>方法：
>>
>>>+ 利用python的panda读取excel表中的内容，根据信息的需要选取需要的数据存入列表中，然后将其联系在一起
>
>四、性能分析测试
>
>>- 通过pycharm自带的profile工具进行代码的测试，然后对各个函数功能进行改进分析
>
>五、代码性能改进
>
>>- 几乎没改动数据接口（没时间优化太多了），但是对代码的各项功能设计了异常处理机制

 **(3.2)爬虫与数据处理。**说明业务逻辑，简述代码的设计过程（例如可介绍有几个类，几个函数， 他们之间的关系），并对关键的函数或算法进行说明。（20'）

+ 代码中导入的模块：

```
import asyncio # 配合pyppeteer使用
import re # 字符匹配
import openpyxl # 进行excel操作
import selenium # 爬虫框架
from pyppeteer import launch # 绕过检测
from bs4 import BeautifulSoup # 解析网页
```

+ 函数封装：

```
async def pyppteer_fetchUrl(url) # 请求网页内容
def fetchUrl(url) # 帮助请求网页内容直到内容全部出现
def getPageUrl() # 获取每页的url
def getTitleUrl(html) # 获取每一页的li标签下的a的href然后拼接成url
def getContent(html, result, date) # 用正则处理请求到网页的内容进行数据处理
def save_to_excel(result) # 最后保存在excel里
```

+ 关键函数：

```
# 国家卫健委使用的反爬技术很强，首先网站是shtml，cookies一直在变，我实测基本在20秒不到就会变化一次；我刚开始用的是selenium和scrapy，但是我给卫健委的反爬机制劝退了（我试过打时间差，频繁改变cookie，但是该站的cookie是经过js加密的，其中至少包含了3个加密后的参数。想要真正意义上破解其加密算法，实现数据爬取，理论上是可行的，因为加密过程是在浏览器中完成的，所有加密的代码都可以在开发者工具中看到，所以理论上，只要懂js，花点功夫是可以完成破解的。（But，我没有time这么做，而且破解对方网站加密算法，就是在法律的边缘试探啊（还是国家的，看着标就给吓死了））
# 所以我各方百度，终于找到了一个神器——pyppeteer，完成了信息的爬取
# 剩下的就是依据国家卫健委的疫情格式正则匹配罢了

async def pyppteer_fetchUrl(url):
    browser = await launch({'headless': False,'dumpio':True, 'autoClose':True})
    page = await browser.newPage()
    await page.goto(url, timeout=10000000) # 请求网页，设置超时时间，不然容易超时出错
    # time.sleep(10)
    await asyncio.wait([page.waitForNavigation()]) # 等待网页内容刷出
    str = await page.content()
    await browser.close() # 关闭网页
    return str

def fetchUrl(url):
    return asyncio.get_event_loop().run_until_complete(pyppteer_fetchUrl(url))
```

**(3.3)数据统计接口部分的性能改进。**记录在数据统计接口的性能上所花费的时间，描述你改进的思路，并展示一张性能分析图（例如可通过VS 2019/JProfiler的性能分析工具自动生成），并展示你程序中消耗最大的函数。（6'）

- 数据统计接口部分程序（爬取网页并处理数据的，红色为占比最大函数，这里只以爬取一页为例）

![](https://images.cnblogs.com/cnblogs_com/blogs/766532/galleries/2214047/o_220919145520_visualization.py2.png)

- 改进思路：上图中可以看出，geturl的接口调用所消耗的资源是最多的，但是基本上没得好改目前我觉得，就改了些冗余的代码，正则和goturl都是必须的（虽然我没有自己改进接口，但是相信pyppeteer，yyds）

 **(3.4)每日热点的实现思路。**简要介绍实现该功能的算法原理，可给出必要的步骤流程图、数学公式推导和核心代码实现，并简要谈谈所采用算法的优缺点与可能的改进方案。（6'）

- 这个吧，实在没有花太多的时间（毕竟没时间呀~害，但是还是用简单的算法实现了一下）

```
def find_max_nums(nums, find_nums):
    if len(nums) == len(list(set(nums))):
        # 使用heapq
        max_number = heapq.nlargest(find_nums, nums)
        max_num_index = list(map(nums.index, max_number))
    else:
        # 使用deepcopy
        nums_copy = copy.deepcopy(nums)
        min_num = min(nums) - 1
        max_num_index = []
        max_number = []
        for i in range(find_nums):
            num_max = max(nums_copy)
            num_index = nums_copy.index(num_max)
            max_number.append(num_max)
            max_num_index.append(num_index)
            nums_copy[num_index] = min_num

    return max_num_index, max_number
  
timez = df.iloc[0:1, :]
day_date = []
for t in province:
day_date.append(list(timez[t]))
day_newcreate_sym = []
# day_newcreate_nosym = []
count = 0
for t in day_date:
x = t
count = count + 1
if count >= len(day_date) - 2:
break
day_newcreate_sym.append(x[0])
# day_newcreate_nosym.append(x[1])
max_num_index_sym, max_number_sym = find_max_nums(day_newcreate_sym, 5)
```

+ 主要就是用上面的find_max_nums(利用heapq模块)找到excel的第一条数据中，关于省份新增数值最大的前五个省份（利用pandas筛选）（因为台湾新增太多了，不大美观，所以只做了大陆版的，其实原理是一样的）（不过heapq有一个很奇怪的地方，就是再用另一个数据去实现的时候，会覆盖原有的列表，我试过先用一个列表保存下值，也不行，所以这里引入了deepcopy模块，用来保存复制这个列表）

**(3.5)数据可视化界面的展示。**在博客中介绍数据可视化界面的组件和设计的思路。（15'）

+ 主要是用Echarts（pyecharts模块）来实现数据可视化（刚开始想做前后端交互的，然后用数据库实现每日动态更新，但是，时间不允许啊~）
+ 左上角是新增确诊和新增无症状的柱状图，然后有一个zoom用来滑动筛选日期的。
+ 左下角是折线图，其中指出了当时zoom选择日期的疫情新增最高和最低点（算是历史热点吧）。
+ 然后右上角就是所谓的今日热点了，排列出当日新增最多的五个省份（奈何技术不够，不能做的很机器学习）。
+ 右下角是新增确诊和新增无症状的玫瑰图，其中图例是可以翻页的，或者选择取消（比如港澳台占比太多，不够美观），下面有一个日期分页可以选择日期。
+ 中间的二维地图也是一样，用来展示不同日期的疫情状况（都是依据excel数据形成的）。
+ 流水表是显示数据精度的（这里没有实际用处，我没有给他加上接口，所以只是用来美观）。
+ 设计的思路（简单来说，就是数据大屏的基本样式，结合了各个表和其他js组件，然后css改样式，最后用html打开，只是我用pyecharts的API简单实现了一下）。

![](https://images.cnblogs.com/cnblogs_com/blogs/766532/galleries/2214047/o_220919150341_%E7%96%AB%E6%83%85%E6%83%85%E5%86%B5%E6%95%B0%E6%8D%AE%E5%A4%A7%E5%B1%8F.jpg)

# 三、心得体会

 **(4.1)在这儿写下你完成本次作业的心得体会，当然，如果你还有想表达的东西但在上面两个板块没有体现，也可以写在这儿~（10'）**

心得体会啊~😔，就是有点像一个毕设的量压缩成一个两周就要完成的半成品（呜呜呜😭，还有我是个菜鸡，学技术还要学一会儿），虽然之前有做过公司爬虫的项目，但是guojia的东西是真的难爬（看到警徽都担惊受怕的😰，万一爬不好可是要吃牢饭的，还有校园网是真的辣鸡，爬到一半卡住了然后就寄了，不过因此我添加了异常保存机制），不过不得不说，还是学到了挺多的，比如shmtl的爬取，新框架pyppeteer的使用，以及echarts的使用（不过如果不是多加了两天的ddl，数据还是不够准确的，这两天纯在改进数据的准确度了，我感觉虽然可视化是很好看的，但是毕竟数据才是最重要的，所以爬虫模块一定要做好！）。但是我还没见到陵城四点钟的福大（不过我也不希望见到，不过指不定下次就见到了😭），总的来说虽然但是，比起随便看一篇文档，自己动手做还是挺好玩的（如果ddl能长一点就好了），然后紧接着下一个任务就来了，害，没事，这才是读书人的亚子，加油，希望下次可以做的更好！
