import typer
import os
import re

app = typer.Typer()

# 给电视剧集重命名

# 替换名称
class WalkCallback(object):
    def __init__(self, fromname: str, toname: str = "") -> None:
        self.fromname = fromname
        self.toname = toname

    def handle(self, path):
        newpath = getFileNewFilePath(path, self.fromname, self.toname)  
        renamefile(path, newpath)

# 不要参数自动生成名称
def autoRenameFile(filepath: str):
    folder = os.path.dirname(filepath)
    filename = os.path.split(filepath)[1]
    (_, ext) = os.path.splitext(filename)
    arr = re.split('\.|\[|\]|\/|\s|【|】', filename)
    for i in range(len(arr)):
        print("[" + str(i) + "]: " + arr[i])
    index = input("输入数字选择一个想要的,多个用,号隔开,没有想要的直接enter：")

    if len(index) == 0:
        return
    indexes = index.split(",")
    n = ""
    for a in indexes:
        n += arr[int(a)] + " "

    newpath = os.path.join(folder, n + ext)
    print(newpath) 
    renamefile(filepath, newpath)

# 获取路径的新名称
def getFileNewFilePath(path: str, fromname: str, to: str = ""):
    folder = os.path.dirname(path)
    (_, file) = os.path.split(path)
    (file, ext) = os.path.splitext(file)
    froms = fromname.split(",")
    for item in froms:
        file = file.replace(item, to)
    newname = file.strip() + ext
    return os.path.join(folder, newname)

# 变量
def walk(path: str, ext: str, call):
    for fpathe, dirs,fs in os.walk(path):
        for f in fs:
            filepath = os.path.join(fpathe, f)
            if os.path.splitext(filepath)[1] == ext: {
                    call(filepath)
            }


# 根方法，把某个文件的名称改为什么
def renamefile(oldpath: str, newpath: str):
    print("本次改名说明：")
    print("原路径：" + oldpath)
    print("新路径：" + newpath)
    dopass = input("确认继续吗？(enter/n)")
    if dopass != "":
        print("停止")
        return
    os.rename(oldpath, newpath)

# 更改一个文件夹内所有文件的名称
@app.command(help="【批量】更改一个文件夹内所有文件的名称")
def rm(folder: str, fromname: str, toname: str):
    rt = WalkCallback(fromname, toname)
    walk(folder, ".mp4", rt.handle)

# 第一种，更换名称，单个更改
@app.command(help="更换名称，单个更改")
def rs(filepath: str, fromname: str, toname: str):
    newpath = getFileNewFilePath(filepath, fromname, toname)
    renamefile(filepath, newpath)

# 批量重命名电视剧的每一集名称，
@app.command(help="批量重命名电视剧的每一集名称，")
def shows(filepath: str):
    # 第一步 把除数字的都删掉
    print(filepath)

# 自动处理电影名称
@app.command(name="a", help="自动处理电影名称")
def movies(filepath: str):
    walk(filepath, ".mp4", autoRenameFile)
    walk(filepath, ".mkv", autoRenameFile)
    walk(filepath, ".rmvb", autoRenameFile)

if __name__ == "__main__":
    app()