# factory


## AutomaticCode

![](./resources/AutomaticCode.png)


```
生成简易 OC 视图代码

参数描述:
    viewName:ViewType:layoutType
    视图名称:视图类型:布局类型
    
    eg: imgView:UIImageView
    
    eg: imgView:UIImageView:e
        (e: make.edges (支持五种布局方式e/t/l/a/s))
        
    eg: imgView:i 
        (i 是UIImageView的简写)
        
    eg: :i
        (省略的名称默认为类型去掉'UI'前缀)
        
    
    eg: imgView:i collectionView:c tableView:UITableView
        (支持同时生成生成多个视图)
```

### 调用
1. 可以使用`python3 xxx.py`运行

```
python3 ./AutomaticCode.py imgView:i nameLabel:l
```
2. 可以使用`./xxx.py`运行

```Shell
# 首先需要给xxx.py设置执行权限 
chmod 777 ./xxx.py

# 执行
./AutomaticCode.py imgView:i nameLabel:l
```

3. shell alias 执行

```Shell
# 以别名的形式运行

#alias alias_name='you code'
alias ac='python3 /xxx/AutomaticCode.py'

# 执行
ac imgView:i nameLabel:l
```