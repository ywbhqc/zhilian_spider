This project is a data visualization application for Python job postings on Zhipin Recruitment, built using the Flask framework, featuring functionalities for data crawling, analysis, and visualization.

## Functional Modules
1. Data Crawling
- Use spider/zhilian_python_spider.py to crawl Python job information from Zhipin Recruitment
- Supports data collection by city (Beijing, Shanghai, Guangzhou, Shenzhen, etc.)
- Saves job data to local files

2. Data Analysis
- Use app.py for data processing and analysis
- Statistic distribution of company types
- Analyze job distribution by city
- Calculate salary level distribution

3. Data Visualization
- Generate pie chart for company type distribution
- Create bar chart for job distribution by city
- Plot box plot for salary level distribution
- Display visualization results via index.html

## File Structure
- app.py: Data processing and Flask service
- spider/: Crawling module
- templates/: Frontend template pages
- .csv files: Store processed data results
- .txt files: Store raw crawled data

## Running Instructions
1. Start the crawler to collect data
2. Run app.py to process the data
3. Access the Flask service to view visualization results

This project is developed in Python using the Flask framework, suitable for recruitment data analysis and visualization.