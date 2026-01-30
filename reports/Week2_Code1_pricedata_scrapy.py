from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time


options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--lang=en')


circle_names = [
    "Andhra Pradesh", "Assam", "Bihar Jharkhand", "Chennai", "Delhi",
    "Gujrat", "Haryana", "Himachal Pradesh", "Jammu Kashmir", "Karnataka",
    "Kerala", "Kolkata", "Madhya Pradesh", "Maharashtra", "Mumbai",
    "North East", "Odisha", "Punjab", "Rajasthan", "Tamil Nadu",
    "UP East", "UP West", "Uttarakhand", "West Bengal", "Chhattisgarh"
]


driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 5)

all_data = []


for i in range(1, 26):
    try:
        circle_name = circle_names[i - 1]
        print(f"scrapying num.{i} state: {circle_name}")


        driver.get('https://web.archive.org/web/20230202103324/https://telecom.economictimes.indiatimes.com/recharge-plans/')
        time.sleep(2)


        button = driver.find_element(By.XPATH, f'//*[@id="filters"]/div[1]/ul/li[{i+1}]/a') #第一个加载出来是All页面，从第二个开始为具体的地区
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)


        headers = driver.find_elements(By.XPATH, "//div[@class='tbl_outr']/table/thead/tr/th")
        cc = len(headers)
        table_header = [driver.find_element(By.XPATH, f"//div[@class='tbl_outr']/table/thead/tr/th[{j}]").text for j in range(1, cc + 1)]

       #after 20 all NA
        rc = 20
        for r in range(1, rc + 1):
            row = []
            for c in range(1, cc + 1):
                try:
                    d = driver.find_element(By.XPATH, f"//*[@id='dataplan']/div[3]/table/tbody/tr[{r}]/td[{c}]").text
                except:
                    d = ""
                row.append(d)
            row.append(circle_name)  # Circle
            row.append("2023-Q1")
            row.append(i)
            all_data.append(row)

    except Exception as e:
        print(f"the {i} order （{circle_names[i - 1]}）cannot scrapy：{e}")


driver.quit()


columns = table_header + ["Circle", "Time", "Circle Index"]
df_all = pd.DataFrame(all_data, columns=columns)


df_all.to_excel("All_Circles_2023Q1.xlsx", index=False)

print("All saved 'All_Circles_2021Q3_AS.xlsx'")
