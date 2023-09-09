# chinamobile-hackson
**请保证每次提交的版本均为可通过name = main函数接受两个参数运行的**

即 
~~~
if __name__ == "__main__":
    to_pred_path  = sys.argv[1] # 数据路径
    result_save_path = sys.argv[2] # 输出路径
    main(to_pred_path,result_save_path) # 运行主函数
~~~ 
应保持不变
## 如何修改使用trainA.csv 还是testdata.cv
在`tools.py`中`get_fcsv_path()`中更改
```
  #file_path = os.path.join(parent_directory, 'input', '数据安全赛道', 'trainA.csv')
  file_path = os.path.join(parent_directory, 'input', '数据安全赛道', 'testdata.csv')
```
这两行的注释即可
## 如何运行程序
run file in python console
然后输入`test()`
