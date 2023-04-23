# 用必应搜索“pixelmator pro”，从搜索的结果中找标题有“Mac App Store 上的”
import requests
import re
import os
from bs4 import BeautifulSoup
import typer
import webbrowser
from watermark import Watermarker, WatermarkerStyles
from PIL import Image

app = typer.Typer()


def downloadwebp(out: str, link: str, ispng: int):
    """
    下载文件
    """
    print("下载：" + link)
    # 下载图片
    response = requests.get(link)
    # 把文件后缀.png/.jpeg/.jpg替换成.webp
    p = re.sub(r"\.(png|jpe?g)$", ".webp", out)
    # 保存图片
    with open(p, 'wb') as f:
        f.write(response.content)
    # webp文件转化为.jpg文件
    # 打开WebP文件
    with Image.open(p) as im:
        if ispng == 1:
            # 保存为JPEG文件
            im.save(p.replace('.webp', '.png'))
        else:
            # 将图像转换为RGB格式
            im = im.convert('RGB')
            # 保存为JPEG文件
            im.save(p.replace('.webp', '.jpg'))
        
    # 删除webp文件
    os.remove(p)


@app.command(name="w", help="添加水印的功能")
def waterfall(name: str):
    """
    添加水印的功能
    """
    # 组合apps和name并创建文件夹
    path = os.path.join(os.getcwd(), "apps/" + name + "/screenshot.png")

    # 如果不存在提示并结束
    if not os.path.exists(path):
        print("没有找到", path)
        exit()

    # 参数
    mark = "喵小猪杂货铺"
    out = os.path.join(os.getcwd(), "apps/" + name + "/screenshot2.png")
    Watermarker(path, mark, WatermarkerStyles.STRIPED).save(out)


@app.command(name="s", help="搜索mac软件并生成长图, 第一个参数是名称，第二个参数是app store地址")
def search(name: str, _url: str):
    """
    搜索mac软件并生成长图
    """
    # 组合apps和name并创建文件夹
    path = os.path.join(os.getcwd(), "apps/" + name)

    # 如果path不存在就创建
    if not os.path.exists(path):
        os.makedirs(path)

    if _url == "":
        # Send a GET request to Bing with the search query
        response = requests.get("https://www.bing.com/search?q=mac+" + name)

        # Parse the HTML content of the response with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the search result titles that contain "Mac App Store 上的"
        titles = soup.find_all('a')
        print(titles)
        mac_app_store_titles = [
            title for title in titles if "Mac App Store" in title.text]

        print(mac_app_store_titles)

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
    else:
        mac_app_store_url = _url

    # 获取页面的内容
    response = requests.get(mac_app_store_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # 获取标题
    mac_app_store_title = soup.find('h1')

    # 对class类为section__description的部分
    mac_app_store_description = soup.find(
        'div', {'class': 'section__description'})

    # 媒体文件夹
    mediapath = path + "/media/"

    # 如果mediapath不存在就创建
    if not os.path.exists(mediapath):
        os.makedirs(mediapath)

    # 如果mediapath文件夹内没有文件，否则就输出文件列表
    ls = os.listdir(mediapath)
    if not ls:
        # 获取class类为we-screenshot-viewer__screenshots 或者 we-screenshot-viewer__screenshots-list 的所有图片，并下载到当前目录
        pic = soup.find('div', {'class': 'we-screenshot-viewer__screenshots'})
        if pic is None:
            pic = soup.find(
                'div', {'class': 'we-screenshot-viewer__screenshots-list'})
        mac_app_store_screenshots = pic.find_all('source')

        # 循环获取图片
        for screenshot in mac_app_store_screenshots:
            srcset = screenshot['srcset']
            # 从srcset中提取https://开头到初次.png结尾的部分
            src = re.search(r"https://.+?\.(png|jpe?g)", srcset)[0]

            # 判断是否成功获取到
            if src is not None:
                downloadwebp(path + "/media/" + src.split('/')[-1], src + "/1286x0w.webp", 0)

    ls = os.listdir(mediapath)

    # mac_app_store_title 和 mac_app_store_description 部分的内容写到index.html中
    with open(path + "/index.html", "w", encoding="utf-8") as f:
        f.write("<!DOCTYPE html>\n")
        f.write("<html lang=\"en\">\n")
        f.write("<head>\n")
        f.write("    <meta charset=\"UTF-8\">\n")
        f.write("    <meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n")
        f.write(
            "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n")
        f.write("    <title>Mac App Store</title>\n")
        f.write("    <link rel=\"stylesheet\" href=\"style.css\">\n")
        f.write("    <style>\n")
        # 背景设置为白色
        f.write("        body {\n")
        f.write("            background-color: white;\n")
        f.write("            padding: 0 10px;\n")
        f.write("        }\n")
        # 添加图片最大百分百的样式
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
        # 循环ls并把其中的四张图片写到index.html中
        # 取ls数组的最大值，最大不能超过4
        for i in range(min(4, len(ls))):
            # 判断ls[i]不为空
            f.write("<img src=\"{}\">\n".format("media/" + ls[i]))
        f.write("</body>\n")
        f.write("</html>\n")

    # 获取软件图片
    icon = soup.find("picture", {'class': 'we-artwork--macos-app-icon'})
    icon_source = icon.find_all('source')[0]

    srcset = icon_source['srcset']
    # 从srcset中提取https://开头到初次.png结尾的部分
    src = re.search(r"https://.+?\.png", srcset)[0]

    downloadwebp(path + "/media/" + src.split('/')[-1], src + "/460x0w.webp", 1)

    # 打开网页
    webbrowser.open("http://127.0.0.1:5500/apps/"+name+"/index.html")


if __name__ == "__main__":
    app()
