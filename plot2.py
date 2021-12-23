"""
说明:
输入的数据需要转为csv格式, 数据为需要画图的片段(不能包含第一行的列名)
一次只能画一种类型的点,
    需要把所有点画到一个图上就把第一次调用的输出文件作为第二次调用的输入文件,第二次不需要加白边
"""
import cv2
import math

font = cv2.FONT_ITALIC


# 参数说明 数据路径 输入图片, 需要画图的类型, 颜色, 时间转换成半径的比例, 输出图片, 是否加白边
def plot_15s(data_path, in_file, state, color, time2pixel_ratio, target_file, need_border):
    orin_img = cv2.imread(in_file)
    img = cv2.resize(orin_img, (1920, 1080))
    if need_border:
        img = cv2.copyMakeBorder(img, 100, 100, 100, 100, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    f = open(data_path, 'r')
    now_state = ''
    i = 0
    now_x, now_y = -1, -1
    wait4next_line = False
    for line in f.readlines():
        elements = line.split('\t')
        if len(elements) < 56:
            continue
        tmp_state = elements[54]#眼动类型 BC->79

        if wait4next_line:
            try:
                duration = int(elements[55])#眼动duration BD 55->80
                x, y = int(elements[26]), int(elements[27])#位置 Gaze point X AA  AB   ->39
                x, y = x + 100, y + 100
            except ValueError:
                wait4next_line = True
                continue
            wait4next_line = False
            i += 1
            cv2.circle(img, (x, y), int(math.sqrt(duration * time2pixel_ratio)), color, -1)
            cv2.putText(img, str(i), (x - 10, y + 10), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
            if now_x != -1:
                cv2.line(img, (x, y), (now_x, now_y), 2)
            now_x, now_y = x, y

        if tmp_state == now_state:
            continue
        now_state = tmp_state
        if now_state != state:
            continue
        try:
            duration = int(elements[55])
            x, y = int(elements[26]), int(elements[27])
            x, y = x + 100, y + 100
        except ValueError:
            wait4next_line = True
            continue
        i += 1
        cv2.circle(img, (x, y), int(math.sqrt(duration * time2pixel_ratio)), color, -1)
        if now_x != -1:
            cv2.line(img, (x, y), (now_x, now_y), color)
        cv2.putText(img, str(i), (x - 10, y + 10), font, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
        now_x, now_y = x, y
    print("end")
    cv2.imwrite(target_file, img)


if __name__ == '__main__':
	'''
	plot_15s('excel/Project77-70 Recording18.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77-70 Recording18-f.png', True)
	plot_15s('excel/Project77-70 Recording25.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77-70 Recording25-f.png', True)
	plot_15s('excel/Project77-70 Recording26.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77-70 Recording26-f.png', True)
	plot_15s('excel/Project77-70 Recording31.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77-70 Recording31-f.png', True)
	plot_15s('excel/Project77-70 Recording46.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77-70 Recording46-f.png', True)
	plot_15s('excel/Project77-70 Recording70.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77-70 Recording70-f.png', True)
	plot_15s('excel/Project63-57 Recording23.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project63-57 Recording23-f.png', True)
	plot_15s('excel/Project63-57 Recording24.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project63-57 Recording24-f.png', True)
	plot_15s('excel/Project63-57 Recording28.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project63-57 Recording28-f.png', True)
	plot_15s('excel/Project63-57 Recording30.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project63-57 Recording30-f.png', True)
	plot_15s('excel/Project63-57 Recording32.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project63-57 Recording32-f.png', True)
	plot_15s('excel/Project63-57 Recording63.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project63-57 Recording63-f.png', True)
	plot_15s('excel/Project77_56-49 Recording20.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77_56-49 Recording20-f.png', True)
	plot_15s('excel/Project77_56-49 Recording27.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77_56-49 Recording27-f.png', True)
	plot_15s('excel/Project77_56-49 Recording33.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77_56-49 Recording33-f.png', True)
	plot_15s('excel/Project77_56-49 Recording35.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77_56-49 Recording35-f.png', True)
	plot_15s('excel/Project77_56-49 Recording38.tsv', 'background.png', 'Fixation', (255, 255, 0), 3, 'out/Project77_56-49 Recording38-f.png', True)
	
	plot_15s('excel/Project77-70 Recording18.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77-70 Recording18.png', True)
	plot_15s('excel/Project77-70 Recording25.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77-70 Recording25.png', True)
	plot_15s('excel/Project77-70 Recording26.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77-70 Recording26.png', True)
	plot_15s('excel/Project77-70 Recording31.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77-70 Recording31.png', True)
	plot_15s('excel/Project77-70 Recording46.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77-70 Recording46.png', True)
	plot_15s('excel/Project77-70 Recording70.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77-70 Recording70.png', True)
	plot_15s('excel/Project63-57 Recording23.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project63-57 Recording23.png', True)
	plot_15s('excel/Project63-57 Recording24.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project63-57 Recording24.png', True)
	plot_15s('excel/Project63-57 Recording28.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project63-57 Recording28.png', True)
	plot_15s('excel/Project63-57 Recording30.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project63-57 Recording30.png', True)
	plot_15s('excel/Project63-57 Recording32.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project63-57 Recording32.png', True)
	plot_15s('excel/Project63-57 Recording63.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project63-57 Recording63.png', True)
	plot_15s('excel/Project77_56-49 Recording20.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77_56-49 Recording20.png', True)
	plot_15s('excel/Project77_56-49 Recording27.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77_56-49 Recording27.png', True)
	plot_15s('excel/Project77_56-49 Recording33.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77_56-49 Recording33.png', True)
	plot_15s('excel/Project77_56-49 Recording35.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77_56-49 Recording35.png', True)
	plot_15s('excel/Project77_56-49 Recording38.tsv', 'background.png', 'Unclassified', (0, 0, 255), 3, 'out-u/Project77_56-49 Recording38.png', True)
	
	plot_15s('excel/Project77-70 Recording18.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77-70 Recording18.png', True)
	plot_15s('excel/Project77-70 Recording25.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77-70 Recording25.png', True)
	plot_15s('excel/Project77-70 Recording26.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77-70 Recording26.png', True)
	plot_15s('excel/Project77-70 Recording31.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77-70 Recording31.png', True)
	plot_15s('excel/Project77-70 Recording46.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77-70 Recording46.png', True)
	plot_15s('excel/Project77-70 Recording70.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77-70 Recording70.png', True)
	plot_15s('excel/Project63-57 Recording23.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project63-57 Recording23.png', True)
	plot_15s('excel/Project63-57 Recording24.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project63-57 Recording24.png', True)
	plot_15s('excel/Project63-57 Recording28.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project63-57 Recording28.png', True)
	plot_15s('excel/Project63-57 Recording30.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project63-57 Recording30.png', True)
	plot_15s('excel/Project63-57 Recording32.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project63-57 Recording32.png', True)
	plot_15s('excel/Project63-57 Recording63.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project63-57 Recording63.png', True)
	plot_15s('excel/Project77_56-49 Recording20.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77_56-49 Recording20.png', True)
	plot_15s('excel/Project77_56-49 Recording27.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77_56-49 Recording27.png', True)
	plot_15s('excel/Project77_56-49 Recording33.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77_56-49 Recording33.png', True)
	plot_15s('excel/Project77_56-49 Recording35.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77_56-49 Recording35.png', True)
	plot_15s('excel/Project77_56-49 Recording38.tsv', 'background.png', 'Saccade', (255, 255, 0), 3, 'out-s/Project77_56-49 Recording38.png', True)
	'''

#数据路径 输入图片, 需要画图的类型, 颜色, 时间转换成半径的比例, 输出图片, 是否加白边
	'''三种类型叠加图,往unclassified叠加fixation,再叠sacaade'''
	plot_15s('read-houshu04/Project63-57-Recording23.tsv', 'background-houshu04.jpg', 'Fixation', (255, 0, 0), 2, 'out-houshu04/Project63-57-Recording23.png', True)
	# plot_15s('newexcel/70.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/70.png', True)
	# plot_15s('newexcel/71.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/71.png', True)
	# plot_15s('newexcel/72.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/72.png', True)
	# plot_15s('newexcel/77.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/77.png', True)
	# plot_15s('newexcel/78.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/78.png', True)
	# plot_15s('newexcel/79.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/79.png', True)
	# plot_15s('newexcel/80.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/80.png', True)
	# plot_15s('newexcel/82.tsv', 'background.png', 'Fixation', (255, 0, 0), 2, 'new-out/82.png', True)
    #
	# plot_15s('excel/Project77-70 Recording18.tsv', 'out-u/Project77-70 Recording18.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77-70 Recording18.png', True)
	# plot_15s('excel/Project77-70 Recording25.tsv', 'out-u/Project77-70 Recording25.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77-70 Recording25.png', True)
	# plot_15s('excel/Project77-70 Recording26.tsv', 'out-u/Project77-70 Recording26.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77-70 Recording26.png', True)
	# plot_15s('excel/Project77-70 Recording31.tsv', 'out-u/Project77-70 Recording31.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77-70 Recording31.png', True)
	# plot_15s('excel/Project77-70 Recording46.tsv', 'out-u/Project77-70 Recording46.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77-70 Recording46.png', True)
	# plot_15s('excel/Project77-70 Recording70.tsv', 'out-u/Project77-70 Recording70.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77-70 Recording70.png', True)
	# plot_15s('excel/Project63-57 Recording23.tsv', 'out-u/Project63-57 Recording23.png', 'Fixation', (255, 0, 0), 3, 'temp/Project63-57 Recording23.png', True)
	# plot_15s('excel/Project63-57 Recording24.tsv', 'out-u/Project63-57 Recording24.png', 'Fixation', (255, 0, 0), 3, 'temp/Project63-57 Recording24.png', True)
	# plot_15s('excel/Project63-57 Recording28.tsv', 'out-u/Project63-57 Recording28.png', 'Fixation', (255, 0, 0), 3, 'temp/Project63-57 Recording28.png', True)
	# plot_15s('excel/Project63-57 Recording30.tsv', 'out-u/Project63-57 Recording30.png', 'Fixation', (255, 0, 0), 3, 'temp/Project63-57 Recording30.png', True)
	# plot_15s('excel/Project63-57 Recording32.tsv', 'out-u/Project63-57 Recording32.png', 'Fixation', (255, 0, 0), 3, 'temp/Project63-57 Recording32.png', True)
	# plot_15s('excel/Project63-57 Recording63.tsv', 'out-u/Project63-57 Recording63.png', 'Fixation', (255, 0, 0), 3, 'temp/Project63-57 Recording63.png', True)
	# plot_15s('excel/Project77_56-49 Recording20.tsv', 'out-u/Project77_56-49 Recording20.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77_56-49 Recording20.png', True)
	# plot_15s('excel/Project77_56-49 Recording27.tsv', 'out-u/Project77_56-49 Recording27.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77_56-49 Recording27.png', True)
	# plot_15s('excel/Project77_56-49 Recording33.tsv', 'out-u/Project77_56-49 Recording33.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77_56-49 Recording33.png', True)
	# plot_15s('excel/Project77_56-49 Recording35.tsv', 'out-u/Project77_56-49 Recording35.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77_56-49 Recording35.png', True)
	# plot_15s('excel/Project77_56-49 Recording38.tsv', 'out-u/Project77_56-49 Recording38.png', 'Fixation', (255, 0, 0), 3, 'temp/Project77_56-49 Recording38.png', True)
	#
	plot_15s('read-houshu04/Project63-57-Recording23.tsv', 'out-houshu04/Project63-57-Recording23.png', 'Saccade', (255, 0, 0), 2, 'out-houshu04/Project63-57-Recording23f+s.png', True)

	# plot_15s('excel/Project77-70 Recording18.tsv', 'temp/Project77-70 Recording18.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77-70 Recording18.png', True)
	# plot_15s('excel/Project77-70 Recording25.tsv', 'temp/Project77-70 Recording25.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77-70 Recording25.png', True)
	# plot_15s('excel/Project77-70 Recording26.tsv', 'temp/Project77-70 Recording26.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77-70 Recording26.png', True)
	# plot_15s('excel/Project77-70 Recording31.tsv', 'temp/Project77-70 Recording31.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77-70 Recording31.png', True)
	# plot_15s('excel/Project77-70 Recording46.tsv', 'temp/Project77-70 Recording46.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77-70 Recording46.png', True)
	# plot_15s('excel/Project77-70 Recording70.tsv', 'temp/Project77-70 Recording70.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77-70 Recording70.png', True)
	# plot_15s('excel/Project63-57 Recording23.tsv', 'temp/Project63-57 Recording23.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project63-57 Recording23.png', True)
	# plot_15s('excel/Project63-57 Recording24.tsv', 'temp/Project63-57 Recording24.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project63-57 Recording24.png', True)
	# plot_15s('excel/Project63-57 Recording28.tsv', 'temp/Project63-57 Recording28.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project63-57 Recording28.png', True)
	# plot_15s('excel/Project63-57 Recording30.tsv', 'temp/Project63-57 Recording30.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project63-57 Recording30.png', True)
	# plot_15s('excel/Project63-57 Recording32.tsv', 'temp/Project63-57 Recording32.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project63-57 Recording32.png', True)
	# plot_15s('excel/Project63-57 Recording63.tsv', 'temp/Project63-57 Recording63.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project63-57 Recording63.png', True)
	# plot_15s('excel/Project77_56-49 Recording20.tsv', 'temp/Project77_56-49 Recording20.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77_56-49 Recording20.png', True)
	# plot_15s('excel/Project77_56-49 Recording27.tsv', 'temp/Project77_56-49 Recording27.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77_56-49 Recording27.png', True)
	# plot_15s('excel/Project77_56-49 Recording33.tsv', 'temp/Project77_56-49 Recording33.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77_56-49 Recording33.png', True)
	# plot_15s('excel/Project77_56-49 Recording35.tsv', 'temp/Project77_56-49 Recording35.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77_56-49 Recording35.png', True)
	# plot_15s('excel/Project77_56-49 Recording38.tsv', 'temp/Project77_56-49 Recording38.png', 'Saccade', (0, 255, 0), 3, 'out-all/Project77_56-49 Recording38.png', True)
	
	