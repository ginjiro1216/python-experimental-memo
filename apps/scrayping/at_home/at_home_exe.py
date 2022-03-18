import requests, csv, tqdm,os, sys
import bs4
import time
import pandas as pd


headers = [
    '商号', '住所', '電話', '代表者', '免許番号', '主な取り扱い物件'
]


def shop_detail_parser():
    data = []
    data_length = int(sys.argv[2])
    with open(f'at_home/code/{sys.argv[1]}' + '.csv', 'r') as counter:
        counter_reader = csv.reader(counter)
        next(counter_reader)
        list_length = len([row for row in counter_reader])
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

    with open(f'at_home/code/{sys.argv[1]}' + '.csv', 'r', errors='ignore') as r:
        reader = csv.reader(r)
        next(reader)
        bar = tqdm.tqdm(total=data_length)
        bar.set_description(f'{sys.argv[1]}のスクレイピング進行状況')
        counter = 0
        for row in reader:
            if data_length == counter:
                break
            try:
                number = row[1]
            except:
                print('エンコーディングエラー\n'
                      'もう一度実行してください。\n'
                      '取得したデータは保存されます。')
                df = pd.read_csv(f'at_home/code/{sys.argv[1]}' + '.csv', dtype=object)
                droped_df = df.drop([0])
                droped_df.to_csv(f'at_home/code/{sys.argv[1]}' + '.csv', index=False)
                bar.update(1)
                break

            try:
                res = requests.get(
                    f'https://www.athome.co.jp/iphone_api/iphoneApi.php?SERVICE=apKaiinDetailService&KAILINKNO={number}')
            except:
                print('情報を取得するのに失敗しました。\n'
                      'ネットワークが切断していないか確認してください。\n'
                      'スクレイピングが中断されます。')
                number = ''
                while True:
                    str_number = str(number)
                    if not os.path.exists('at_home/' + sys.argv[1] + str_number + '.csv'):
                        with open('at_home/' + sys.argv[1] + str_number + '.csv', 'w') as w:
                            writer = csv.writer(w)
                            writer.writerows([headers])
                            writer.writerows(data)
                        return
                    else:
                        if number == '':
                            number = 1
                        number += 1
                        continue
                print(f'{sys.argv[1]}{str_number}.csvを出力しました。')

            soup = bs4.BeautifulSoup(res.content, "html.parser")
            try:
                syogo = soup.select('SYOGO')[0]
                address = soup.select('SHOZAI')[0]
                phone_number = soup.select('TEL')[0]
                representer = soup.select('DAIHYO_NM')[0]
                menkyo = soup.select('MENKYO_NM')[0]
                bukken = soup.select('TORIATU')[0]
            except:
                bar.update(1)
                df = pd.read_csv(f'at_home/code/{sys.argv[1]}' + '.csv', dtype=object)
                droped_df = df.drop([0])
                droped_df.to_csv(f'at_home/code/{sys.argv[1]}' + '.csv', index=False)
                time.sleep(3)
                continue
            row = [syogo.string, address.string, phone_number.string, representer.string, menkyo.string, bukken.string]
            bar.update(1)
            data.append(row)
            df = pd.read_csv(f'at_home/code/{sys.argv[1]}' + '.csv', dtype=object)
            droped_df = df.drop([0])
            droped_df.to_csv(f'at_home/code/{sys.argv[1]}' + '.csv', index=False)
            time.sleep(2)
            counter += 1
    number = ''
    while True:
        str_number = str(number)
        if not os.path.exists('at_home/' + sys.argv[1] + str_number + '.csv'):
            with open('at_home/' + sys.argv[1] + str_number + '.csv', 'w') as w:
                writer = csv.writer(w)
                writer.writerows([headers])
                writer.writerows(data)
            break
        else:
            if number == '':
                number = 1
            number += 1
            continue
    print(f'{sys.argv[1]}{str_number}.csvを出力しました。')


if __name__ == '__main__':
    shop_detail_parser()