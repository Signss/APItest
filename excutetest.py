import time, os
from libs import contants, utils
from APIGettest import TuBoGetAPI


# time.sleep(10)
# os.remove('json_err_file.txt')

def deal_get():
    # get_test = TuBoGetAPI(contants.DOMAIN)
    # get_test.run()
    json_result = utils.deal_err_file('json_err_file.txt')
    print(json_result)
    request_result = utils.deal_err_file('request_err_result.txt')
    print(request_result)
    response_result = utils.deal_err_file('response_err_file.txt')
    print(response_result)
    lack_result = utils.deal_err_file('lack_response_err_file.txt')
    print(lack_result)


if __name__ == '__main__':
    deal_get()