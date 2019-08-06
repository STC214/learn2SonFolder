import os
import os.path
import json
import re
import shutil
from pprint import pprint as prt

'''
整理目录中的教程文件
1.教程文件如果总体积大于500M则以不超过500M为标准分文文件夹保存
2.条件1中的最子级文件夹以此文件夹保存的教程视频序号区间命名
3.单个系列教程的根目录生成所有教程的文件列表文档
4.若文件名没有序号则添加序号
5.除了视频主目录其他目录下没有列表文件
6.修复了mp4文件会被修改后缀的bug
7.修复了以前会创建多层目录保存file_list文件的bug
8.提升了效率
9.修正了某些目录名导致的网络文件系统不显示的bug
10.修正了某些文件名导致某些网络文件系统不显示的bug
'''


class FileConturl:
    # 获取所有文件名并统一化改名
    def get_filenames(self, root_dir):
        for root, dirs, files in os.walk(root_dir, False):

            fi_list = []

            for i in files:
                if 'mp4' in i:
                    fi_list.append(i)
            for i in files:
                if 'flv' in i:
                    fi_list.append(i)
            for i in files:
                if 'mkv' in i:
                    fi_list.append(i)

            if len(fi_list) != 0 and ('__' not in root):
                print('\r\n')
                # prt(fi_list)

                for i in fi_list:
                    tstr = i.replace('mp4', '').replace(' ', '').replace(
                        ',', '').replace('，', '').replace(':', '')
                    res = re.search(pattern=(r'\d{1,3}'), string=tstr)
                    # prt(res.group(0))
                    if res is not None:
                        num_str = res.group(0)
                    # print(len(num_str))
                        q = i

                        if len(num_str) == 1:
                            q = q.replace(num_str, ('00' + num_str), 1)
                        if len(num_str) == 2:
                            q = q.replace(num_str, ('0' + num_str), 1)

                        print(q)
                        old_path = root + '\\' + i
                        new_path = root + '\\' + q
                        os.rename(old_path, new_path)

    # 文件列表保存方法

    def save_file(self, root_dict, fi_list, json_path, txt_list_path):
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(root_dict, f, ensure_ascii=False, indent=4)

        with open(txt_list_path, 'w', encoding='utf-8') as f:
            strs = ''
            for p in fi_list:
                strs += p + '\r'
            f.write(strs)

    # 处理记录列表的bug

    def path_con_for_list(self, f_path):
        path_splited = f_path.split('\\')
        files_name = path_splited.pop()
        path_splited.pop()
        # print(path_splited)
        root_path = '\\'.join(path_splited)

        return files_name, path_splited, root_path

    # 目标子目录处理方法

    def dir_con(self, dir_str):
        nalc = re.findall(pattern=(r'\d{3}\__\d{3}'), string=dir_str)
        if len(nalc) > 1:
            dirlist_old = dir_str.split('\\')
            pop_times = len(nalc)

            for i in range(1, pop_times):
                dirlist_old.pop()

            final_dir = '\\'.join(dirlist_old)
        else:
            final_dir = dir_str
        prt(final_dir)

        return final_dir

    # 处理文件移动具体方法

    def move_file(self, root_dict):
        try:
            file_tmp_list = []
            size_count = 0
            for k, v in root_dict.items():
                file_list = []
                for x, y in v.items():
                    file_list.append(x)

                for x, y in v.items():
                    file_tmp_list.append(x)
                    size_count += y
                    file_tmp_list.sort()
                    if len(file_tmp_list) != 0:
                        # if len(file_tmp_list) > 1:
                        if int(size_count / 1024 / 1024) > 500:
                            # prt(file_tmp_list)
                            new_tmp_list = [file_tmp_list[-1], ]
                            new_count = v[file_tmp_list[-1]]

                            file_tmp_list.pop()

                            start_num = re.search(
                                pattern=(r'\d{3}'), string=(file_tmp_list[0])).group(0)
                            print(start_num)
                            end_num = re.search(
                                pattern=(r'\d{3}'), string=file_tmp_list[-1]).group(0)

                            son_dir_name = start_num + '__' + end_num
                            son_path = k + '\\' + son_dir_name
                            son_path = dir_con(son_path)

                            if not os.path.exists(son_path):
                                os.mkdir(son_path)

                            for i in file_tmp_list:
                                old_path = k + '\\' + i
                                new_path = son_path + '\\' + i
                                print(new_path)
                                # new_path = dir_con(new_path)
                                shutil.move(old_path, new_path)

                            file_tmp_list = new_tmp_list
                            size_count = new_count

                        if int(size_count / 1024 / 1024) < 500 and (file_list[-1] == file_tmp_list[-1]):
                            start_num = re.search(
                                pattern=(r'\d{3}'), string=file_tmp_list[0]).group(0)
                            end_num = re.search(
                                pattern=(r'\d{3}'), string=file_tmp_list[-1]).group(0)
                            son_dir_name = start_num + '__' + end_num
                            son_path = k + '\\' + son_dir_name
                            son_path = dir_con(son_path)

                            if not os.path.exists(son_path):
                                os.mkdir(son_path)

                            for i in file_tmp_list:
                                old_path = k + '\\' + i
                                new_path = son_path + '\\' + i
                                print(new_path)
                                # new_path = dir_con(new_path)
                                shutil.move(old_path, new_path)
                    print('处理完成：' + k)
        except Exception as e:
            pass

    # 移动文件准备流程和调用移动文件方法

    def file_move(self, root_dir):
        for root, dirs, files in os.walk(root_dir, False):
            # fi_list = files
            fi_list = []
            for i in files:
                if 'mp4' in i:
                    fi_list.append(i)
            for i in files:
                if 'flv' in i:
                    fi_list.append(i)
            for i in files:
                if 'mkv' in i:
                    fi_list.append(i)

            if len(fi_list) != 0 and ('__' not in root):
                # print('\r\n')
                # res_mol = False

                txt_list_path = root + '\\' + 'file_list.txt'
                json_path = root + '\\' + 'file_list.json'

                root_dict = {}
                dir_dict = {}

                for i in fi_list:
                    file_path = root + '\\' + i
                    # res_num = re.search(pattern=(r'\d{3}'), string=i).group(0)
                    file_size = os.path.getsize(file_path)
                    dir_dict[i] = file_size
                root_dict[root] = dir_dict

                if '__' not in json_path and "__" not in txt_list_path:
                    self.save_file(root_dict, fi_list, json_path, txt_list_path)
                else:
                    if os.path.exists(json_path):
                        os.remove(json_path)
                    if os.path.exists(txt_list_path):
                        os.remove(txt_list_path)

                self.move_file(root_dict)
            else:
                print('此处不需要处理')

    # 得到文件目录索引
    def gen_txt_json(self, root_dir):
        fil_list = []
        for root, dirs, files in os.walk(root_dir, False):
            fi_list = []
            for i in files:
                if 'mp4' in i:
                    fi_list.append(i)
            for i in files:
                if 'flv' in i:
                    fi_list.append(i)
            for i in files:
                if 'mkv' in i:
                    fi_list.append(i)

            if len(fi_list) != 0 and ('__' not in root):
                for i in fi_list:
                    ffp = root + '\\' + i
                    fil_list.append(ffp)

                nef = sorted(fil_list)

                fl = []
                fd = {}
                for f in range(1, len(nef)):
                    files_name, path_splited, root_path = self.path_con_for_list(
                        nef[f])
                    fn_1, ps_1, rp_1 = self.path_con_for_list(nef[f - 1])
                    txt_path = rp_1 + '\\' + 'file_list.txt'
                    json_path = rp_1 + '\\' + 'file_list.json'

                    if path_splited == ps_1:
                        fl.append(fn_1)
                        fl.append(files_name)
                        fl = sorted(list(set(fl)))
                        fd[rp_1] = fl

                    if path_splited != ps_1 and (fl != []) and (fd != {}):
                        self.save_file(fd, fl, json_path, txt_path)
                        fl = []
                        fd = {}

                    if f == len(nef) - 1:
                        self.save_file(fd, fl, json_path, txt_path)

                    prt(fl)
                    prt(fd)

    # 删除多余的目录记录文件
    def del_more_log(self, root_dir):
        for root, dirs, files in os.walk(root_dir, False):
            for i in files:
                if ('file_list.txt' in i) or ('file_list.json' in i):
                    if root.count('__') >= 2:
                        print(root)
                        if os.path.exists(root):
                            shutil.rmtree(root)

    # 旧规则中的破折号改为下划线，文件名中的符号和空格改为下划线

    def rename_root(self, root_dir):
        for root, dirs, files in os.walk(root_dir, False):
            for i in dirs:

                # 教程目录去空格为下划线
                if ' ' in i:
                    oldroot = root + '\\' + i
                    newroot = root + '\\' + i.replace(' ', '_')
                    os.rename(oldroot, newroot)
                    print(newroot)
                else:
                    print('目录名已经整理了')

                # 分P目录破折号改下划线
                if '——' in i:
                    # print(i)
                    # print(root)
                    oldroot = root + '\\' + i
                    newroot = root + '\\' + i.replace('——', '__')
                    print(newroot)
                    os.rename(oldroot, newroot)
                else:
                    print('分p目录已处理')

    def rename_files(self, root_dir):
        for root, dirs, files in os.walk(root_dir, False):
            # 文件名中空格和符号改下划线
            for i in files:
                if ('(' or ')') in i:
                    print(i)
                    strls = ['(', ')', '（', '）', ',', ' ', '-']
                    k = i
                    for l in strls:
                        newname = k.replace(l, '_')
                        k = newname

                    odpt = root + '\\' + i
                    nwpt = root + '\\' + newname
                    os.rename(odpt, nwpt)
                    print(newname)
                else:
                    print('文件名已处理')


##################################################################################


def main():
    # path_list = [r'H:\learn_video', r'G:\down',
    #              r'E:\Program Files\JiJiDown\Download']
    # path_list = [r'F:\整理教程']
    # path_list = [r'F:\教程']
    path_list = [r'H:\testpath']

    # 实例化对象
    F = FileConturl()

    for pathi in path_list:
        F.rename_root(pathi)
        F.rename_files(pathi)
        F.get_filenames(pathi)
        F.file_move(pathi)
        F.gen_txt_json(pathi)
        F.del_more_log(pathi)


main()
