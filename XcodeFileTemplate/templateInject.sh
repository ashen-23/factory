currentPath=`pwd`

cd /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/Xcode/Templates/File\ Templates/Source/

# 备份
tar -cf backup.xctemplate.tar Cocoa\ Touch\ Class.xctemplate 

# 移除
rm -rf "Cocoa Touch Class.xctemplate"

# 拷贝
cp -rf $currentPath"/Cocoa Touch Class.xctemplate" "Cocoa Touch Class.xctemplate"

