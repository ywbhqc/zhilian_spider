#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智联招聘Python岗位爬虫
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import re
from urllib.parse import quote
from datetime import datetime

class ZhilianPythonSpider:
    def __init__(self):
        self.session = requests.Session()
        self.keyword = "Python"
        self.output_file = "zhiliandata.txt"

        # 31个省会城市及其jl代码
        self.cities = [
            {'name': '北京', 'code': '530'},
            {'name': '上海', 'code': '538'},
            {'name': '天津', 'code': '531'},
            {'name': '重庆', 'code': '551'},
            {'name': '石家庄', 'code': '565'},
            {'name': '太原', 'code': '576'},
            {'name': '呼和浩特', 'code': '587'},
            {'name': '沈阳', 'code': '599'},
            {'name': '长春', 'code': '613'},
            {'name': '哈尔滨', 'code': '622'},
            {'name': '南京', 'code': '635'},
            {'name': '杭州', 'code': '653'},
            {'name': '合肥', 'code': '664'},
            {'name': '福州', 'code': '681'},
            {'name': '南昌', 'code': '691'},
            {'name': '济南', 'code': '702'},
            {'name': '郑州', 'code': '719'},
            {'name': '武汉', 'code': '736'},
            {'name': '长沙', 'code': '749'},
            {'name': '广州', 'code': '763'},
            {'name': '南宁', 'code': '785'},
            {'name': '海口', 'code': '799'},
            {'name': '成都', 'code': '801'},
            {'name': '贵阳', 'code': '822'},
            {'name': '昆明', 'code': '831'},
            {'name': '拉萨', 'code': '847'},
            {'name': '西安', 'code': '854'},
            {'name': '兰州', 'code': '864'},
            {'name': '西宁', 'code': '878'},
            {'name': '银川', 'code': '886'},
            {'name': '乌鲁木齐', 'code': '890'}
        ]

        # User-Agent列表
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0"
        ]

    def get_headers(self):
        """获取请求头"""
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

    def parse_job_info(self, container, city_name):
        """解析单个职位信息"""
        try:
            # 职位名称
            job_name = "未知职位"
            job_name_elem = container.find('a', class_='jobinfo__name')
            if job_name_elem:
                job_name = job_name_elem.get_text(strip=True)

            # 公司名称
            company_name = "未知公司"
            company_name_elem = container.find('a', class_='companyinfo__name')
            if company_name_elem:
                company_name = company_name_elem.get_text(strip=True)

            # 薪资
            salary = "薪资面议"
            salary_elem = container.find('p', class_='jobinfo__salary')
            if salary_elem:
                salary = salary_elem.get_text(strip=True)

            # 工作地点
            location = f"{city_name}·未知区域"
            location_items = container.find_all('div', class_='jobinfo__other-info-item')
            for item in location_items:
                if item.find('img', class_='jobinfo__other-info-location-image'):
                    span_elem = item.find('span')
                    if span_elem:
                        location = span_elem.get_text(strip=True)
                        break

            # 经验和学历要求
            experience = "经验不限"
            education = "学历不限"

            for item in location_items:
                text = item.get_text(strip=True)
                if '·' in text:
                    continue
                if re.search(r'\d+-\d+年|经验不限|应届', text):
                    experience = text
                elif re.search(r'本科|大专|硕士|博士|学历不限', text):
                    education = text

            # 公司性质
            company_nature = "民营"
            company_tag_container = container.find('div', class_='companyinfo__tag')
            if company_tag_container:
                company_tags = company_tag_container.find_all('div', class_='joblist-box__item-tag')
                for tag in company_tags:
                    tag_text = tag.get_text(strip=True)
                    if tag_text in ['民营', '国企', '外企', '合资']:
                        company_nature = tag_text
                        break

            # 数据清洗
            job_name = job_name.replace('|', '').strip()
            company_name = company_name.replace('|', '').strip()
            salary = salary.replace('|', '').strip()
            location = location.replace('|', '').strip()

            # 格式化输出
            formatted_job = f"{city_name}|{job_name}|{company_name}|{salary}|{location}|{experience}|{education}|{company_nature}"
            return formatted_job

        except Exception as e:
            print(f"解析职位信息失败: {e}")
            return None

    def save_job_data(self, job_data):
        """保存职位数据到文件"""
        try:
            with open(self.output_file, 'a', encoding='utf-8') as f:
                f.write(job_data + '\n')
        except Exception as e:
            print(f"保存数据失败: {e}")

    def crawl_city_jobs(self, city_name, city_code):
        """爬取单个城市的Python职位（最多10页）"""
        print(f"开始爬取 {city_name} 的Python职位...")

        page = 1
        total_jobs = 0
        max_pages = 5

        while page <= max_pages:
            print(f"正在爬取第 {page} 页...")

            # 构建URL
            url = f"https://sou.zhaopin.com/?jl={city_code}&kw={quote(self.keyword)}&p={page}"

            try:
                # 发送请求
                response = self.session.get(url, headers=self.get_headers(), timeout=10)

                if response.status_code != 200:
                    print(f"HTTP {response.status_code}, 跳过第 {page} 页")
                    page += 1
                    continue

                # 解析页面
                soup = BeautifulSoup(response.text, "html.parser")
                job_containers = soup.find_all('div', class_='joblist-box__item')

                # 检查是否为空白页面
                if len(job_containers) == 0:
                    print(f"第 {page} 页为空白页面，{city_name} 爬取完成")
                    break

                # 解析并保存每个职位
                page_jobs = 0
                for container in job_containers:
                    job_data = self.parse_job_info(container, city_name)
                    if job_data:
                        self.save_job_data(job_data)
                        page_jobs += 1
                        total_jobs += 1

                print(f"第 {page} 页获取 {page_jobs} 条职位")

                # 随机延时
                time.sleep(random.uniform(1, 3))
                page += 1

            except Exception as e:
                print(f"第 {page} 页爬取失败: {e}")
                break

        print(f"{city_name} 完成，共获取 {total_jobs} 条Python职位")
        return total_jobs

    def start_crawling(self):
        """开始爬取所有城市的Python职位"""
        print(f"开始爬取全国省会城市的Python职位")
        print(f"总城市数: {len(self.cities)}")
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # 创建输出文件并写入标题行
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write("城市|职位名称|公司名称|薪资|地点|经验|学历|公司性质\n")

        total_jobs = 0
        start_time = datetime.now()

        for i, city in enumerate(self.cities):
            city_name = city['name']
            city_code = city['code']

            print(f"\n[{i+1}/{len(self.cities)}] 开始爬取 {city_name}...")

            try:
                city_jobs = self.crawl_city_jobs(city_name, city_code)
                total_jobs += city_jobs

            except KeyboardInterrupt:
                print(f"\n用户中断爬取")
                break
            except Exception as e:
                print(f"{city_name} 爬取失败: {e}")
                continue

        # 爬取完成统计
        end_time = datetime.now()
        duration = end_time - start_time

        print(f"\nPython职位爬取完成！")
        print(f"总计获取: {total_jobs} 条Python职位数据")
        print(f"耗时: {duration}")
        print(f"数据文件: {self.output_file}")

def main():
    """主函数"""
    print("智联招聘Python岗位爬虫")
    print("=" * 50)

    spider = ZhilianPythonSpider()
    print(f"已加载 {len(spider.cities)} 个省会城市")
    spider.start_crawling()

if __name__ == "__main__":
    main()