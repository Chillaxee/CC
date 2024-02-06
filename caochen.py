from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import argparse
import time







def main(date, currency):

    #先进行货币代码转换为中文的操作
    # 使用 Edge 浏览器，指定 WebDriver 的路径
    url = "https://www.11meigui.com/tools/currency"
    driver = webdriver.Edge()
    driver.get(url)

    # 找到货币列表
    table_rows = driver.find_elements(By.XPATH, "//tr")

    # 遍历每一行，查找目标货币代码的行
    for row in table_rows:
        td_elements = row.find_elements(By.TAG_NAME, "td")
        if len(td_elements) >= 5 and td_elements[4].text == currency:
            # 找到符合条件的行
            currency_text = td_elements[1].text
            break

    time.sleep(5)
    driver.quit()

    #把货币代码换成中文，以便于后续操作
    currency_update = currency_text

    #进行数据趴虫操作
    url = "https://www.boc.cn/sourcedb/whpj/"
    driver = webdriver.Edge()
    driver.get(url)

    # 解析日期参数
    year = date[:4]
    month = date[4:6]
    day = date[6:]

    # 时间选择
    time_start_button = driver.find_element(By.ID, "erectDate")
    time_start_button.click()

    # 使用 Select 类选择年份
    select = Select(driver.find_element(By.ID, "calendarYear"))
    select.select_by_value(year)

    # 使用 Select 类选择月份
    select = Select(driver.find_element(By.ID, "calendarMonth"))
    select.select_by_value(str(int(month) - 1))  # 月份需要减1，因为月份从0开始

    # 点击日期
    date_to_select = driver.find_element(By.XPATH, f"//table[@id='calendarTable']//td[normalize-space()='{day}']")
    date_to_select.click()

    time_end_button = driver.find_element(By.ID, "nothing")
    time_end_button.click()

    select = Select(driver.find_element(By.ID, "calendarYear"))
    select.select_by_value(year)

    select = Select(driver.find_element(By.ID, "calendarMonth"))
    select.select_by_value(str(int(month) - 1))

    date_to_select = driver.find_element(By.XPATH, f"//table[@id='calendarTable']//td[normalize-space()='{day}']")
    date_to_select.click()

    # 定位货币选择下拉菜单,从下拉菜单中选择指定的货币
    currency_select = Select(driver.find_element(By.NAME, 'pjname'))
    currency_select.select_by_value(currency_update)

    # 等待搜索按钮出现并且可点击
    search_button = driver.find_element(By.XPATH, "//input[@class='search_btn'][@onclick='executeSearch()']")
    search_button.click()

    # 提取数据
    target = driver.find_element(By.XPATH, "//tr[@class='odd']/td[4]")
    result_text = target.text


    # 打开文件 result.txt 以写入模式，并将文本写入文件
    with open('result.txt', 'w') as file:
        file.write(result_text)

    # 打印成功消息
    print("数据已保存到 result.txt 文件中")

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve currency exchange rate data")
    parser.add_argument("date", type=str, help="Date in format YYYYMMDD")
    parser.add_argument("currency", type=str, help="Currency code")

    args = parser.parse_args()
    main(args.date, args.currency)
