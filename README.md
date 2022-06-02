<!--
 * @Author        : fineemb
 * @Github        : https://github.com/fineemb
 * @Description   : 
 * @Date          : 2019-11-18 22:30:07
 * @LastEditors   : fineemb
 * @LastEditTime  : 2020-01-31 23:54:43
 -->
# Yeelight-ven-fan

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

这是一个用于Hame assistant的Yeelight智能凉霸自定义组件
![ven_fan](https://img.youpin.mi-img.com/shopmain/19e12ab2af3a8db1dea1248ef2e36851.png)
Please follow the instructions on [Retrieving the Access Token](https://www.home-assistant.io/components/vacuum.xiaomi_miio/#retrieving-the-access-token) to get the API token to use in the configuration.yaml file.

Credits: Thanks to [Rytilahti](https://github.com/rytilahti/python-miio) for all the work.


## 特点

### 凉霸
* 开关机
* 风量(两档)
* 摆风(摇头)
* 固定角度(65-120)
* 负离子
* 上电运行

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

### 服务  `yeelink_set_angle`

设置凉霸风口角度

| 服务数据属性               | 选项      | 描述                                                                       |
|---------------------------|----------|----------------------------------------------------------------------------|
| `entity_id`               |      必选 | 指定一个凉霸的ID                                                            |
| `angle`                   |      必选 | 凉霸的风口角度可用用值范围是 65-120                                          |

### 服务  `yeelink_set_init`

设置凉霸是否默认上电运行

| 服务数据属性               | 选项      | 描述                                                                       |
|---------------------------|----------|----------------------------------------------------------------------------|
| `entity_id`               |      必选 | 指定一个凉霸的ID                                                            |
| `init`                    |      必选 | 开关上电运行, 值为on/off                                                    |

### 服务  `yeelink_set_anion`

设置凉霸负离子开关

| 服务数据属性               | 选项      | 描述                                                                       |
|---------------------------|----------|----------------------------------------------------------------------------|
| `entity_id`               |      必选 | 指定一个凉霸的ID                                                            |
| `anion`                   |      必选 | 开关负离子, 值为on/off                                                      |

