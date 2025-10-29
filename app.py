#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智联招聘Python岗位数据可视化（简化版）
单页面展示三个图表：公司性质、地区分布、薪资分布
"""

from flask import Flask, render_template
import pandas as pd
import os
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie
from pyecharts.globals import ThemeType

app = Flask(__name__)

def load_data(filename):
    """加载CSV数据"""
    try:
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            print(f"成功加载: {filename} ({len(df)} 行)")
            return df
        else:
            print(f"文件不存在: {filename}")
            return None
    except Exception as e:
        print(f"加载数据失败: {e}")
        return None

def create_company_chart():
    """创建公司性质柱状图"""
    data = load_data('comptypenum.csv')
    if data is None or len(data) == 0:
        return None

    # 取前8个公司性质
    data = data.head(8)

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="400px", height="300px"))
        .add_xaxis(data['company_type'].tolist())
        .add_yaxis("职位数量", data['count'].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="公司性质分布"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            yaxis_opts=opts.AxisOpts(name="职位数量")
        )
    )
    return bar

def create_city_chart():
    """创建城市分布饼图"""
    data = load_data('cityjob.csv')
    if data is None or len(data) == 0:
        return None

    # 取前10个城市，其余归为"其他"
    top_cities = data.head(10)
    other_count = data.iloc[10:]['count'].sum() if len(data) > 10 else 0

    pie_data = [(row['city'], row['count']) for _, row in top_cities.iterrows()]
    if other_count > 0:
        pie_data.append(("其他城市", other_count))

    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="400px", height="300px"))
        .add("", pie_data, radius=["30%", "75%"])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="地区分布"),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%")
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    )
    return pie

def create_salary_chart():
    """创建薪资分布柱状图"""
    data = load_data('salary.csv')
    if data is None or len(data) == 0:
        return None

    # 按薪资等级排序（与第二阶段生成的数据一致）
    salary_order = ['5-15K', '15-25K', '25-30K', '30K以上', '面议/未知']
    data['salary_level'] = pd.Categorical(data['salary_level'], categories=salary_order, ordered=True)
    data = data.sort_values('salary_level')

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS, width="400px", height="300px"))
        .add_xaxis(data['salary_level'].tolist())
        .add_yaxis("职位数量", data['count'].tolist())
        .set_global_opts(
            title_opts=opts.TitleOpts(title="薪资分布"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
            yaxis_opts=opts.AxisOpts(name="职位数量")
        )
    )
    return bar

@app.route('/')
def index():
    """主页 - 展示三个图表"""
    # 创建三个图表
    company_chart = create_company_chart()
    city_chart = create_city_chart()
    salary_chart = create_salary_chart()

    # 获取数据摘要
    city_data = load_data('cityjob.csv')
    total_jobs = city_data['count'].sum() if city_data is not None else 0

    return render_template('index.html',
                         company_chart=company_chart.render_embed() if company_chart else "",
                         city_chart=city_chart.render_embed() if city_chart else "",
                         salary_chart=salary_chart.render_embed() if salary_chart else "",
                         total_jobs=total_jobs)

if __name__ == '__main__':
    print("启动Python岗位数据可视化应用")
    print("访问地址: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)