# MySQLiteAPI
用于个人任务（如爬虫等）保存数据的轻量型数据库（SQLite）接口。
目前仅实现了基础的增删查改功能，具体如下：
  create_sql()       # 创建SQLite数据库文件
  insert_data()      # 向数据库文件中插入一条信息
  insert_datas()     # 向数据库文件中插入多条信息
  fetchone_data()    # 获取表内的所有数据并返回数据列表
  fetchall_datas()   # 获取表内的一条数据并返回数据元组
  update_data()      # 更新一条已有数据
  update_datas()     # 更新多条已有数据
  delete_data()      # 删除一条已有数据
  delete_datas()     # 批量删除多条数据
