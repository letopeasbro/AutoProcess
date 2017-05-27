# AutoProcess

用Python做的iOS自动化交付脚本

运行环境：python2.7

### Pack

打开终端

cd (AutoProcess文件夹的路径) 

python pack.py -p (\*P) -w (\*W) -s (\*S) -d (D) -c (C)

```
*P: 必填，包含workspace文件的文件夹路径

*W: 必填，workspace文件名，例test.xcworkspace

*S: 必填，待打包的scheme名，例test

D: 非必填，可填入device/simulator，默认device，即默认打真机安装包

C: 非必填，可填入Debug/Release，默认Debug，即默认打Debug版本安装包
```

**注意**：如果使用git进行版本管理，并且存在.gitignore文件的话，会在.gitignore文件里添加archive保存路径和ipa保存路径的忽略。

**结果**：会在workspace文件路径下存在(scheme)_ipa文件夹，里面保存了得到的.ipa文件。
