from typing import List

from pydantic import BaseModel


class File(BaseModel):
    group_id: int  # 群号
    file_id: str  # 文件ID
    file_name: str  # 文件名
    busid: int  # 文件类型
    file_size: int  # 文件大小
    upload_time: int  # 上传时间
    dead_time: int  # 过期时间,永久文件恒为0
    modify_time: int  # 最后修改时间
    download_times: int  # 下载次数
    uploader: int  # 上传者ID
    uploader_name: str  # 上传者名字


class Folder(BaseModel):
    group_id: int  # 群号
    folder_id: str  # 文件夹ID
    folder_name: str  # 文件名
    create_time: int  # 创建时间
    creator: int  # 创建者
    creator_name: str  # 创建者名字
    total_file_count: int  # 子文件数量


class GroupFileResponse(BaseModel):
    files: List[File]  # 文件列表
    folders: List[Folder]  # 文件列表


class FileUrlResponse(BaseModel):
    url: str  # 文件下载链接
