# 用必应搜索“pixelmator pro”，从搜索的结果中找标题有“Mac App Store 上的”
import requests
import re
import os
from bs4 import BeautifulSoup
import typer
import time
from selenium import webdriver
from PIL import Image
from io import BytesIO

app = typer.Typer()


# 不加上这个不能使用下面的，不知道为啥
@app.command()
def hello(name: str):
    print(f"Hello {name}")

# 搜索mac软件并生成长图
@app.command(name="s", help="搜索mac软件并生成长图")
def search(name: str):
    # 组合apps和name并创建文件夹
    path = os.path.join(os.getcwd(), "apps/" + name)

    # 如果path不存在就创建
    if not os.path.exists(path):
        os.makedirs(path)

    # Send a GET request to Bing with the search query
    response = requests.get("https://www.bing.com/search?q=" + name)

    # Parse the HTML content of the response with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the search result titles that contain "Mac App Store 上的"
    titles = soup.find_all('a')
    mac_app_store_titles = [title for title in titles if "Mac App Store 上的" in title.text]

    # 展示 mac_app_store_titles，并显示序号，让用户选择一个
    for i, title in enumerate(mac_app_store_titles):
        print(i, ": ", title.text, "\n", title["href"])

    # 如果只有一个那么直接用第0个，否则让用户选择一个
    if len(mac_app_store_titles) == 1:
        mac_app_store_url = mac_app_store_titles[0]["href"]
    else:
        choice = int(input("请输入序号:"))
        mac_app_store_url = mac_app_store_titles[choice]["href"]

    # 选择的没有URL时结束并提示没有找到
    if mac_app_store_url is None:
        print("没有找到")
        exit()

    # 获取页面的内容
    response = requests.get(mac_app_store_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 获取标题
    mac_app_store_title = soup.find('h1')

    # 对class类为section__description的部分
    mac_app_store_description = soup.find('div', {'class': 'section__description'})

    # 媒体文件夹
    mediapath = path + "/media/"

    # 如果mediapath不存在就创建
    if not os.path.exists(mediapath):
        os.makedirs(mediapath)

    # 如果mediapath文件夹内没有文件，否则就输出文件列表
    ls = os.listdir(mediapath)
    if not ls:
        # 获取class类为we-screenshot-viewer__screenshots的所有图片，并下载到当前目录
        pic = soup.find('div', { 'class': 'we-screenshot-viewer__screenshots' })
        mac_app_store_screenshots = pic.find_all('source')

        # 循环获取图片
        for screenshot in mac_app_store_screenshots:
            srcset = screenshot['srcset']
            # 从srcset中提取https://开头到初次.png结尾的部分
            src = re.search(r"https://.+?\.png", srcset)[0]

            # 判断是否成功获取到
            if src is not None:
                # 下载图片
                response = requests.get(src + "/1286x0w.webp")
                # 保存图片
                with open(path + "/media/" + src.split('/')[-1], 'wb') as f:
                    f.write(response.content)
    
    ls = os.listdir(mediapath)

    # mac_app_store_title 和 mac_app_store_description 部分的内容写到index.html中
    with open(path + "/index.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang=\"en\">\n")
        f.write("<head>\n")
        f.write("    <meta charset=\"UTF-8\">\n")
        f.write("    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n")
        f.write("    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        f.write("    <title>Mac App Store</title>\n")
        f.write("    <link rel=\"stylesheet\" href=\"style.css\">\n")
        # 添加图片最大百分百的样式
        f.write("    <style>\n")
        f.write("        img {\n")
        f.write("            max-width: 100%;\n")
        f.write("        }\n")
        # 添加一个样式，.app-header__title .badge--product-title隐藏
        f.write("        .app-header__title .badge--product-title {\n")
        f.write("            display: none;\n")
        f.write("        }\n")
        # 添加样式 .visuallyhidden隐藏
        f.write("        .visuallyhidden {\n")
        f.write("            display: none;\n")
        f.write("        }\n")
        f.write("    </style>\n")
        f.write("</head>\n")   
        f.write("<body>\n")
        # 写入标签
        f.write("{}".format(mac_app_store_title))
        # 使用字符串格式化写入mac_app_store_description
        f.write("{}".format(mac_app_store_description))
        # 循环ls并把图片写到index.html中
        for file in ls:
            f.write("<img src=\"media/" + file + "\" alt=\"\">\n")
        f.write("</body>\n")
        f.write("</html>\n")

    # 创建Chrome浏览器对象
    driver = webdriver.Chrome()

    # 打开网页并改变窗口大小
    driver.get("http://127.0.0.1:5500/apps/"+name+"/index.html")
    driver.set_window_size(500, 800)  # 将窗口大小设置为 500x800

    time.sleep(4)

    # 截取窗口长图
    screenshot = driver.get_screenshot_as_png()
    screenshot = Image.open(BytesIO(screenshot))  # 将截图转换为 Image 对象
    screenshot.save(path + "/screenshot.png")

if __name__ == "__main__":
    app()


    





