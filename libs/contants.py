import datetime

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
# 导播管理界面
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
# 个人设备信息
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

# 首页布局接口
# 首页布局接口 授权信息Header+Token, 参数表单提交
URL_HOMEPAGE = '/app/content/homepage'
HOME_PAGE = 1
HOME_NUM = 5
# 设备页布局接口 授权信息Header+Token, 参数无
URL_DEVICEDETAIL = '/app/content/deviceDetail'

# 个人名片页接口
# 个人名片页浏览接口 授权信息Header+Token, 参数无
URL_VISITCARD = '/app/content/visitingCard'
# 个人名片页编辑接口 授权信息Header+Token, 参数无
URL_EDITVISCARD = '/app/content/editVisitingCard'

# 活动页接口 请求参数title activity_time 授权信息Header+Token
URL_CREATE = '/app/v2/activity/create'
create_t = datetime.datetime.now().strftime('%Y-%m-%d')
CREATE_TITLE = 'xia_test' + create_t
CREATE_TIME = create_t

# https://www.baidu.com/img/bd_logo1.png?where=super

# 图片上传成功回调
URL_CALLBACK = '/app/upload/callback'
DATA = {
    "code": 200,
	"uid": 10,
	"activity_id": 53,
	"file_size": 182157,
    "image-frames": 1,
    "image-height": 1280,
    "image-type": "JPEG",
    "image-width": 960,
    "message": "ok",
    "mimetype": "image/jpeg",
    "time": "1542351989",
    "url": "/app/activity/154235132510815860/images/c55717edfaac1a62eed6f6d28e6f0a20f4c755e5.jpg",
}

# 活动接口 授权信息Header+Token 参数活动id
# 修改活动
URL_ACTIVITY_EDIT = '/activity/edit'

# 删除直播
URL_ACTIVITY_DELETE = '/activity/delete'

# 开始直播
URL_ACTIVITY_START = '/activity/start'

# 关闭直播
URL_ACTIVITY_CLOSE = '/activity/close'

# 摄影师参数id
CAMERIST_INVITE_ID = 636
CAMERIST_UID = 98
# 摄影师加入
URL_INVITE = '/camerist/invite'

# 摄影师退出直播
URL_QUIT = '/camerist/quit'

# 摄影师 被 移出直播
URL_OUT = '/camerist/out'

# 分配摄影师到场地
URL_ALLOT = '/camerist/allot'

# 用户摄影师修改资料
URL_USER_UPDATE = '/user/update'

# 认证摄影师
# URL_USER_IDENTITY = '/user/identity'
# SN = '154328393018212518'

# 预约摄影师
URL_BOOKING = '/booking'
BOOK_DATA = {
    'name': 'xiayong',
    'mobile': '18601927460',
    'location': '上海',
    'category_id': 1,
    'to_uid': 0,
    'when': '2018-12-12'
}

# 举报
URL_REPORT = '/report'
REPORT_DATA = {
    'id': 488,
    'text': 1
}


