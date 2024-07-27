import re


def extract_words_from_dictionary(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    pattern = re.compile(r"【(.*?)】")
    matches = pattern.findall(text)
    cleaned_matches = {re.sub(r"（儿）", "", match) for match in matches}

    return cleaned_matches


def save_to_file(strings_set, output_path):
    with open(output_path, "w", encoding="utf-8") as file:
        for string in strings_set:
            file.write(f"{string}\n")


if __name__ == "__main__":
    file_path = "resource/XDHYCD7th.txt"  # 替换为你的文件路径
    output_path = "output.txt"  # 替换为你的输出文件路径

    extracted_strings = extract_words_from_dictionary(file_path)
    save_to_file(extracted_strings, output_path)
