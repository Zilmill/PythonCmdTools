import os


def findAllFile(path, ext, cb):
    """
    查找指定后缀的文件
    """
    list = os.listdir(path)
    for i in list:
        if os.path.splitext(i)[1] == ext:
            cb(i)


def mp4_to_wav(mp4_path):
    """
    mp4 转 wav
    :return: .wav文件
    """
    wav_path = os.getcwd() + "/wavs/" + mp4_path.replace("mp4", "wav")
    # 如果存在wav_path文件，先删除。
    if os.path.exists(wav_path):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(wav_path)
        # 终端命令
    command = "ffmpeg -i '{}' -ac 1 -ar {} '{}'".format(
        mp4_path, 16000, wav_path)
    print('命令是：', command)
    # 执行终端命令
    os.system(command)
    os.remove(mp4_path)

class ReplaceTitle(object):
    def __init__(self, title):
        self.title = title

    def handle(self, path):
        if self.title != '':
            ar = path.split(self.title)
            if len(ar) > 1:
                nn = ar[1]
                os.rename(path, nn)


if __name__ == "__main__":
    # 读取参数 执行命令，下载视频
    print("###依赖 you-get 库####")
    org = input("输入视频地址\n")
    is_play_list = input("是视频列表吗？[enter/n]")
    title = input("如果需要删除名称，就输入，否则直接enter")
    cmd = "you-get " + org
    if is_play_list != 'n':
        cmd += " --playlist"
    os.system(cmd)
    # 删除所有xml文件
    findAllFile(os.getcwd(), '.xml', os.remove)
    # 更改所有视频文件名称
    rt = ReplaceTitle(title)
    findAllFile(os.getcwd(), '.mp4', rt.handle)
    # 开始转化
    has_folder = os.path.exists(os.getcwd() + "/wavs/")
    if not has_folder:
        os.makedirs(os.getcwd() + "/wavs/")
    findAllFile(os.getcwd(), '.mp4', mp4_to_wav)
