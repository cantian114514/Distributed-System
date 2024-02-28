import requests
from bs4 import BeautifulSoup

def get_label():
    url = "https://github.com/pytorch/pytorch/labels"  # GitHub Bug页面的URL
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }  # 添加User-Agent头部，模拟浏览器请求

    for i in range(1, 5): # 经检查 共有8页
        # 为了格式统一 仅爬取头部为module的标签
        response = requests.get(url + f"?page={i}&q=module", headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"页面{i}请求成功")
            soup = BeautifulSoup(response.text, "html.parser")
            labels = soup.find_all("a", class_ = "IssueLabel")
            for label in labels:
                label_name = label.get('data-name')
                if "module" in label_name and label_name not in original_data:
                    original_data[label_name] = []
                    # print(label_name)
        
            flag = soup.find_all("a", class_ = "next_page")
            if len(flag) == 0: # 不存在下一页
                break

        else:
            print(f"页面{i}请求失败, 状态码：{response.status_code}")
            break


def get_title(): # 只爬取含module的
    base_url = "https://github.com/pytorch/pytorch/labels/"  # GitHub Bug页面的URL
    for label in original_data.keys():
        print(f"正在处理{label}标签")
        temp_label = label[8:]
        for i in range(1, 10): # 一个页面有25个标题，避免一个标签爬太多标题导致数据不平衡
            tail = f"module:%20{temp_label}?page={i}&q=is%3Aopen+label%3A%22module%3A+{temp_label}%22"
            url = base_url + tail
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"{label}: 页面{i}请求成功")
                soup = BeautifulSoup(response.text, "html.parser")
                titles = soup.find_all('a', class_='Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title')
                for title in titles:
                    title_text = title.text.strip()
                    original_data[label].append(title_text)
                    print(title_text)
            
                flag = soup.find_all("a", class_ = "next_page")
                if len(flag) == 0: # 不存在下一页
                    break

            else:
                print(f"页面{i}请求失败, 状态码：{response.status_code}")
                break


def write_data(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for label in original_data.keys():
            for i in range(len(original_data[label])):
                text = f"{label}\t{original_data[label][i]}"
                file.write(text)
                file.write('\n')
    print("数据写入完成")

original_data = {}
file_path = 'D:\\VSCode_code\\python\\file\\FBSxitong\\dataset\\original_data.txt'
get_label()
get_title()
original_data = dict(sorted(original_data.items(), key=lambda item: len(item[1]), reverse=True)) # 按评论数从高到低进行排序
write_data(file_path)