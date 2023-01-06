import time
import csv
from os import system
from chemspipy import ChemSpider


if __name__ == '__main__':
    print('CAS查询英文名和SMILES')
    print('By wehnes ver. 1.0')
    try:
        fcode = open('api.txt', 'r')
        api = fcode.read()
        print("获取到api:" + api)
        fp = open('raw.txt', 'r')
        cas = fp.read().splitlines()
    except:
        print("Error: 没有找到文件或读取文件失败，请检查根目录是否存在api.txt和raw.txt")
        system('pause')
    else:
        fcode.close()
        fp.close()
        cs = ChemSpider(api)
        header = ["CAS", "Name", "SMILES"]
        # f = open('cas_' + str(time.time()) + '.csv', 'w+', encoding='utf-8')
        f_cas = open('cas_' + str(time.time()) + '.csv', "w+", encoding='utf-8-sig', newline="")
        writer = csv.writer(f_cas)
        writer.writerow(header)
        for i in cas:
            i = i.strip()
            if i:
                c_quest = cs.filter_name(i)
                c_ids = cs.filter_results(c_quest)
                if c_ids:
                    name = cs.get_compound(c_ids[0]).common_name
                    smiles = cs.get_compound(c_ids[0]).smiles
                    row = [i, name, smiles]
                    print(row)
                    writer.writerow(row)
                else:
                    print('Not Found')
                    row = [i, "0", "0"]
                    writer.writerow(row)
            else:
                print('Not Found')
                row = [i, "0", "0"]
                writer.writerow(row)
        f_cas.close()
        system('pause')
