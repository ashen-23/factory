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