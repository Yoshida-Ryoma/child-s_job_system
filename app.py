import streamlit as st
import requests

# サンプルのユーザー情報
user__id__date = ['24c1001000', '24c1001001']
user__pass__date = ['yoshida_0822', 'childs0505']

# ユーザーIDとパスワードを組み合わせたものを作成
user1 = user__id__date[0] + user__pass__date[0]
user2 = user__id__date[1] + user__pass__date[1]

# notif TOKEN
TOKEN="Z0mewR5mIJMhufOKyTMYsH4Vm2srOYygGKwn64ZBTt3"

# ユーザーデータリスト
user__date = [user1, user2]

# ログイン状態とページ情報の初期化
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"  # 初期ページはログインページ
if "job_description" not in st.session_state:
    st.session_state.job_description = ""  # 依頼内容の初期化
if "need_ability" not in st.session_state:
    st.session_state.need_ability = ""  # 必要技能の初期化
if "your_name" not in st.session_state:  # 修正
    st.session_state.your_name = ""  # 名前の初期化

def login_page():
    """ログインページのUI"""
    st.title("ログインページ")
    input__id = st.text_input('IDを入力してください')
    input__pass = st.text_input('Passwordを入力してください', type="password")

    if st.button('ログイン'):
        input__user = input__id + input__pass
        if input__user in user__date:
            st.session_state.logged_in = True
            st.session_state.page = "main"  # メインページに切り替え
        else:
            st.error("ログインに失敗しました。再度入力してください")

def main_page():
    """メインページのUI"""
    st.title('仕事内容送信')
    
    # テキストエリアとテキスト入力の更新
    st.session_state.job_description = st.text_area(
        "依頼内容を記入してください",
        value=st.session_state.job_description,
        key="job_description_key"
    )
    st.session_state.need_ability = st.text_input(
        "欲しい能力等を書いてください(もし必要ないならなしと書いてください)",
        value=st.session_state.need_ability,
        key="need_ability_key"
    )
    st.session_state.your_name = st.text_input(
        "あなたの名前を入力してください",
        value=st.session_state.your_name,
        key="your_name_key"
    )
    
    if st.button("依頼を送信"):
        if st.session_state.job_description.strip() and st.session_state.need_ability.strip() and st.session_state.your_name.strip():
            st.success("依頼が送信されました。ありがとうございます！")
            api_url = 'https://notify-api.line.me/api/notify'
            job_description="仕事内容:"
            need_ability="必要な技術:"
            your_name="依頼者:"


            send_contents =f"\n{job_description}\n{st.session_state.job_description}\n{need_ability}\n{st.session_state.need_ability}\n{your_name}\n{st.session_state.your_name}"
            TOKEN_dic = {'Authorization': 'Bearer ' + TOKEN}
            send_dic = {'message': send_contents}
                    
            # メッセージ送信
            requests.post(api_url, headers=TOKEN_dic, data=send_dic)

            # テキストボックスを空にする
            st.session_state.job_description = ""
            st.session_state.need_ability = ""
            st.session_state.your_name = ""
        else:
            st.error("全ての項目を入力してください。")
    
    if st.button("ログアウト"):
        st.session_state.logged_in = False
        st.session_state.page = "login"  # ログインページに戻る

# ページごとの処理を分岐
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "main":
    main_page()
