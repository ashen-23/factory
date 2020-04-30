#
#  AutomaticCode.py
#
#  Created by ashen23 on 2020/4/2130.
#  Copyright © 2020. All rights reserved.

import sys
import os

helpInfo = '''
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
'''

### 以下是模板

# 默认padding
paddings = '15'

viewMap = {'c': 'UICollectionView', 't':'UITableView', 'l':'UILabel', 
           't':'UITextField', 'tv':'UITextView', 'i':'UIImageView',
            'b':'UIButton', 'v':'UIView'}

getFunc = '''
- (<#type#> *)<#name#> {
    if (!_<#name#>) {
        _<#name#> = [[<#type#> alloc] init];
        <#extension#>
    }
    return _<#name#>;
}
'''

# 默认：左+上
layoutDefault = '''
[<#parent#> addSubview:self.<#name#>];
[self.<#name#> mas_makeConstraints:^(MASConstraintMaker *make) {
    make.left.equalTo(<#parent#>).offset(<#padding#>);
    make.top.equalTo(<#parent#>).offset(<#padding#>);
}];
'''

# edge
layoutEdge = '''
[<#parent#> addSubview:self.<#name#>];
[self.<#name#> mas_makeConstraints:^(MASConstraintMaker *make) {
    make.edges.equalTo(<#parent#>);
}];
'''

# 上左+宽高
layoutSize = '''
[<#parent#> addSubview:self.<#name#>];
[self.<#name#> mas_makeConstraints:^(MASConstraintMaker *make) {
    make.left.equalTo(<#parent#>).offset(<#padding#>);
    make.top.equalTo(<#parent#>).offset(<#padding#>);
    make.width.equalTo(<#width#>);
    make.height.equalTo(<#height#>);
}];
'''

# 上下左右
layoutAll = '''
[<#parent#> addSubview:self.<#name#>];
[self.<#name#> mas_makeConstraints:^(MASConstraintMaker *make) {
    make.left.equalTo(<#parent#>).offset(<#padding#>);
    make.top.equalTo(<#parent#>).offset(<#padding#>);
    make.right.equalTo(<#parent#>).offset(-<#padding#>);
    make.height.equalTo(<#parent#>).offset(-<#padding#>);
}];
'''

# 左侧与左面视图右侧相关
layoutL = '''
[<#parent#> addSubview:self.<#name#>];
[self.<#name#> mas_makeConstraints:^(MASConstraintMaker *make) {
    make.left.equalTo(<#last#>.mas_bottom).offset(<#padding#>);
    make.top.equalTo(<#parent#>).offset(<#padding#>);
}];
'''

# 顶部与上面视图的底部相关
layoutT = '''
[<#parent#> addSubview:self.<#name#>];
[self.<#name#> mas_makeConstraints:^(MASConstraintMaker *make) {
    make.left.equalTo(<#parent#>).offset(<#padding#>);
    make.top.equalTo(<#last#>.mas_bottom).offset(<#padding#>);
}];
'''

module_button = '''
        [_<#name#> setTitle:<#buttonTitle#> forState:UIControlStateNormal];
'''

module_tableView = '''
        _<#name#>.delegate = self;
        _<#name#>.dataSource = self;
'''

module_collection = '''
        UICollectionViewFlowLayout *layout = [[UICollectionViewFlowLayout alloc] init];
        layout.itemSize = CGSizeMake(<#55#>, <#55#>);
        layout.minimumLineSpacing = <#15#>;
        layout.minimumInteritemSpacing = <#10#>;
        
        _<#name#> = [[UICollectionView alloc] initWithFrame:CGRectMake(0, 0, kScreenWidth, kScreenHeight) collectionViewLayout:layout];
        
        _<#name#>.backgroundColor = [Theme colorWhite];
        
        [_<#name#> registerClass:[<#PHMineCell#> class] forCellWithReuseIdentifier:<#@"PHMineCell"#>];
        
        _<#name#>.delegate = self;
        _<#name#>.dataSource = self;
'''

module_label = '''
    _<#name#>.textColor = [Theme themeColorGray];
    _<#name#>.font = [UIFont systemFontOfSize:14.f];
    _<#name#>.numberOfLines = 0;
    _<#name#>.textAlignment = NSTextAlignmentCenter;
    _<#name#>.text = <#text#>;
'''

### 以上是模板

def highlightPrint(text):
    print('\033[33m{}\033[0m'.format(text))

def errorPrint(error):
    print('\033[31m{}\033[0m'.format(error))

# 处理参数
def makeParams(info):
    params = info.split(":")
    name = params[0]
    if len(params) <= 1:
        params.append('v')
        params.append('')
    if name == '':
        name = getClass(params[1])[2:]
        name = name[0].lower() + name[1:]
    if len(params) <= 2:
        params.append('d')
    return (name, params[1], params[2])


def getClass(key):
    return viewMap.get(key, key)

def getExtension(name, className):
    result = ''
    if className == 'UICollectionView':
        result = module_collection
    elif className == 'UIButton':
        result = module_button
    elif className == 'UITableView':
        result = module_tableView
    return result.replace('<#name#>', name)

def makeProperty(name, className):
    return "@property (nonatomic, strong){} *{};".format(className, name)

def makeGetFunc(name, className):
    extensionStr = getExtension(name, className)
    tempStr = getFunc
    if className == 'UICollectionView':
        tempStr = tempStr.replace('_<#name#> = [[<#type#> alloc] init];', '')
    return tempStr.replace('<#name#>', name).replace('<#type#>', className).replace('<#extension#>', extensionStr)

def makeMasonry(name, isVC, relation, last, padding):
    parentName = 'self.view' if isVC else 'self'
    result = ''
    if relation == 't':
        result = layoutT.replace('<#last#>', 'self.{}'.format(last))
    elif relation == 'l':
        result = layoutL.replace('<#last#>', 'self.{}'.format(last))
    elif relation == 'e':
        result = layoutEdge
    elif relation == 's':
        result = layoutSize
    elif relation == 'a':
        result = layoutAll
    elif relation == 'd':
        result = layoutDefault

    return result.replace('<#parent#>', parentName).replace('<#name#>', name).replace('<#padding#>', padding)

# 执行代码
def run(info):
    # 参数
    properties = []
    # get方法
    gets = []
    # 布局
    layouts = []
    
    params = info.split(' ')
    views = []

    # 分解参数和视图
    isVC = True
    padding = paddings
    for param in params:
        if param.startswith('-'):
            if param == '-View':
                isVC = False
            elif param.startswith('-p:'):
                padding = param.replace('-p:', '')
            pass
        else:
            if ':' in param:
                views.append(param)

    # 上一个视图名称
    lastName = ''
    for view in views:
         params = makeParams(view)
         name = params[0]
         className = getClass(params[1])
         layoutName = params[2]
         properties.append(makeProperty(name, className))
         gets.append(makeGetFunc(name, className))
         layouts.append(makeMasonry(name, isVC, layoutName, lastName, padding))
         lastName = name
    
    print('\n######################\n######## 🎉🎉🎉 ######\n######################\n')
    res = '#pragma mark - Property\n\n' + '\n'.join(properties) + '\n\n#pragma mark - Getter && Setter\n' + ''.join(gets) + '\n\n#pragma mark - Builder\n' + ''.join(layouts)
    highlightPrint(res)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        errorPrint('参数输入有误，请使用-help查看使用说明')
    elif '-help' in sys.argv:
        highlightPrint(helpInfo)
    else:
        os.system('clear')
        run(' '.join(sys.argv[1:]))
