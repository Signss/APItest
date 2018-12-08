# 测试环境接口域名
DOMAIN = 'https://dapi.livepic.com.cn'
# 用户手机号
MOBILE = '16601297365'
# 测试环境固定验证码数值
FIX_CODE = '123456'
# 1.1.公共参数
COMMON_PARA = {
"Authorization": "Bearer b6a9817f4d9ec7ff676f2e0159ddda20fc48502e8b903c1c8b742d0b91d1cd755bee32721df97",
"AppVersion": "1.0.1",
"UserId": 53
}
# token前缀
TOKEN_PREFIX = 'Bearer '
# 方法为get请求的接口
# 配置参数接口接口：GET /app/init请求参数：无
URL_CONFIG = '/app/init'
# 升级更新接口
URL_CHECKUPDATE = '/app/checkUpdate'
# 购买页
URL_BY = '/buy'
# 全国城市列表
URL_CITY = '/city'
# 又拍云上传签名
URL_UPLOADSIGN = '/uploadsign'
# 计费商品列表
URL_GOODS = '/goods'


# 活动列表
URL_ACTIVITY = '/activity'
# 资料页
URL_ACTIVITY_DATA = '/activity/data'
# 摄影师管理详情页
URL_CAMERIST = '/camerist'
# 直播原相册
URL_PIC_ALBUM = '/picture/album'
# 直播详情页
URL_PIC_DETAIL = '/picture/detail'
# 用户已上传图片列表
URL_USER_PIC = '/user/picture'
# 导播管理节目
URL_EDITOR = '/editor/list'
# 编辑室列表
URL_EDIT = '/edit/list'
# 预约摄影师列表
URL_RESERVE = '/reserve/list'
# 直播预sn
URL_PREP = '/prep'
# 分类列表
URL_CATEGORY = '/category'
# 我预约别人的
URL_USER_MY = '/user/mybooking'
# 别人预约我的
URL_MYCUSTOMER = '/user/mycustomer'
# 我的关注列表
URL_USER_SUB = '/user/subscribe'
# 二维码扫描
URL_SCAN = '/scan'
# 分享加强版
URL_SHARE = '/share'
# 设备码校验
URL_DEVICE = '/device/verify'
# 消息列表
URL_MESSAGE = '/user/message'
# 个人设置信息
URL_USER_DEVICE = '/user/device'
# banner
URL_BANNER = '/banner'
# 设备相册
URL_DEVICE_ALBUM = '/device/album'
# 验证邀请码
URL_INVITE_CODE = '/invite-code'
# 已结束的直播列表（在该直播下有身份）
URL_ACTIVITY_END = '/activity/end/list'

# 方法为post请求的接口
# 手机验证码接口
URL_CODE = '/code'
# 登陆接口
URL_LOGIN = '/user/authorization'
# 图片上传成功回调接口
URL_UPLOAD_CALLBACK = '/app/upload/callback'
