import time, csv, tqdm
import sys, os
import bs4, requests
import pandas as pd


headers = [
    '商号', '住所', '電話', '代表者', '免許番号', '主な取り扱い物件', '交通'
]


def shop_detail_parser():
    with open(f'hatosite/code/{sys.argv[1]}' + '.csv', 'r') as counter:
        counter_reader = csv.reader(counter)
        next(counter_reader)
        list_length = len([row for row in counter_reader])
    data_length = int(sys.argv[2])


    if data_length > 300:
        print('一度に実行できるのは300件までです。')
        print('取得件数を300件に切り替えて実行します。')
        data_length = 300
        time.sleep(3)

    if data_length > list_length:
        print('取得したい件数が残りの件数を上回っています。\n'
              f'残り件数は{list_length}です。\n'
              f'取得件数を{list_length}に切り替えて取得を行います。')
        data_length = list_length
        time.sleep(3)

    csv_data = []
    parserd_data_list = []
    bar = tqdm.tqdm(total=data_length)
    bar.set_description(f'{sys.argv[1]}のスクレイピング進行状況')
    with open(f'hatosite/code/{sys.argv[1]}' + '.csv', 'r', errors='ignore') as r:
        reader = csv.reader(r)
        next(reader)
        counter = 0
        for row in reader:
            if data_length == counter:
                break
            try:
                number = row[1]
            except:
                df = pd.read_csv(f'hatosite/code/{sys.argv[1]}' + '.csv', dtype=object)
                droped_df = df.drop([0])
                droped_df.to_csv(f'hatosite/code/{sys.argv[1]}' + '.csv', index=False)
                print('\nエンコーディングエラー\n'
                      'もう一度実行してください。\n'
                      '取得したデータは保存されます。')
                bar.update(1)
                break
            try:
                res = requests.get(
                    f'https://www.hatomarksite.com/search/zentaku/agent/{number}')
            except:
                print('情報を取得するのに失敗しました。\n'
                      'ネットワークが切断していないか確認してください。\n'
                      'スクレイピングを中断します。。')
                number = ''
                while True:
                    str_number = str(number)
                    if not os.path.exists('hatosite/' + sys.argv[1] + str_number + '.csv'):
                        with open('hatosite/' + sys.argv[1] + str_number + '.csv', 'w') as w:
                            writer = csv.writer(w)
                            writer.writerows([headers])
                            writer.writerows(csv_data)
                        return
                    else:
                        if number == '':
                            number = 1
                        number += 1
                        continue
            soup = bs4.BeautifulSoup(res.content, "html.parser")
            data_list = soup.find_all('td')

            for i in data_list:
                parserd_data_list.append(i.get_text())
            try:
                syogo = parserd_data_list[0]
                address = parserd_data_list[1]
                phone_number = parserd_data_list[2]
                koutuu = parserd_data_list[3]
                representer = parserd_data_list[6]
                menkyo = parserd_data_list[8]
                bukken = parserd_data_list[9]
            except:
                counter += 1
                df = pd.read_csv(f'hatosite/code/{sys.argv[1]}' + '.csv', dtype=object)
                droped_df = df.drop([0])
                droped_df.to_csv(f'hatosite/code/{sys.argv[1]}' + '.csv', index=False)
                bar.update(1)
                continue
            parserd_data_list = []
            row = [syogo, address, phone_number, representer, menkyo, bukken, koutuu]
            csv_data.append(row)
            bar.update(1)
            df = pd.read_csv(f'hatosite/code/{sys.argv[1]}' + '.csv', dtype=object)
            droped_df = df.drop([0])
            droped_df.to_csv(f'hatosite/code/{sys.argv[1]}' + '.csv', index=False)
            counter += 1
            time.sleep(2)
    number = ''
    while True:
        str_number = str(number)
        if not os.path.exists('hatosite/' + sys.argv[1] + str_number + '.csv'):
            with open('hatosite/' + sys.argv[1] + str_number + '.csv', 'w') as w:
                writer = csv.writer(w)
                writer.writerows([headers])
                writer.writerows(csv_data)
            break
        else:
            if number == '':
                number = 1
            number += 1
            continue
    print(f'{sys.argv[1]}{str_number}.csvを出力しました。')


if __name__ == '__main__':
    shop_detail_parser()
