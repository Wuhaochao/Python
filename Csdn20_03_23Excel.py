import os, xlrd, re, datetime, shutil, xlwt

'''将首目录的xls文件放入日期文件夹中'''
def moveXls(xlsNum, monthDay):
    #创建日期命名的文件
    os.makedirs('.\\'+monthDay+'')
    #通过正则表达式收集含有“销售单”字样的excel表格
    strRegex = re.compile(r'.*销.*售.*单.*')
    for xls in  xlsNum:
        if strRegex.search(xls):
            shutil.move('.\\'+xls+'', '.\\'+monthDay+'')

'''将文档数据汇总成字典组'''
def sumDataDic(xlsNum):
    ifff = 0
    aaa = []
    for xls in  xlsNum:
        #读取对应excel文件，返回BOOK对象
        book = xlrd.open_workbook(xls)
        #第一表单，索引号为0
        sh = book.sheet_by_index(0)

        #第一张excel表
        if ifff == 0:
            for rx in range(sh.nrows):
                if rx - 6 >= 0 and rx + 2 < sh.nrows:
                    spam3[sh.row_values(rx)[1]] = int(sh.row_values(rx)[4])
        #后面的一堆excel表
        else:
            for rx in range(sh.nrows):
                if rx - 6 >= 0 and rx + 2 < sh.nrows:
                    spam2[sh.row_values(rx)[1]] = int(sh.row_values(rx)[4])
        ifff += 1
    
    #有多张张excel表的情况，若2字典有3字典的值，就把3字典的值添加到2字典里
    if ifff != 0:
        for k, v in spam3.items():
            if k in spam2:
                spam2[k] += v
            else:
                spam2[k] = v
        #通过压缩zip函数，转化元组，然后用sorted函数排序
        aaa = sorted(zip(spam2.values(),spam2.keys()), reverse=True)
    #只要一张excel表的情况，3字典就是全部值
    else:
        #通过压缩zip函数，转化元组，然后用sorted函数排序
        aaa = sorted(zip(spam3.values(),spam3.keys()), reverse=True)
    
    #再转换成字典
    for i, j in aaa:
        spam1[j] = int(i)
    


'''将字典组打入新的xls'''
def dicTranXks(spam1):
    lenSpam1 = len(spam1)
    #含有中文，所以使用了万国码
    wb = xlwt.Workbook(encoding='utf-8')
    worksheet = wb.add_sheet('sheet1', cell_overwrite_ok=True)

    #单元格宽度
    worksheet.col(0).width = 23 * 256
    worksheet.col(1).width = 8 * 256
    worksheet.col(3).width = 23 * 256
    worksheet.col(4).width = 8 * 256
    worksheet.col(6).width = 23 * 256
    worksheet.col(7).width = 8 * 256

    #设置单元格的高度
    worksheet.row(0).height_mismatch = True
    worksheet.row(0).height = 2 * 256

    #字体对象
    font = xlwt.Font()
    font.bold = True        #加粗
    font.height = 25*14     #字大小

    #单元框对象
    borders = xlwt.Borders()
    borders.left = 2
    borders.right = 2
    borders.top = 2
    borders.bottom = 2
    borders.left_colour = 2
    borders.right_colour = 2
    borders.top_colour = 2
    borders.bottom_colour = 2

    #创建style：合并font和borders对象
    style0 = xlwt.XFStyle()
    style0.font = font
    style0.borders = borders

    i, t = 0, 0
    for k,v in spam1.items():
        if i % 15 == 0:
            worksheet.write(int(i % 15), int(0 + (i / 15) * 3), '商品名称', style0)
            worksheet.write(int(i % 15), int(1 + (i / 15) * 3), '数量', style0)
            t += 1
            i += 1
        
        worksheet.write(int(i % 15), int(0 + ( t-1 ) * 3), k, style0)
        worksheet.write(int(i % 15), int(1 + (t-1) * 3), v, style0)
        i += 1

    wb.save('汇总单.xls')



#main
os.chdir(r'G:\大学\大三下\python\xls')
#获得当前目录的文件名
xlsNum = os.listdir(r'.')
#print(os.getcwd())
#日期文件夹中
monthDay = datetime.datetime.now().strftime('%m-%d-%H')

#将首目录的xls文件放入日期文件夹中
#moveXls(xlsNum, monthDay)


os.chdir('.\\'+monthDay+'')
xlsNum = os.listdir(r'.')
spam1,spam2,spam3 = {}, {}, {}

#将文档数据汇总成字典组
sumDataDic(xlsNum)
print(spam1)



#将字典组打入新的xls
dicTranXks(spam1)
