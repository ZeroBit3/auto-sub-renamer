import os
import re

# 定义常见的视频和字幕扩展名，可根据需求自行增删
VIDEO_EXTS = {'.mkv', '.mp4', '.avi', '.rmvb', '.wmv'}
SUB_EXTS = {'.ass', '.srt', '.ssa', '.vtt'}

def get_episode_num(filename):
    # 提前剔除分辨率、编码等常见的干扰数字
    clean_name = re.sub(r'(1080p|720p|2160p|4k|x264|x265|h264|h265|8bit|10bit)', '', filename, flags=re.IGNORECASE)
    
    # 匹配常见的集数格式：E01, EP01, 第01集, - 01, [01] 等
    pattern = r'(?:[Ee][Pp]?\s*0*(\d+))|(?:第\s*0*(\d+)\s*[集话])|(?:-\s*0*(\d+)\s*(?:[vV]\d)?\.)|(?:\[0*(\d+)\])|(?:\s0*(\d+)\s)'
    match = re.search(pattern, clean_name)
    
    if match:
        for group in match.groups():
            if group is not None:
                return int(group)
                
    # 如果没有匹配到明显的集数标识，提取文件名中剩下的最后一组纯数字
    numbers = re.findall(r'\d+', clean_name)
    return int(numbers[-1]) if numbers else None

def main():
    folder_path = '.'
    
    all_files = os.listdir(folder_path)
    
    # 根据扩展名筛选视频和字幕文件
    video_files = [f for f in all_files if os.path.splitext(f)[1].lower() in VIDEO_EXTS]
    sub_files = [f for f in all_files if os.path.splitext(f)[1].lower() in SUB_EXTS]

    # 建立 集数 -> 视频文件名 的映射字典
    video_map = {}
    for video in video_files:
        ep_num = get_episode_num(video)
        if ep_num is not None:
            video_map[ep_num] = video

    # 遍历并重命名字幕文件
    for sub in sub_files:
        ep_num = get_episode_num(sub)
        
        if ep_num is not None and ep_num in video_map:
            video_name = video_map[ep_num]
            
            # 提取视频主体名和字幕原扩展名
            video_base = os.path.splitext(video_name)[0]
            sub_ext = os.path.splitext(sub)[1]
            
            # 拼接新的字幕文件名
            new_sub_name = video_base + sub_ext
            
            old_path = os.path.join(folder_path, sub)
            new_path = os.path.join(folder_path, new_sub_name)
            
            if old_path != new_path:
                print(f"重命名: {sub}  --->  {new_sub_name}")
                os.rename(old_path, new_path)

    print("执行完毕。")

if __name__ == '__main__':
    main()