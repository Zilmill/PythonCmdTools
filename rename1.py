import typer
import os

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
def rm(folder: str, fromname: str, toname: str = ""):
    rt = WalkCallback(fromname, toname)
    walk(folder, ".mp4", rt.handle)

# 第一种，更换名称，单个更改
@app.command(help="更换名称，单个更改")
def rs(filepath: str, fromname: str, toname: str = ""):
    newpath = getFileNewFilePath(filepath, fromname, toname)
    renamefile(filepath, newpath)

# 在名称的前后加上指定字符串
@app.command(help="批量重命名电视剧的每一集名称，")
def ad(filepath: str):
    print(filepath)

if __name__ == "__main__":
    app()