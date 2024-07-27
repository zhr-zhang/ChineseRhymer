import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from time import sleep
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

root_url = "https://xinhuazidian.cn"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}

def get_untoned_pinyin_list(session) -> list[str]:
    response = session.get(root_url + "/pinyin", headers=headers)
    response.encoding = "utf-8"  # 确保响应内容使用 UTF-8 编码
    soup = BeautifulSoup(response.text, "html.parser")
    ul_tag = soup.find("ul", class_="lnk-sqr no-width")
    untoned_pinyin_list = []
    if ul_tag:
        for li in ul_tag.find_all("li"):
            a_tag = li.find("a")
            if a_tag and "/pinyin/" in a_tag["href"]:
                untoned_pinyin_list.append(a_tag.get_text())
    return untoned_pinyin_list

def get_characters_by_untoned_pinyin(untoned_pinyin: str, session):
    response = session.get(root_url + "/pinyin/" + untoned_pinyin, headers=headers)
    response.encoding = "utf-8"  # 确保响应内容使用 UTF-8 编码
    soup = BeautifulSoup(response.text, "html.parser")
    ul_tags = soup.find_all("ul", class_="lnk-sqr")

    # 提取汉字和链接并组成字典，只提取链接中含有 /zi/ 的内容
    hanzi_dict = {}
    for ul_tag in ul_tags:
        for li in ul_tag.find_all("li"):
            a_tag = li.find("a")
            if a_tag and "/zi/" in a_tag["href"] and "/pinyin/" not in a_tag["href"]:
                hanzi = a_tag.get_text()
                link = a_tag["href"]
                hanzi_dict[hanzi] = link

    return hanzi_dict

def get_character_info(character_link: str, session):
    response = session.get(root_url + character_link, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    info_section = soup.find("div", class_="info")
    data = {}
    for attr in info_section.find_all("div", class_="attr"):
        attr_name = attr.find("span", class_="attr_name").text
        attr_value = attr.find_all("span")[1].text.strip()
        if attr_name == "反义字":
            attr_value = attr_value.replace("\n", ",")
        data[attr_name] = attr_value
    return data

if __name__ == "__main__":
    session = requests.Session()
    retry = Retry(
        total=5,  # 总共重试5次
        backoff_factor=1,  # 重试等待时间指数增长，1秒, 2秒, 4秒...
        status_forcelist=[500, 502, 503, 504]  # 针对这些状态码进行重试
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    untoned_pinyin_list = get_untoned_pinyin_list(session)
    characters_dict = {}
    for untoned_pinyin in tqdm(untoned_pinyin_list, desc="Processing untoned pinyins"):
        try:
            characters_dict.update(get_characters_by_untoned_pinyin(untoned_pinyin, session))
        except requests.exceptions.RequestException as e:
            print(f"Error processing {untoned_pinyin}: {e}")
        sleep(random.uniform(2, 7))  # 增加随机等待时间范围
    
    with open("resource/中.json", "w", encoding="utf-8") as f:
        for character, link in tqdm(characters_dict.items(), desc="Processing characters"):
            try:
                character_info = get_character_info(link, session)
                json.dump({character: character_info}, f, ensure_ascii=False, indent=4)
            except requests.exceptions.RequestException as e:
                print(f"Error processing {character}: {e}")
            sleep(random.uniform(2, 7))  # 增加随机等待时间范围
