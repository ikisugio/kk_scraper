from sqlalchemy import create_engine, Table, Column, String, MetaData, UniqueConstraint
from sqlalchemy.exc import IntegrityError
from db.test import url_lists_data


def create_table(engine):
    metadata = MetaData()
    
    # テーブルを作成
    my_table = Table('my_table', metadata,
        Column('jigyosyo_cd', String),
        Column('jigyosyo_name', String),
        Column('jigyosyo_url', String),
        UniqueConstraint('jigyosyo_cd', 'jigyosyo_name', name='uix_1')  # 両方が一緒に重複している場合にエラー
    )

    metadata.create_all(engine)

    return my_table


def hydrate(data_object):
    # データベースへの接続を作成
    engine = create_engine('sqlite:///db/out/kk_jigyosyo.db')

    # テーブル作成（存在しない場合）
    my_table = create_table(engine)
    with engine.begin() as connection:
        try:
            ins = my_table.insert().values(
                jigyosyo_cd=data_object['jigyosyo_cd'],
                jigyosyo_name=data_object['jigyosyo_detail']['jigyosyo_name'],
                jigyosyo_url=data_object['jigyosyo_detail']['jigyosyo_url']
            )
            connection.execute(ins)
        except IntegrityError as e:
            print(f"Error occurred: {e}")


# for i in url_lists_data.test_data:
#     hydrate(i)