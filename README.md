# Yeelink-ven-fan

这是一个用于Hame assistant的Yeelink凉霸自定义组件

Please follow the instructions on [Retrieving the Access Token](https://www.home-assistant.io/components/vacuum.xiaomi_miio/#retrieving-the-access-token) to get the API token to use in the configuration.yaml file.

Credits: Thanks to [Rytilahti](https://github.com/rytilahti/python-miio) for all the work.件


## 特点

### 凉霸
* 开关机
* 风量(两档)
* 摆风(摇头)
* 固定角度(65-120)

## 安装


```yaml
# configuration.yaml

fan:
  - platform: yeelink
    name: 凉霸
    host: 192.168.130.71
    token: b7c4a758c21555d2c24b1d9e41ce47d
```
配置变量
- **host** (*必须*): 凉霸的IP地址.
- **token** (*必须*): 凉霸的API token.
- **name** (*选填*): 自定义名字.

## 平台服务

### Service `yeelink_set_angle`

设置凉霸风口角度

| 服务数据属性               | 选项      | 描述                                                                       |
|---------------------------|----------|----------------------------------------------------------------------------|
| `entity_id`               |      必选 | 指定一个凉霸的ID                                                            |
| `angle`                   |      必选 | 凉霸的风口角度可用用值范围是 65-120                                          |

