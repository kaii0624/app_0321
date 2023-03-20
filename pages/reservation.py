import streamlit as st
import pandas as pd
from datetime import date
import os

csv_file = "reservation_data.csv"

def load_data():
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame(columns=["date", "name", "purpose"])

def save_data(data):
    data.to_csv(csv_file, index=False)

def remove_reservation(data, idx):
    if not data.empty:
        data = data.drop(index=idx)
        save_data(data)
    return data

st.set_page_config(page_title="市ヶ谷予約アプリ", layout="wide")
st.title("市ヶ谷予約アプリ")

data = load_data()

# 新規予約
st.subheader("新規予約")
with st.form("add_reservation"):
    new_date = st.date_input("日付を選択", value=date.today())
    new_name = st.text_input("名前を入力", value="")
    new_purpose = st.text_input("用途を入力", value="")
    add_reservation = st.form_submit_button("予約を追加")

    if add_reservation and new_name and new_purpose:
        data = data.append({"date": new_date, "name": new_name, "purpose": new_purpose}, ignore_index=True)
        save_data(data)
        st.experimental_rerun()

# 予約済みスケジュール
st.subheader("予約済みスケジュール")
if not data.empty:
    st.write(data[["date", "name", "purpose"]])

    # 予約の削除
    st.subheader("予約の削除")
    with st.form("remove_reservation"):
        reservation_idx = st.selectbox("削除する予約を選択", options=data.index, format_func=lambda x: f"{data.loc[x, 'date']} - {data.loc[x, 'purpose']} - {data.loc[x, 'name']}")
        remove_reservation_button = st.form_submit_button("予約を削除")

        if remove_reservation_button:
            data = remove_reservation(data, reservation_idx)
            st.experimental_rerun()
else:
    st.write("現在予約はありません。")