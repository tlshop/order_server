

import datetime
from libs.utils.mytime import send_toTimestamp
from alipay import AliPay
from decimal import Decimal
from libs.utils.log import logger
from libs.utils.exceptions import PubErrorCustom

from education.config.params import \
    AliPay_Appid,AliPay_app_private_key,AliPay_alipay_public_key,AliPay_way,Alipay_callbackUrl,Alipay_callbackUrlForVip


def get_today_start_end_timestamp():
    return send_toTimestamp(datetime.datetime.now().strftime('%Y-%m-%d' ) +' 00:00:01'), \
                send_toTimestamp(datetime.datetime.now().strftime('%Y-%m-%d') + ' 23:59:59')


def get_today_start_end_time():
    return datetime.datetime.now().strftime('%Y-%m-%d' ) +' 00:00:01', \
                 datetime.datetime.now().strftime('%Y-%m-%d') + ' 23:59:59'


class AlipayBase(object):

    def __init__(self,isVip=None):

        # print(AliPay_alipay_private_key)
        #
        #
        # print(AliPay_alipay_public_key)
        #
        # print(AliPay_Appid)

        self.alipay = AliPay(
            appid=AliPay_Appid,
            app_notify_url=Alipay_callbackUrl if not isVip else Alipay_callbackUrlForVip,
            app_private_key_string=AliPay_app_private_key,
            alipay_public_key_string=AliPay_alipay_public_key,
            sign_type="RSA2",
            debug=False,  # 上线则改为False , 沙箱True
        )

    def create(self,order_id,amount,subject=None):

        order_string = self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(amount.quantize(Decimal('0.00'))),
            subject='支付订单:%s' % order_id if not subject else subject,
            return_url=None,
            notify_url=None,
        )

        pay_url = '{}?{}'.format(AliPay_way,order_string)
        logger.info(pay_url)
        return pay_url

    def callback(self,data):

        iData = dict()
        for item in data:
            iData[item] = data[item]

        logger.info("支付宝回调数据=>{}".format(iData))
        sign = iData.pop("sign",None)
        if not self.alipay.verify(iData,sign):
            raise PubErrorCustom("验签失败!")

        if iData.get("trade_status",None) != 'TRADE_SUCCESS':
            raise PubErrorCustom("交易状态异常!")
        #
        # try:
        #     orderObj = Order.objects.select_for_update().get(orderid=iData.get("out_trade_no",""))
        #     if orderObj.status == '1':
        #         logger.info("订单{}已处理".format(orderObj.orderid))
        #         raise PubErrorCustom("订单{}已处理".format(orderObj.orderid))
        # except Order.DoesNotExist:
        #     raise PubErrorCustom("订单不存在!")
        #
        # orderObj.status = '1'
        # orderObj.save()
        #
        # user = Users.objects.select_for_update().get(userid=orderObj.userid)
        #
        # logger.info("用户{}积分余额{}使用积分{}获得积分{}".format(user.mobile,user.jf,orderObj.use_jf,orderObj.get_jf))
        # user.jf -= orderObj.use_jf
        # user.jf += orderObj.get_jf
        # user.save()
        #
        logger.info("支付宝回调订单处理成功!=>{}".format(iData))


