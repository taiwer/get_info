import time

import requests
import ast
import pandas as pd



class Update_info:
    def __init__(self):
        # 执业机构 登记日期 登记类别 登记状态
        self.practice_organization = ""
        self.register_date = ""
        self.register_type = ""
        self.register_status = ""


class Person:
    def __init__(self):
        # 姓名  | 性别 | 登记编号 | 代理期间 | 执业地域 | 服务营业部 | 执业机构 | 登记日期 | 登记类别 | 登记状态
        self.name = ""
        self.sex = ""
        self.register_num = ""
        self.agent_period = ""
        self.practice_area = ""
        self.service_department = ""
        self.update_info = []


def get_uuid(num_page):
    url = "https://gs.sac.net.cn/publicity/getPersonList"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "Hm_lvt_c1ca07c04e2a25c0b65c1c140e138eda=1726241201; Hm_lpvt_c1ca07c04e2a25c0b65c1c140e138eda=1726241201; HMACCOUNT=096C55770630C047",
        "origin": "https://gs.sac.net.cn",
        "priority": "u=1, i",
        "referer": "https://gs.sac.net.cn/pages/registration/sac-publicity-finish.html?aoiId=1999088&ptiId=3",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }

    data = {
        "aoiId": "1999088",
        "ptiId": "3",
        "_search": "false",
        "nd": "1726241753753",
        "pageSize": "100",
        "pageNum": f"{num_page}",
        "orderBy": "id",
        "order": "desc"
    }

    response = requests.post(url, headers=headers, data=data)

    res_json = response.json()

    list = res_json['data']['data']['list']

    uuids = []

    for i in list:
        uuids.append(i['uuid'])

    return uuids


def get_sub_info(uuid_in):
    url = "https://gs.sac.net.cn/publicity/getPersonDetail"

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5",
        "content-type": "application/x-www-form-urlencoded",
        "cookie": "Hm_lvt_c1ca07c04e2a25c0b65c1c140e138eda=1726241201,1726247490,1726247790; Hm_lpvt_c1ca07c04e2a25c0b65c1c140e138eda=1726247790; HMACCOUNT=35AE5080F5206BDB",
        "origin": "https://gs.sac.net.cn",
        "priority": "u=0, i",
        "referer": f"https://gs.sac.net.cn/pages/registration/sac-other-finish-person.html?r2SS_IFjjk={uuid_in}",
        "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    data = {
        "uuid": f"{uuid_in}"
    }

    response = requests.post(url, headers=headers, data=data)

    res_json = response.json()

    data_json = res_json['data']['data']

    person = Person()
    person.name = data_json['name']
    person.sex = data_json['gender']
    person.register_num = data_json['certifNo']
    person.agent_period = '自： ' + data_json['agtStartDate'] + " 至 " + data_json['agtEndDate']
    person.practice_area = data_json['pracAreaName']
    person.service_department = data_json['servBrnName']

    # update_info = Update_info()
    reg_history_ls = ast.literal_eval(data_json['regHistory'])
    for i in reg_history_ls:
        update_info = Update_info()
        update_info.practice_organization = i['org_name']
        update_info.register_date = i['get_date']
        update_info.register_type = i['reg_type']
        update_info.register_status = i['status']
        person.update_info.append(update_info)

    return person


if __name__ == "__main__":
    uuid_all = []
    for i in range(1, 12):
        uuid_all.extend(get_uuid(i))

    # 保存uuid_all 到本地
    with open('uuid_all.txt', 'w') as f:
        for i in uuid_all:
            f.write(i + '\n')

    tt = get_sub_info(1614059640944711821)

    # 获取 res.txt 的行数
    with open('res.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line_th = len(lines)
    # 循环uuid获取子页面信息
    personals = []

    with open('uuid_new.txt', 'r') as f:
        uuid_all = f.readlines()
    for i, j in enumerate(uuid_all[line_th:]):
        time.sleep(5)
        # 去掉换行符
        j = j.strip()
        person_details = get_sub_info(j)
        print(f"第{i}个人员信息获取完成")
        personals.append(person_details)

        for z in person_details.update_info:
            tmp = [person_details.name, person_details.sex, person_details.register_num, person_details.agent_period, person_details.practice_area, person_details.service_department,
                             z.practice_organization, z.register_date, z.register_type, z.register_status]
            # 保存到txt
            with open('res.txt', 'a', encoding='utf-8') as f:
                for t in tmp:
                    f.write(str(t)+'\t')
                f.write('\n')

    # 转为list
    res_list = []
    for i in personals:
        for j in i.update_info:
            res_list.append([i.name, i.sex, i.register_num, i.agent_period, i.practice_area, i.service_department,
                             j.practice_organization, j.register_date, j.register_type, j.register_status])



    df = pd.DataFrame(res_list,
                      columns=['姓名', '性别', '登记编号', '代理期间', '执业地域', '服务营业部', '执业机构', '登记日期',
                               '登记类别', '登记状态'])
    df.to_excel('res.xlsx', index=False)
