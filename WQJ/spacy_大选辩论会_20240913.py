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

    topic_name = 'president_debate'
    # 定义输入和输出目录
    input_dir = r'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate'
    output_dir = rf'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate\Topic_Keywords_Identification\spacy_{topic_name}'
    #大选辩论会相关
    terms = [
        "Presidential", "President", "Presidents", "Maine Legislature", "Legislature", "Legislatures", "Legislative",
        "Legislations", "Legislation", "Legislate", "Legislates", "Legislated", "Legislating", "Voting", "Vote",
        "Votes",
        "Voted", "Votor", "Votors", "Voter", "Voters", "Elector", "Electors", "Electorate", "Electorates",
        "Electorating", "Electorated", "Election", "Elections", "Elect", "Elects", "Electing", "Elected", "Electoral",
        "Election Night", "Presidential election", "Constituency", "Janet Mills", "Pollsters", "Pollster",
        "Media polling",
        "Phony polls", "Fake polls", "Polls", "Poll", "Polled", "Polling", "Pollings", "Vote", "Votes", "Banknote",
        "Banknotes", "Polling Station", "Polling Stations", "Ballot", "Ballots", "Tickets", "Ticket", "Bill", "Bills",
        "Billing", "Billed", "Election", "Elections", "Electoral Vote", "Electoral Votes", "Electoral", "Immigration",
        "Immigrations", "Immigrate", "Immigrating", "Immigrates", "Immigrated", "Virus", "Debate", "Debates",
        "Moderator", "Moderators", "Candidate", "Candidates", "Quadrennial", "Senator", "Senators", "Senate", "Senates",
        "Senating", "Senated", "Community", "Communities", "Democracy", "Democratic", "Democrat", "Democrats",
        "Republican", "Republicans", "Republic", "Party", "Parties", "Government", "Governments", "Vice",
        "Vice President", "President", "Presidents", "Presidential", "Wall Street", "Latino", "African American",
        "Asian American", "Hurricane", "First Lady", "Karen Pence", "Border Wall", "Middle East", "ISIS", "Iran",
        "Afghanistan", "Iran Nuclear Deal", "Embassy", "Embassies", "Jerusalem", "Israeli", "Qasem Soleimani",
        "Manufacturing jobs", "Auto Industry", "Iraq War", "Vaccine", "Socialism", "Congresswoman", "5G", "Borders",
        "Taxes", "Opportunity Zones", "Patriotic education", "Free Speech", "Economy", "Economies", "Healthcare",
        "Climate Change", "Education", "Justice", "Equality", "Reform", "Reforming", "Reformed", "Reforms", "Policy",
        "Policies", "Security", "Securities", "Innovation", "Innovations", "Platform", "Platforms", "Policy",
        "Policies",
        "Discussion", "Discussions", "Question", "Questions", "Answer", "Answers", "Argument", "Arguments", "Issue",
        "Issues", "Result", "Results", "Turnout", "Turnouts", "Winner", "Winners", "Loser", "Losers", "Campaign",
        "Campaigns", "Advocate", "Advocating", "Law", "Discrimination", "LGBTQ+", "Feminism", "Authenticity", "LGBT+",
        "Far-left", "Donald Trump", "Joe Biden", "Delaware", "Florida", "Kamala Harris", "Mike Pence", "Biden", "Trump",
        "Pence", "Harris", "Presidential debate", "Vice presidential", "Vice president", "First debate",
        "Second debate",
        "Third debate", "Moderator Debate", "Fact-checking", "Opening statement", "Closing statement",
        "Debate schedule",
        "Delegates", "George Floyd", "Supreme Court", "Public health", "Ruth Bader Ginsburg", "Amy Coney Barrett",
        "Affordable Care Act", "Mail-in", "Mail-ins", "Post", "Posts", "Posted", "Posting", "Swing states", "States",
        "State", "Vote counting", "Voter fraud", "Fraud", "Frauds", "Frauding", "Fraudulent", "Fraudulently",
        "Fraudulency", "Fraudulence", "Fraudulences", "Defrauding", "Defraud", "Defrauds", "Defrauded", "Forgery",
        "Forgeries", "Deceit", "Deceiting", "Deceits", "Deceited", "Deceitful", "Deceitfully", "Scams", "Scam",
        "Scaming", "Scamed", "Deception", "Deceptions", "Decept", "Decepts", "Decepting", "Deceptive", "Deceptively",
        "Decepted", "Fob", "Fobs", "Fobing", "Fobbed", "Gudgeon", "Gudgeons", "Fakement", "Fakements", "Fake", "Fakes",
        "Fakeing", "Faked", "Deceive", "Deceives", "Deceiving", "Deceived", "Misrepresentation", "Misrepresentations",
        "Misrepresent", "Misrepresents", "Misrepresenting", "Misrepresented", "Theft", "Thefts", "Cheat", "Cheats",
        "Cheating", "Cheated", "Finagle", "Finagles", "Finagling", "Finagled", "Swindle", "Swindling", "Swindles",
        "Swindling", "Crime", "Crimes", "Law", "Coup", "Coups", "Coup d'état", "Congress", "Department of Justice",
        "Corrupt", "Corrupted", "Corruption", "Corruptions", "Electoral College", "Fight like hell", "Capitol",
        "Inauguration", "Primary election", "Nominate", "Nominating", "Nominates", "Nominated", "Propose", "Proposed",
        "Proposes", "Proposing", "United States House of Representatives", "Representatives", "Representative", "Agent",
        "Agents", "Official", "Officers", "Officer", "Spokesman", "Spokesmen", "Speech", "speeches", "United States",
        "US", "U.S", "House of Representatives"
    ]

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 定义部分函数，固定部分参数
    worker = partial(process_file, terms=terms, input_dir=input_dir, output_dir=output_dir)

    # 顺序处理，不使用多线程
    for date in dates:
        worker(date)

    print("所有文件处理完成。")