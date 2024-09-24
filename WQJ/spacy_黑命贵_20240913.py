import spacy
from spacy.matcher import PhraseMatcher
import pandas as pd
import os
from functools import partial
from tqdm import tqdm










def initialize_matcher(nlp, terms):
    """
    初始化 PhraseMatcher，添加匹配模式。
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")  # 忽略大小写
    unique_terms = list(set(terms))  # 去除重复项
    patterns = [nlp.make_doc(text) for text in unique_terms]
    matcher.add("TechTerms", patterns)
    return matcher


def process_file(date, terms, input_dir, output_dir):
    """
    处理单个日期对应的CSV文件，进行关键词匹配并保存结果。
    """
    # 加载spaCy模型
    try:
        nlp = spacy.load("en_core_web_lg")
    except Exception as e:
        print(f"Error loading spaCy model: {e}")
        return

    # 初始化 PhraseMatcher
    matcher = initialize_matcher(nlp, terms)

    # 定义文件路径
    orign_filepath = os.path.join(input_dir, f'combined_original_fulltext_and_tweet_id_{date}_with_languages.csv')
    result_filepath = os.path.join(output_dir, f'fulltext_and_tweet_id_with_economy_{date}.csv')

    print(f'正在处理文件： {orign_filepath}')

    # 读取原始CSV文件
    try:
        df = pd.read_csv(orign_filepath, encoding='utf-8')
    except FileNotFoundError:
        print(f"文件未找到： {orign_filepath}")
        return
    except Exception as e:
        print(f"读取文件 {orign_filepath} 时出错： {e}")
        return
    # 定义匹配函数
    def match_terms(text):
        doc = nlp(text)
        matches = matcher(doc)
        matched = set()
        for match_id, start, end in matches:
            span = doc[start:end]
            matched.add(span.text)
        return '/'.join(matched) if matched else ''
    # 初始化计数器和存储匹配结果的列表
    processed_count = 0
    matched_phrases = []

    # 在循环前初始化 tqdm
    for text in tqdm(df['retweeted_origin_full_text'].astype(str), desc="Processing rows"):
        matched = match_terms(text)
        matched_phrases.append(matched)
        processed_count += 1
        if processed_count % 10000 == 0:
            print(f"Processed {processed_count} rows.")

    # 将匹配结果添加到DataFrame
    df['Matched Phrases'] = matched_phrases

    # 过滤出有匹配结果的行
    df_matched = df[df['Matched Phrases'] != '']

    # 保存结果到新的CSV文件
    try:
        df_matched.to_csv(result_filepath, index=False, encoding='utf-8')
        print(f"结果已保存到： {result_filepath}")
    except Exception as e:
        print(f"写入文件 {result_filepath} 时出错： {e}")

    print(f"处理完成，日期： {date}，总行数： {len(df)}")






if __name__ == "__main__":
    """
        主函数，设置参数并启动多进程处理。
        """
    # 定义日期列表
    dates = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
             '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']

    topic_name = 'blackLivesMatter'
    # 定义输入和输出目录
    input_dir = r'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate'
    output_dir = rf'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate\Topic_Keywords_Identification\spacy_{topic_name}'
    #blackLivesMatter相关
    terms = [
        "Black Life", "Black-Life", "Blacklife", "BLM", "Black Lives", "Lives", "Life", "Black-Lives", "Blacklives",
        "Black Lives Matter", "Racial", "Racism", "Discrimination", "Discriminations", "Equality", "Justice",
        "Police Brutality", "Brutality", "Violence", "Force", "Police", "Polices", "Law Enforcement",
        "Police Reform", "Defund the Police", "Protests", "Protest", "Protesting", "Protested", "Demonstrations",
        "Civil Disobedience", "Disobedience", "Disobediences", "Riots", "Riot", "Marches", "Sit-ins", "Vigil",
        "Vigils", "Vigilance", "vigilant", "#BlackLivesMatter", "#BLM", "#SayTheirNames", "#JusticeForGeorgeFloyd",
        "#NoJusticeNoPeace", "#ICantBreathe", "#HandsUpDontShoot", "#M4BL", "#JusticeForBreonnaTaylor",
        "#JusticeForAhmaudArbery", "#JusticeForElijahMcClain", "#JusticeForTamirRice", "#JusticeForMichaelBrown",
        "#JusticeForPhilandoCastile", "#EndPoliceBrutality", "#DefundThePolice", "#AbolishThePolice",
        "#PoliceReform", "#PoliceAccountability", "#StopKillingUs", "#RacialJustice", "#EndRacism", "#FightRacism",
        "#SystemicRacism", "#InstitutionalRacism", "#AntiRacism", "#EducateYourself", "#BlackOutTuesday",
        "#BlackLivesMatterProtests", "#SolidarityWithBLM", "#StandWithBLM", "#ProtestForChange", "#WeStandWithYou",
        "#WhiteAllies", "#AlliesForBlackLives", "#SupportBlackLives", "#Allyship", "#Solidarity", "#RestInPower",
        "#SayHerName", "#SayHisName", "#RememberTheirNames", "#HonorTheirMemory", "#CriminalJusticeReform",
        "#CivilRights", "#BodyCamsForCops", "#ReformThePolice", "#BlackJoy", "#BlackHealing", "#BlackLove",
        "#BlackExcellence", "#BlackPride", "#BLMProtest", "#BLM2024", "#BlackLivesMatterMovement", "GeorgeFloyd",
        "George Floyd", "Breonna Taylor", "BreonnaTaylor", "Ahmaud Arbery", "AhmaudArbery", "Eric Garner",
        "EricGarner", "Tamir Rice", "TamirRice", "Michael Brown", "MichaelBrown", "Coalition Building", "Coalition",
        "Police Reform Bills", "Reform", "Reforms", "Reformed", "Reforming", "Reformation", "Reformations",
        "Criminal", "Crime", "Crimes", "Crimer", "Crimers", "Justice", "Justices", "Court", "Courts",
        "Criminal Justice Reform", "Civil Rights", "Rights", "Legislation", "Legislating", "Legislate",
        "Legislated", "Legislates", "Legislations", "Body Cameras", "Force Policies", "White Supremacy",
        "Backlash", "Counter-Protests", "Movement", "Movements", "Matter", "Matters", "Inequity", "Inequities",
        "equity", "equities", "NAACP", "National Association for the Advancement of Colored People", "ACLU",
        "American Civil Liberties Union", "Color of Change", "Campaign Zero", "Movement for Black Lives", "M4BL",
        "Incarceration", "Incarcerations", "Incarcer", "Incarcers", "Incarcerate", "Incarcerates", "Incarcerated",
        "Incarcerating", "Breath", "Breathe", "Breathy", "Breathes", "Breathing", "Breathed"
    ]

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 定义部分函数，固定部分参数
    worker = partial(process_file, terms=terms, input_dir=input_dir, output_dir=output_dir)

    # 顺序处理，不使用多线程
    for date in dates:
        worker(date)

    print("所有文件处理完成。")