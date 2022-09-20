import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Liquid, Page, Pie, Timeline, Map
from pyecharts.commons.utils import JsCode
# from pyecharts.components import Table
# from pyecharts.faker import Faker
# from pyecharts.render import make_snapshot
# from snapshot_selenium import snapshot
# 内置主题类型可查看 pyecharts.globals.ThemeType
from pyecharts.charts import PictorialBar
from pyecharts.globals import SymbolType
from pyecharts.globals import ThemeType
import heapq
import copy

# 省份
province = ['安徽', '北京', '重庆', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南', '黑龙江', '湖北', '湖南', '江西', '吉林', '江苏', '辽宁', '内蒙古', '宁夏', '青海', '山西', '山东', '陕西', '上海', '四川', '天津', '西藏', '新疆', '云南', '浙江', '香港', '澳门', '台湾']
# 设置列对齐
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
# 打开文件
df = pd.read_excel('疫情新增以及新增无症状表.xlsx')
# 对时间进行统计
data1 = df['时间']
time_list = list(data1)
time_list_new = []
# 整合时间
for i in range(0, len(time_list)):
    if(i % 2 == 0):
        time_list_new.append(time_list[i])

# print(time_list)
data2 = df['新增总人数']
newcreate_list = list(data2)
newcreate_list_sym = []
newcreate_list_nosym = []
# 选择新增确诊和无症状
for i in range(0, len(newcreate_list)):
    if(i % 2 == 0):
        newcreate_list_sym.append(newcreate_list[i])
    elif(i % 2 == 1):
        newcreate_list_nosym.append(newcreate_list[i])
# print(newcreate_list)
# data_pro = []
# for pro in range(0, len(province)):
#     data_pro.append(list(df[province[pro]]))

# print(data_pro)
# 左上角柱状图新增和无症状的
def bar_datazoom_slider() -> Bar:
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        # 设置x、y轴格式
        .add_xaxis(time_list_new)
        .add_yaxis("新增确诊", newcreate_list_sym, itemstyle_opts={
            "normal": {
                "color": JsCode(
                    """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(0, 244, 255, 1)'
            }, {
                offset: 1,
                color: 'rgba(0, 77, 167, 1)'
            }], false)"""
                ),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": "rgb(0, 160, 221)",
            }
        })
        .add_yaxis("新增无症状", newcreate_list_nosym, itemstyle_opts={
            "normal": {
                "color": JsCode(
                    """new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: '#ACCBFC'
            }, {
                offset: 1,
                color: '#3F4EE5'
            }], false)"""
                ),
                "barBorderRadius": [30, 30, 30, 30],
                "shadowColor": "rgb(0, 160, 221)",
            }
        })
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            datazoom_opts=[opts.DataZoomOpts()],
            legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color='white')))
        .set_series_opts(label_opts=opts.LabelOpts(color='white'))
    )
    return c

# 左下角新增和无症状的折线图随时间
def line_markpoint() -> Line:
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        # 设置x、y轴格式
        .add_xaxis(time_list_new)
        .add_yaxis(
            "新增确诊",
            newcreate_list_sym,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="min")]),
        )
        .add_yaxis(
            "新增无症状",
            newcreate_list_nosym,
            markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=""), datazoom_opts=[opts.DataZoomOpts()], legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color='white')))
    )
    return c

# timez = df.iloc[:,:][df.时间 == '2022年9月11日']
# print(timez)
# print(list(timez['北京']))
# 玫瑰图
def pie_rosetype() -> Timeline:
    attr = province
    tl = Timeline()
    # 设置滚动条
    tl.add_schema(play_interval=1000, label_opts=opts.series_options.LabelOpts(is_show=True, color='white', font_size=10))
    # 时间可以改 这里我只爬取2022年8到9月的
    for year in range(2022, 2023):
        for month in range(8, 10):
            for day in range(1, 32):
                try:
                    timez = df.iloc[:,:][df.时间 == (str(year) + '年' + str(month) + '月' + str(day) + '日')]
                    # print(timez)
                    day_date = []
                    # print(year, month, day)
                    for t in province:
                        day_date.append(list(timez[t]))
                    # print(day_date)
                    day_newcreate_sym = []
                    day_newcreate_nosym = []
                    for t in day_date:
                        x = t
                        day_newcreate_sym.append(x[0])
                        day_newcreate_nosym.append(x[1])
                    # print(day_newcreate_sym)
                    # print(day_newcreate_nosym)
                except:
                    print('没有该日期的{}.{}.{}'.format(year, month, day))
                try:
                    pie = (
                        Pie(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
                            .add(
                            "新增确诊",
                            [list(z) for z in zip(attr, day_newcreate_sym)],
                            radius=["30%", "75%"],
                            center=["25%", "60%"],
                            rosetype="area",
                            label_opts=opts.LabelOpts(is_show=False),
                        )
                            .add(
                            "新增无症状",
                            [list(z) for z in zip(attr, day_newcreate_nosym)],
                            radius=["30%", "75%"],
                            center=["75%", "60%"],
                            rosetype="area",
                            label_opts=opts.LabelOpts(is_show=False),
                        )
                            .set_global_opts(title_opts=opts.TitleOpts(title="{}年{}月{}日".format(year, month, day), pos_bottom='2%', pos_left='2%', title_textstyle_opts=opts.TextStyleOpts(color='white', font_size=20)),
                                             legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color='white', font_size=10), type_="scroll", pos_top='10%'))
                    )
                    tl.add(pie, "{}年{}月{}日".format(year, month, day))
                except:
                    pass
    return tl

# 流水图 美观
def liquid_data_precision() -> Liquid:
    c = (
        Liquid()
        .add(
            "lq",
            [0.3254],
            label_opts=opts.LabelOpts(
                font_size=30,
                formatter=JsCode(
                    """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
                ),
                position="inside",
            ),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    return c

# 疫情地图中间
def map_china() -> Timeline:
    attr = province
    tl = Timeline()
    tl.add_schema(play_interval=1000, label_opts=opts.series_options.LabelOpts(is_show=True, color='white', font_size=14))
    for year in range(2022, 2023):
        for month in range(8, 10):
            for day in range(1, 32):
                try:
                    timez = df.iloc[:, :][df.时间 == (str(year) + '年' + str(month) + '月' + str(day) + '日')]
                    # print(timez)
                    day_date = []
                    # print(year, month, day)
                    for t in province:
                        day_date.append(list(timez[t]))
                    # print(day_date)
                    day_newcreate_sym = []
                    day_newcreate_nosym = []
                    for t in day_date:
                        x = t
                        day_newcreate_sym.append(x[0])
                        day_newcreate_nosym.append(x[1])
                    # print(day_newcreate_sym)
                    # print(day_newcreate_nosym)
                except:
                    print('没有该日期的{}.{}.{}'.format(year, month, day))
                try:
                    map0 = (
                        Map(init_opts=opts.InitOpts())
                            .add("新增确诊", [list(z) for z in zip(attr, day_newcreate_sym)], "china")
                            .add("新增无症状", [list(z) for z in zip(attr, day_newcreate_nosym)], "china")
                            .set_global_opts(
                            title_opts=opts.TitleOpts(title="{}年{}月{}日".format(year, month, day), pos_top='10%', pos_left='40%', title_textstyle_opts=opts.TextStyleOpts(color='white', font_size=30)), visualmap_opts=opts.VisualMapOpts(max_= 1000, item_height=100, item_width=20, pos_left='25%', pos_bottom='8%', textstyle_opts=opts.TextStyleOpts(color='white'), range_color=['#B9DFFE', '#334AE2', '#0E1D87']), legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(color='white'), pos_top='20%'))
                            .set_series_opts(itemstyle_opts=opts.ItemStyleOpts(opacity=0.7, border_color='#B9DFFE'))
                    )

                    tl.add(map0, "{}年{}月{}日".format(year, month, day))
                except:
                    pass
    return tl

# 找最大的下标的函数
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

# 今日热点
def Picbar_base() -> PictorialBar:
    # table = Table()
    c = PictorialBar()
    try:
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
        # print(max_number_sym, max_num_index_sym)
        # max_num_index_nosym, max_number_nosym = find_max_nums(day_newcreate_nosym, 5)
        location = [province[max_num_index_sym[4]], province[max_num_index_sym[3]], province[max_num_index_sym[2]], province[max_num_index_sym[1]], province[max_num_index_sym[0]]]
        values = [day_newcreate_sym[max_num_index_sym[4]], day_newcreate_sym[max_num_index_sym[3]], day_newcreate_sym[max_num_index_sym[2]], day_newcreate_sym[max_num_index_sym[1]], day_newcreate_sym[max_num_index_sym[0]]]
        # print(location)
        # print(values)
        # table.add(headers, rows)
        # table.set_global_opts({"title": "今日热点(大陆)",
        #                        "title_style": "style='color:white'",
        #                        "text-style": "style='color:white'",
        #                        })
        # return table
        c.add_xaxis(location)
        c.add_yaxis(
            "",
            values,
            label_opts=opts.LabelOpts(is_show=False),
            color='#CCE3FD',
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol=SymbolType.ROUND_RECT,
        )
        c.reversal_axis()
        c.set_global_opts(
            title_opts=opts.TitleOpts(title="今日热点(大陆版)", title_textstyle_opts=opts.TextStyleOpts(color='#7EC5FB', font_size=30)),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
                axislabel_opts=opts.LabelOpts(color='white', font_size=20),
            ),
        )
        return c
    except:
        # return table
        return c
# 背景
def lin_background1() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="700px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情状况",
                                      subtitle='更新日期: 2022/9/17',
                                      pos_left='center',
                                      title_textstyle_opts=opts.TextStyleOpts(font_size=35, color='#ffffff'),
                                      pos_top='2%'),
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/bg.jpg';
        """
    )
    return line3
# 左上角框
def lin_background2() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/left_line.png';

        """
    )
    return line3
# 右上角框
def lin_background3() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/right_line.png';

        """
    )
    return line3
# 背景地球
def lin_background4() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/map.png';

        """
    )
    return line3
# 光环
def lin_background5() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/jt.png';

        """
    )
    return line3
# 地球光环
def lin_background6() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/lbx.png';

        """
    )
    return line3
# 网格线
def lin_background7() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/line.png';

        """
    )
    return line3
# 标题框
def lin_background8() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/header.png';

        """
    )
    return line3
# 下表框
def lin_background9() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/linx.png';

        """
    )
    return line3
# 光环2
def lin_background10() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/gq.png';

        """
    )
    return line3
# 玫瑰光环1
def lin_background11() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/jzxz1.png';

        """
    )
    return line3
# 玫瑰光环2
def lin_background12() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/jzxz2.png';

        """
    )
    return line3
# 数据框1
def lin_background13() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/k_1.png';

        """
    )
    return line3
# 数据框2
def lin_background14() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/k_2.png';

        """
    )
    return line3
# 数据框3
def lin_background15() -> Line:
    line3 = (
        Line(init_opts=opts.InitOpts(width="1250px",
                                     height="725px",
                                     bg_color={"type": "pattern", "image": JsCode("img"), "repeat": "no-repeat"}))
            .add_xaxis([None])
            .add_yaxis("", [None])
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(is_show=False))
    )
    line3.add_js_funcs(
        """
        var img = new Image(); img.src = './img/k_3.png';

        """
    )
    return line3

def page_default_layout():
    page = Page(layout=Page.DraggablePageLayout)
    page.add(
        lin_background1(),
        lin_background2(),
        lin_background3(),
        lin_background4(),
        lin_background5(),
        lin_background6(),
        lin_background7(),
        lin_background8(),
        lin_background9(),
        lin_background10(),
        lin_background11(),
        lin_background12(),
        lin_background13(),
        lin_background13(),
        lin_background13(),
        lin_background13(),
        map_china(),
        bar_datazoom_slider(),
        line_markpoint(),
        Picbar_base(),
        pie_rosetype(),
        liquid_data_precision(),
    )
    # page.render("initial.html")
    Page.save_resize_html("initial.html", cfg_file="./chart_config.json", dest="疫情数据可视化.html")
if __name__ == "__main__":
    page_default_layout()
