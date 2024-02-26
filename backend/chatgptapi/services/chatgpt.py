# bizlogic
from logging.handlers import TimedRotatingFileHandler
from django.conf import settings
from googletrans import Translator
import openai
import json
import logging
from chatgptapi import LOG_FILE_PATH

openai.api_key = settings.API_KEY
# 最大桁数
MAX_LEN = 50

translator = Translator()

# ログファイルの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# 日別にログファイルを作成し、過去10日分までログファイルを保持する
handler = TimedRotatingFileHandler(LOG_FILE_PATH, when='D', interval=1, backupCount=10)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False
# ログにはタイムスタンプ及び、ファイル名、行番号、ログレベル、メッセージを出力する
formatter = logging.Formatter('%(asctime)s %(name)s:%(lineno)d [%(levelname)s]: %(message)s')
handler.setFormatter(formatter)

def createPrompt(request):
    logger.debug("createPrompt start")

    # リクエストデータ取得
    request_data = request.data
    prompt = request_data["prompt"]
    logger.debug("prompt:" + json.dumps(prompt))

    # 作りたいアプリ概要
    app_over_view = prompt["appOverview"]
    # DB使用有無
    use_database = prompt["useDatabase"]
    # クラウド使用有無
    use_cloud = prompt["useCloud"]

    # 作りたいアプリ概要がない場合、処理終了
    if not app_over_view:
        logger.warning("作りたいアプリの概要 入力無し")
        return ""
    # 桁数チェック
    if isMaxLen(app_over_view, MAX_LEN):
        logger.warning("桁数上限エラー app_over_view:" + app_over_view)
        return "max_len_error"

    # JSONファイルの読み込み及び取得
    # 言語
    with open('./json/programmingLanguage.json', 'r', encoding='utf-8') as programming_language_open:
        programming_language_json = json.load(programming_language_open)
    programming_language = getPrompt(programming_language_json, "lang", int(prompt["programmingLanguage"]))
    if programming_language == "":
        return "存在しない言語です。入力内容を確認してください。"

    # プラットフォーム
    with open('./json/platform.json', 'r', encoding='utf-8') as platform_open:
        platform_json = json.load(platform_open)
    platform = getPrompt(platform_json, "platform", int(prompt["platform"]))
    if platform == "":
        return "存在しないプラットフォームです。入力内容を確認してください。"
    
    # system_prompt
    system_prompt1 = " 「作りたいアプリの概要：」で指定された内容を「プラットフォーム：」と「プログラム言語：」に指定された条件で構築する際、お勧めのフレームワーク名を最大３つまで提案してください。\n"
    system_prompt2 = "また、提案された各フレームワークの「開発環境」を簡潔に教えてください。\n"
    system_prompt3 = "「DB使用有無：」が「有り」の場合、「DB使用」を考慮したライブラリを、「クラウド使用有無：」が「有り」となっていの場合は「クラウド使用」を考慮したライブラリを紹介してください。\n"
    system_prompt_template = "回答は＜テンプレート＞の内容に沿って返却してください。\n ＜テンプレート＞ \n フレームワーク名： \n  開発環境： \n  ライブラリ： \n"
    system_prompt_ehd = "それ以外の回答はしないでください。\n 「作りたいアプリの概要：」で回答できない質問を指定された場合は、「アプリが不明です。」と返答してください。"
    system_prompt = system_prompt1 + system_prompt2 + system_prompt3 + system_prompt_template + system_prompt_ehd
    logger.debug("system_prompt:\n" + system_prompt)
    # user_prompt
    prompt_app_overview = "作りたいアプリの概要：" + app_over_view + "\n"
    prompt_programming_language = "プログラム言語：" + programming_language + "\n"
    prompt_platform = "プラットフォーム：" + platform + "\n"
    prompt_use_database = "DB使用有無：有り" if use_database == "true" else ""
    prompt_use_cloud = "クラウド使用有無：有り" if use_cloud == "true" else ""
    prompt = prompt_app_overview + prompt_programming_language + prompt_platform + prompt_use_database + prompt_use_cloud
    logger.debug("prompt:\n" + prompt)

    # 質問を投げる
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": translator.translate(system_prompt, dest='en').text
            },
            {
                "role": "user",
                "content": translator.translate(prompt, dest='en').text
            },
        ],
        n           = 1,                # 返答数
        temperature = 0,                # 出力する単語のランダム性（0から2の範囲） 0であれば毎回返答内容固定
    )
    logger.debug("発行トークン数：" + json.dumps(res['usage']))
    logger.debug("createPrompt end")
    # 日本語に翻訳して返却
    return translator.translate(res["choices"][0]["message"]["content"], dest='ja').text;

# 桁数チェック
def isMaxLen(element, max_len):
    return len(element) > max_len

# prompt取得
def getPrompt(json, element_str, id):
    # 指定されたIDの要素を取得
    element_list = json.get(element_str)
    found_element = None
    element_id = id
    for element in element_list:
        if element.get("id") == element_id:
            found_element = element
            break
    # IDに対応するpromptを取得
    if found_element:
        return found_element.get("prompt")
    else:
        return ""


# 言語取得
def get_programming_language():
    # 言語
    programming_language_open = open('./json/programmingLanguage.json', 'r')
    programming_language_json = json.load(programming_language_open)["lang"]
    return str(programming_language_json)


# プラットフォーム取得
def get_platform():
    # プラットフォーム
    platform_open = open('./json/platform.json', 'r')
    platform_json = json.load(platform_open)["platform"]
    return str(platform_json)
