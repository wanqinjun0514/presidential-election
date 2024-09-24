import spacy
from spacy.matcher import PhraseMatcher
import csv
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import os
from nltk.stem import WordNetLemmatizer
from multiprocessing import Pool, cpu_count
from functools import partial
from tqdm import tqdm

def spacy_too_slow():
    terms = [  # 经济指标
        "Investment", "Invest", "Investing", "Invests", "Invested", "Investing", "Investor", "Investors", "GDP", "GDPs",
        "GDP growth", "Gross Domestic Product", "GDP increases",
        "Unemployment", "Employing", "Unemploy", "employ", "employer", "employee", "Unemployment rate", "Job", "jobs",
        "Jobless rate", "Jobless",
        "Manufacturing PMI", "Purchasing Managers' Index", "PMI", "Housing starts", "House", "Houses",
        "Consumer", "Consuming", "Consumed", "Consumers", "consumption", "consumptions", "Consumer spending",
        "Consumer expenditure", "Personal consumption expenditures",
        "Personal spending",

        # 政策措施
        "Quantitative Easing", "QE", "Emergency rate cut", "Fiscal stimulus",
        "Stimulus package", "Relief bill", "bill", "bills", "Relief package", "Loan support",
        "Unlimited QE", "Unlimited Quantitative Easing",

        # 行业影响
        "industry", "industries", "Tourism industry", "Tourism sector", "Agriculture", "Farming", "Manufacturing",
        "Real estate", "Property market", "market", "markets", "marketing", "marketed", "Service industry",
        "Service sector", "sectors",

        # 经济事件
        "Economic", "COVID-19 pandemic", "COVID-19", "Coronavirus pandemic", "Economic recession",
        "Economic downturn", "Stock market volatility", "volatility", "Market fluctuations",
        "Lockdown measures", "Lockdowns", "Vaccine development", "Vaccine rollout",
        "Economic recovery", "Recovery",

        # 经济数据
        "Gross Domestic Product", "GDP", "Federal funds rate", "Fed rate",
        "Interest rate", "Inflation rate", "Trade balance", "Fiscal deficit",
        "Budget deficit",

        # 经济预测
        "Economic outlook", "Growth forecast", "Market expectations",

        # 经济主体
        "Federal Reserve", "Fed", "Department of the Treasury", "Treasury",
        "Enterprises", "Companies", "Company", "Corporations", "Consumers", "Investors",
        "commerce", "business", "trade", "trades", "trading", "traded", "funds", "fund", "funding", "funded",

        # 经济行为
        "shopping", "Online shopping", "E-commerce", "Remote work", "work", "works", "working", "worked",
        "Telecommuting",
        "Work from home", "Shelter-in-place", "Stay-at-home orders", "Investment decision",
        "Investment choices",

        # 经济术语
        "Economic stimulus", "Stimulus", "Economic contraction", "Recession",
        "Negative interest rates", "Monetary policy", "Fiscal policy",

        # 主要指数
        "Dow Jones Industrial Average", "DJIA", "S&P 500",
        "Standard & Poor's 500", "NASDAQ Composite", "Russell 2000",

        # 交易所
        "New York Stock Exchange", "NYSE", "NASDAQ Stock Market",
        "NASDAQ", "American Stock Exchange", "AMEX",

        # 交易时间
        "Opening Bell", "Open", "Closing Bell", "Close",
        "Pre-market trading", "After-hours trading",

        # 交易行为
        "Buy", "Buys", "Buying", "Bought", "Purchase", "Purchases", "Purchasing", "Purchased", "Sell", "Sells", "sold",
        "Selling", "Seller", "Bullish", "Bull market",
        "Bearish", "Bear market", "Stop-loss",

        # 市场参与者
        "Investors", "Traders", "Brokers", "Analysts", "Fund Managers",

        # 金融产品
        "Stocks", "Shares", "Equities", "Options", "Futures",
        "Bonds", "Mutual Funds", "Index Funds", "ETFs", "Exchange Traded Funds",

        # 市场分析
        "Technical Analysis", "Fundamental Analysis", "Macroeconomic",
        "Macroeconomics", "Microeconomic", "Microeconomics", "Market Trend", "Market analysis",

        # 市场指标
        "P/E Ratio", "Price-to-Earnings Ratio", "P/B Ratio",
        "Price-to-Book Ratio", "Dividend Yield", "Dividend", "Beta", "Volatility", "Volatilities",

        # 市场事件
        "Earning", "Earn", "Earns", "Earner", "Earned", "Earnings Season", "Earnings report", "Stock Split", "IPO",
        "Initial Public Offering", "Secondary Offering", "Buyback", "Buybacks", "Buybacking", "Buybacked",
        "stock", "stocks", "Stock buyback", "Dividend", "offer", "offers", "offering", "offered",

        # 监管机构
        "Securities and Exchange Commission", "SEC",
        "Financial Industry Regulatory Authority", "FINRA",

        # 经济数据
        "Employment Data", "Job data", "Interest Rates", "Inflation", "Inflations",
        "GDP", "Manufacturing Index", "Consumer Confidence Index",

        # 市场术语
        "Bull Market", "Bear Market", "Correction", "Corrections", "Market correction",
        "Crash", "Crashed", "Crashing", "Market crash", "Circuit Breaker", "Market halt", "Blue-Chip Stocks",

        # 股票走势
        "Rise", "Increase", "Upswing", "Fall", "Decrease",
        "Drop", "Downtrend", "Volatility", "Fluctuation", "Rebound",
        "Rally", "Pullback", "Breakout", "Reversal",

        # 市场表现
        "Strong", "Weak", "Stable", "Volatile",
        "Increased Volatility", "Decreased Volatility",

        # 交易量
        "Volume", "High Volume", "Low Volume", "Active Trading", "Sparse Trading",

        # 价格行为
        "Limit Up", "Limit Down", "Gap", "Price gap",
        "Support Level", "Resistance Level",

        # 市场情绪
        "Optimistic", "Positive sentiment", "Pessimistic", "Negative sentiment",
        "Panic", "Greed", "Confidence", "Panic Selling",

        # 投资策略
        "Long-term Investment", "Long-term investing", "Short-term Trading",
        "Short-term investing", "Value Investing", "Growth Investing",
        "Technical Analysis", "Fundamental Analysis",

        # 市场阶段
        "Bull Market", "Bear Market", "Consolidation", "Market consolidation",
        "Bottoming", "Topping",

        # 市场分类
        "Large-cap Stocks", "Large-cap", "Mid-cap Stocks",
        "Mid-cap", "Small-cap Stocks", "Small-cap", "Blue-chip Stocks",
        "Blue-chips", "Junk Stocks", "Junk", "Cyclical Stocks",
        "Cyclicals", "Defensive Stocks", "Defensives",

        # 交易时间
        "Open", "Opening Bell", "Close", "Closing Bell",
        "Pre-market Trading", "After-hours Trading",

        # 市场分析
        "Market Trend", "Market Analysis", "Market Forecast",
        "Market Report",

        # 经济数据
        "Employment Data", "Job data", "Interest Rates",
        "GDP", "Gross Domestic Product", "Manufacturing Index",

        # 金融事件
        "IPO", "Initial Public Offering", "Secondary Offering",
        "Stock Buyback", "Buyback", "Dividend", "Stock Split",

        # 监管机构
        "SEC", "Securities and Exchange Commission",
        "FINRA", "Financial Industry Regulatory Authority",

        # 金融产品
        "Stocks", "Shares", "Equities", "Bonds", "Debt instruments",
        "Options", "Futures", "ETFs", "Exchange Traded Funds",
        "Mutual Funds",
    ]
    dates = ['2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
             '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    nlp = spacy.load("en_core_web_lg")
    for date in dates:
        orign_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\combined_original_fulltext_and_tweet_id_{date}_with_languages.csv'
        result_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\spacy_economy\fulltext_and_tweet_id_with_economy_{date}.csv'
        print('正在处理经济词表的：',orign_filepath)
        # 创建匹配器函数，忽略大小写
        def case_insensitive_matcher(nlp, terms):
            patterns = [nlp.make_doc(text.lower()) for text in terms]
            return patterns

        # 创建PhraseMatcher对象
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        # 将词表转换为文档对象，用于匹配
        patterns = case_insensitive_matcher(nlp, terms)

        # 向匹配器添加词表
        matcher.add("TechTerms", None, *patterns)

        processed_count = 0  # 用于计数已处理的数据行数

        # 打开结果文件，准备写入结果
        with open(result_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Text', 'Language', 'Matched Phrases'])

            # 打开原始数据文件，并读取数据
            with open(orign_filepath, newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader)  # Skip header

                for row in reader:
                    id, text, language = row  # Assuming the order is id, text, language
                    doc = nlp(text)
                    matches = matcher(doc)
                    matched_terms = []
                    for match_id, start, end in matches:
                        span = doc[start:end]
                        matched_terms.append(span.text)
                    if matched_terms:
                        matched_terms = '/'.join(set(matched_terms))  # Remove duplicates and join with '/'
                        writer.writerow([id, text, language, matched_terms])  # Write results directly to file

                    processed_count += 1
                    if processed_count % 10000 == 0:
                        print(f"Processed {processed_count} rows.")

        print(f"Total processed rows: {processed_count}")
        print(f"Results saved to {result_filepath}")


def spacy_candidate():
    dates = ['2019_12', '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
              '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']
    terms = [
    "Maine Legislature",
    "Legislature",
    "Legislatures",
    "Legislative",
    "Legislations",
    "Legislation",
    "Legislate",
    "Legislates",
    "Legislated",
    "Legislating",
    "Voting",
    "Vote",
    "Votes",
    "Voted",
    "Votor",
    "Votors",
    "Voter",
    "Voters",
    "Elector",
    "Electors",
    "Electorate",
    "Electorates",
    "Electorating",
    "Electorated",
    "Election",
    "Elections",
    "Elect",
    "Elects",
    "Electing",
    "Elected",
    "Electoral",
    "Election Night",
    "Presidential election",
    "Constituency",
    "Janet Mills",
    "Pollsters",
    "Pollster",
    "Media polling",
    "Phony polls",
    "Fake polls",
    "Polls",
    "Poll",
    "Polled",
    "Polling",
    "Pollings",
    "Vote",
    "Votes",
    "Banknote",
    "Banknotes",
    "Polling Station",
    "Polling Stations",
    "Ballot",
    "Ballots",
    "Tickets",
    "Ticket",
    "Bill",
    "Bills",
    "Billing",
    "Billed",
    "Election",
    "Elections",
    "Electoral Vote",
    "Electoral Votes",
    "Electoral",
    "Immigration",
    "Immigrations",
    "Immigrate",
    "Immigrating",
    "Immigrates",
    "Immigrated",
    "Virus",
    "Debate",
    "Debates",
    "Moderator",
    "Moderators",
    "Candidate",
    "Candidates",
    "Quadrennial",
    "Senator",
    "Senators",
    "Senate",
    "Senates",
    "Senating",
    "Senated",
    "Community",
    "Communities",
    "Democracy",
    "Democratic",
    "Democrat",
    "Democrats",
    "Republican",
    "Republicans",
    "Republic",
    "Party",
    "Parties",
    "Government",
    "Governments",
    "Vice",
    "Vice President",
    "President",
    "Presidents",
    "Presidential",
    "Wall Street",
    "Latino",
    "African American",
    "Asian American",
    "Hurricane",
    "First Lady",
    "Karen Pence",
    "Border Wall",
    "Middle East",
    "ISIS",
    "Iran",
    "Afghanistan",
    "Iran Nuclear Deal",
    "Embassy",
    "Embassies",
    "Jerusalem",
    "Israeli",
    "Qasem Soleimani",
    "Manufacturing jobs",
    "Auto Industry",
    "Iraq War",
    "Vaccine",
    "Socialism",
    "Congresswoman",
    "5G",
    "Borders",
    "Taxes",
    "Opportunity Zones",
    "Patriotic education",
    "Free Speech",
    "Economy",
    "Economies",
    "Healthcare",
    "Climate Change",
    "Education",
    "Justice",
    "Equality",
    "Reform",
    "Reforming",
    "Reformed",
    "Reforms",
    "Policy",
    "Policies",
    "Security",
    "Securities",
    "Innovation",
    "Innovations",
    "Platform",
    "Platforms",
    "Policy",
    "Policies",
    "Discussion",
    "Discussions",
    "Question",
    "Questions",
    "Answer",
    "Answers",
    "Argument",
    "Arguments",
    "Issue",
    "Issues",
    "Result",
    "Results",
    "Turnout",
    "Turnouts",
    "Winner",
    "Winners",
    "Loser",
    "Losers",
    "Campaign",
    "Campaigns",
    "Advocate",
    "Advocating",
    "Law",
    "Discrimination",
    "LGBTQ+",
    "Feminism",
    "Authenticity",
    "LGBT+",
    "Far-left",
    "Donald Trump",
    "Joe Biden",
    "Delaware",
    "Florida",
    "Kamala Harris",
    "Mike Pence",
    "Biden",
    "Trump",
    "Pence",
    "Harris",
    "Debate",
    "Presidential debate",
    "Vice presidential",
    "debate First debate Second debate Third debate Moderator Debate topics Fact-checking Debate highlights Debate performance Opening statement Closing statement Debate schedule",
    "Delegates",
    "George Floyd",
    "Supreme Court",
    "Public health",
    "Ruth Bader Ginsburg",
    "Amy Coney Barrett",
    "Affordable Care Act",
    "Mail-in",
    "Mail-ins",
    "Post",
    "Posts",
    "Posted",
    "Posting",
    "Swing states",
    "States",
    "State",
    "Vote counting",
    "Voter fraud",
    "Fraud",
    "Frauds",
    "Frauding",
    "Fraudulent",
    "Fraudulently",
    "Fraudulency",
    "Fraudulence",
    "Fraudulences",
    "Defrauding",
    "Defraud",
    "Defrauds",
    "Defrauded",
    "Forgery",
    "Forgeries",
    "Deceit",
    "Deceiting",
    "Deceits",
    "Deceited",
    "Deceitful",
    "Deceitfully",
    "Scams",
    "Scam",
    "Scaming",
    "Scamed",
    "Deception",
    "Deceptions",
    "Decept",
    "Decepts",
    "Decepting",
    "Deceptive",
    "Deceptively",
    "Decepted",
    "Fob",
    "Fobs",
    "Fobing",
    "Fobbed",
    "Gudgeon",
    "Gudgeons",
    "Fakement",
    "Fakements",
    "Fake",
    "Fakes",
    "Fakeing",
    "Faked",
    "Deceive",
    "Deceives",
    "Deceiving",
    "Deceived",
    "Misrepresentation",
    "Misrepresentations",
    "Misrepresent",
    "Misrepresents",
    "Misrepresenting",
    "Misrepresented",
    "Theft",
    "Thefts",
    "Cheat",
    "Cheats",
    "Cheating",
    "Cheated",
    "Finagle",
    "Finagles",
    "Finagling",
    "Finagled",
    "Swindle",
    "Swindling",
    "Swindles",
    "Swindling",
    "Crime",
    "Crimes",
    "Law",
    "Coup",
    "Coups",
    "Coup d'état",
    "Congress",
    "Department of Justice",
    "Corrupt",
    "Corrupted",
    "Corruption",
    "Corruptions",
    "Electoral College",
    "Fight like hell",
    "Capitol",
    "Inauguration",
    "Primary election",
    "Nominate",
    "Nominating",
    "Nominates",
    "Nominated",
    "Propose",
    "Proposed",
    "Proposes",
    "Proposing",
    "United States House of Representatives",
    "Representatives",
    "Representative",
    "Agent",
    "Agents",
    "Official",
    "Officers",
    "Officer",
    "Spokesman",
    "Spokesmen",
    "Speech",
    "speeches",
    "United States",
    "US",
    "U.S",
    "House of Representatives",
]
    nlp = spacy.load("en_core_web_lg")
    for date in dates:
        orign_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\combined_original_fulltext_and_tweet_id_{date}_with_languages.csv'
        result_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\spacy_candidate\fulltext_and_tweet_id_with_economy_{date}.csv'
        print('正在处理候选人词表的：', orign_filepath)
        # 创建匹配器函数，忽略大小写
        def case_insensitive_matcher(nlp, terms):
            patterns = [nlp.make_doc(text.lower()) for text in terms]
            return patterns

        # 创建PhraseMatcher对象
        matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        # 将词表转换为文档对象，用于匹配
        patterns = case_insensitive_matcher(nlp, terms)

        # 向匹配器添加词表
        matcher.add("TechTerms", None, *patterns)

        processed_count = 0  # 用于计数已处理的数据行数

        # 打开结果文件，准备写入结果
        with open(result_filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', 'Text', 'Language', 'Matched Phrases'])

            # 打开原始数据文件，并读取数据
            with open(orign_filepath, newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                header = next(reader)  # Skip header

                for row in reader:
                    id, text, language = row  # Assuming the order is id, text, language
                    doc = nlp(text)
                    matches = matcher(doc)
                    matched_terms = []
                    for match_id, start, end in matches:
                        span = doc[start:end]
                        matched_terms.append(span.text)
                    if matched_terms:
                        matched_terms = '/'.join(set(matched_terms))  # Remove duplicates and join with '/'
                        writer.writerow([id, text, language, matched_terms])  # Write results directly to file

                    processed_count += 1
                    if processed_count % 10000 == 0:
                        print(f"Processed {processed_count} rows.")

        print(f"Total processed rows: {processed_count}")
        print(f"Results saved to {result_filepath}")

#word_tokenize使用的是Punkt分词算法，这是一个基于机器学习的分词器。对于每个文本的处理时间通常是线性的，即时间复杂度是 O(n)，其中 n 是文本中的字符数
#NLTK的word_tokenize可以帮助处理单词的标点和变体形式，提高分词的准确性
def nltk_test_convid():
    # 确保已经安装并下载了punkt tokenizer
    nltk.download('punkt')
    nltk.download('wordnet')

    date = '2019_12'
    orign_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\combined_original_fulltext_and_tweet_id_{date}_with_languages.csv'
    result_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\nltk_convid\fulltext_and_tweet_id_with_convid_{date}.csv'
    lemmatizer = WordNetLemmatizer()
    def process_text(text, terms):
        # 使用NLTK的word_tokenize进行分词
        words = word_tokenize(text.lower())
        # 使用词形还原
        lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
        # 查找并返回匹配的关键词
        return '/'.join(set(word for word in lemmatized_words if word in terms))


    # 假设terms是你的关键词列表
    # 将词表转换为集合
    terms = {"Coronavirus", "COVID-19", "SARS-CoV-2", "Pandemic", "Epidemic", "Epi", "Outbreak", "Infection",
             "Virus",
             "Variant", "Strain", "Coronavirus", "CDC", "Ncov", "covid-19", "covid 19", "covid19", "corona virus",
             "corona", "covd", "covid", "covid19vaccine", "covid19 pfizer", "covid19 moderna",
             "covid19 astrazeneca",
             "covid19 biontech", "pfizercovidvaccine", "covidvaccine pfizer", "modernacovidvaccine",
             "astrazenecacovidvaccine", "biontechcovidvaccine", "covidvaccine", "notocoronavirusvaccines",
             "coronavirusvaccine", "coronavaccine", "vaccinessavelives", "pfizervaccine", "modernavaccine",
             "oxfordvaccine", "astrazenecavaccine", "biontechvaccine", "vaccineworks", "azvaccine", "vaccine",
             "covidiots", "covid_19 pfizer", "Pfizer", "covid Pfizer", "covid-19 moderna", "covid moderna",
             "coronavirusupdates astrazeneca", "coronavirusupdates biontech", "coronavirus astrazeneca",
             "coronavirus biontech", "covid-19 astrazeneca", "covid astrazeneca", "covid biontech",
             "covid-19 biontech",
             "vaccination", "corona Pfizer", "pfizerbiontech", "corona moderna", "endthelockdown", "greatreset",
             "corona astrazeneca", "corona biontech", "plandemic", "iwillgetvaccinated", "getvaccinated", "mrna",
             "eugenics", "thisisourshot", "vaccinate", "sputnikv", "covax", "kungflu", "rna", "gavi",
             "depopulation",
             "peoplesbodyyourchoice", "iwillnotcomply", "mybodymychoice", "pharmagreed", "glyphosate", "vaxxx",
             "vaxx",
             "vax", "cepi", "nvic", "sars-cov-2", "COVID", "Corona", "Virus", "C19", "Vaccine", "Vax", "Jab",
             "Vaxx",
             "Coronavirus disease", "C19", "Corona", "Virus", "SARS", "CoV2", "Global outbreak", "Local outbreak",
             "Breakout", "Infection", "Infect", "virus", "Mutation", "Fever", "Cough", "Fatigue", "Loss of taste",
             "Loss of smell", "Shortness of breath", "Muscle or body aches", "Headache", "Sore throat",
             "Congestion",
             "Nausea", "Vomiting", "Diarrhea", "Symptoms", "Asymptomatic", "Symptomatic", "PCR test",
             "Antigen test",
             "Antibody test", "Rapid test", "Test kit", "Diagnosis", "Quarantine", "Isolation", "PCR", "Rapid test",
             "Social distancing", "SD", "S. Distancing", "Soc Dist", "Social Dist", "Physical Distancing",
             "Physical Dist", "Phy Dist", "P. Distancing", "Keep Distance", "Stay Away", "Avoid Crowds",
             "No Crowds",
             "Safe Distance", "Safety Space", "Limit Gatherings", "No Gatherings", "Avoid Gatherings", "Distanc",
             "Distancing", "Distance", "Social Distancing", "Distancing", "Socialdistancing", "Hand washing",
             "Sanitizer", "Disinfection", "Lockdown", "lock down", "lockdown", "Isolation", "Iso", "Curfew",
             "Contact tracing", "Travel ban", "Vaccine", "Vaccination", "Booster shot", "Immunity", "Herd immunity",
             "Mask", "mask", "Mask wearing", "wear a mask", "wearamask", "maskup", "Wearamask", "Wearadamnmask",
             "NoMasks", "masksoff", "MasksOffAmerica", "face cover", "facecover", "PPE", "Sanitizer", "Ventilator",
             "Quarantine", "stayathome", "stay at home", "stay-at-home", "social distanc", "Ventilator", "PPE",
             "ICU",
             "Oxygen", "Respirator", "Flatten the curve", "Super spreader", "Hotspot", "Wave", "Asymptomatic",
             "Symptomatic", "Transmission", "Incubation period", "Mortality rate", "Recovery rate"}
    terms = set(lemmatizer.lemmatize(term) for term in terms)  # 词形还原处理

    # 读取CSV文件中的待匹配文本
    matches_output = []
    processed_count = 0
    with open(orign_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header
        for row in reader:
            id, text, language = row  # Assuming the order is id, text, language
            matched_terms = process_text(text, terms)
            if matched_terms:
                matches_output.append([id, text, language, matched_terms])
            processed_count += 1
            if processed_count % 10000 == 0:
                print(f"Processed {processed_count} rows.")

    # 将匹配结果保存到新文件
    with open(result_filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Text', 'Language', 'Matched Phrases'])
        writer.writerows(matches_output)

def drop_duplicate():
    # 指定文件夹路径
    directory = r'G:\original_fulltext_and_tweet_id_with_languages'
    # 输出文件夹路径
    output_directory = r'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate'
    os.makedirs(output_directory, exist_ok=True)

    # 遍历文件夹下所有文件
    for filename in os.listdir(directory):
        if filename.startswith("combined_original_fulltext_and_tweet_id_") and filename.endswith(".csv"):
            # 构建完整的文件路径
            file_path = os.path.join(directory, filename)
            # 读取CSV文件
            df = pd.read_csv(file_path, dtype=str)

            # 去重，保留第一个出现的retweet_id
            df.drop_duplicates(subset=['retweet_id'], keep='first', inplace=True)

            # 构建输出文件路径
            output_file_path = os.path.join(output_directory, filename)
            # 保存处理后的数据到新文件
            df.to_csv(output_file_path, index=False)
            print("新文件保存在：",output_file_path)

    print("所有文件已处理并保存在新的文件夹中。")









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
    dates = ['2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
             '2020_10', '2020_11', '2020_12', '2021_01', '2021_02']

    topic_name = 'economy'
    # 定义输入和输出目录
    input_dir = r'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate'
    output_dir = rf'F:\Intermediate Results\original_fulltext_and_tweet_id_spacy_drop_duplicate\Topic_Keywords_Identification\spacy_{topic_name}'
    #经济相关
    terms = [  # 经济指标
        "Investment", "Invest", "Investing", "Invests", "Invested", "Investing", "Investor", "Investors", "GDP", "GDPs",
        "GDP growth", "Gross Domestic Product", "GDP increases",
        "Unemployment", "Employing", "Unemploy", "employ", "employer", "employee", "Unemployment rate", "Job", "jobs",
        "Jobless rate", "Jobless",
        "Manufacturing PMI", "Purchasing Managers' Index", "PMI", "Housing starts", "House", "Houses",
        "Consumer", "Consuming", "Consumed", "Consumers", "consumption", "consumptions", "Consumer spending",
        "Consumer expenditure", "Personal consumption expenditures",
        "Personal spending",

        # 政策措施
        "Quantitative Easing", "QE", "Emergency rate cut", "Fiscal stimulus",
        "Stimulus package", "Relief bill", "bill", "bills", "Relief package", "Loan support",
        "Unlimited QE", "Unlimited Quantitative Easing",

        # 行业影响
        "industry", "industries", "Tourism industry", "Tourism sector", "Agriculture", "Farming", "Manufacturing",
        "Real estate", "Property market", "market", "markets", "marketing", "marketed", "Service industry",
        "Service sector", "sectors",

        # 经济事件
        "Economic", "COVID-19 pandemic", "COVID-19", "Coronavirus pandemic", "Economic recession",
        "Economic downturn", "Stock market volatility", "volatility", "Market fluctuations",
        "Lockdown measures", "Lockdowns", "Vaccine development", "Vaccine rollout",
        "Economic recovery", "Recovery",

        # 经济数据
        "Gross Domestic Product", "GDP", "Federal funds rate", "Fed rate",
        "Interest rate", "Inflation rate", "Trade balance", "Fiscal deficit",
        "Budget deficit",

        # 经济预测
        "Economic outlook", "Growth forecast", "Market expectations",

        # 经济主体
        "Federal Reserve", "Fed", "Department of the Treasury", "Treasury",
        "Enterprises", "Companies", "Company", "Corporations", "Consumers", "Investors",
        "commerce", "business", "trade", "trades", "trading", "traded", "funds", "fund", "funding", "funded",

        # 经济行为
        "shopping", "Online shopping", "E-commerce", "Remote work", "work", "works", "working", "worked",
        "Telecommuting",
        "Work from home", "Shelter-in-place", "Stay-at-home orders", "Investment decision",
        "Investment choices",

        # 经济术语
        "Economic stimulus", "Stimulus", "Economic contraction", "Recession",
        "Negative interest rates", "Monetary policy", "Fiscal policy",

        # 主要指数
        "Dow Jones Industrial Average", "DJIA", "S&P 500",
        "Standard & Poor's 500", "NASDAQ Composite", "Russell 2000",

        # 交易所
        "New York Stock Exchange", "NYSE", "NASDAQ Stock Market",
        "NASDAQ", "American Stock Exchange", "AMEX",

        # 交易时间
        "Opening Bell", "Open", "Closing Bell", "Close",
        "Pre-market trading", "After-hours trading",

        # 交易行为
        "Buy", "Buys", "Buying", "Bought", "Purchase", "Purchases", "Purchasing", "Purchased", "Sell", "Sells", "sold",
        "Selling", "Seller", "Bullish", "Bull market",
        "Bearish", "Bear market", "Stop-loss",

        # 市场参与者
        "Investors", "Traders", "Brokers", "Analysts", "Fund Managers",

        # 金融产品
        "Stocks", "Shares", "Equities", "Options", "Futures",
        "Bonds", "Mutual Funds", "Index Funds", "ETFs", "Exchange Traded Funds",

        # 市场分析
        "Technical Analysis", "Fundamental Analysis", "Macroeconomic",
        "Macroeconomics", "Microeconomic", "Microeconomics", "Market Trend", "Market analysis",

        # 市场指标
        "P/E Ratio", "Price-to-Earnings Ratio", "P/B Ratio",
        "Price-to-Book Ratio", "Dividend Yield", "Dividend", "Beta", "Volatility", "Volatilities",

        # 市场事件
        "Earning", "Earn", "Earns", "Earner", "Earned", "Earnings Season", "Earnings report", "Stock Split", "IPO",
        "Initial Public Offering", "Secondary Offering", "Buyback", "Buybacks", "Buybacking", "Buybacked",
        "stock", "stocks", "Stock buyback", "Dividend", "offer", "offers", "offering", "offered",

        # 监管机构
        "Securities and Exchange Commission", "SEC",
        "Financial Industry Regulatory Authority", "FINRA",

        # 经济数据
        "Employment Data", "Job data", "Interest Rates", "Inflation", "Inflations",
        "GDP", "Manufacturing Index", "Consumer Confidence Index",

        # 市场术语
        "Bull Market", "Bear Market", "Correction", "Corrections", "Market correction",
        "Crash", "Crashed", "Crashing", "Market crash", "Circuit Breaker", "Market halt", "Blue-Chip Stocks",

        # 股票走势
        "Rise", "Increase", "Upswing", "Fall", "Decrease",
        "Drop", "Downtrend", "Volatility", "Fluctuation", "Rebound",
        "Rally", "Pullback", "Breakout", "Reversal",

        # 市场表现
        "Strong", "Weak", "Stable", "Volatile",
        "Increased Volatility", "Decreased Volatility",

        # 交易量
        "Volume", "High Volume", "Low Volume", "Active Trading", "Sparse Trading",

        # 价格行为
        "Limit Up", "Limit Down", "Gap", "Price gap",
        "Support Level", "Resistance Level",

        # 市场情绪
        "Optimistic", "Positive sentiment", "Pessimistic", "Negative sentiment",
        "Panic", "Greed", "Confidence", "Panic Selling",

        # 投资策略
        "Long-term Investment", "Long-term investing", "Short-term Trading",
        "Short-term investing", "Value Investing", "Growth Investing",
        "Technical Analysis", "Fundamental Analysis",

        # 市场阶段
        "Bull Market", "Bear Market", "Consolidation", "Market consolidation",
        "Bottoming", "Topping",

        # 市场分类
        "Large-cap Stocks", "Large-cap", "Mid-cap Stocks",
        "Mid-cap", "Small-cap Stocks", "Small-cap", "Blue-chip Stocks",
        "Blue-chips", "Junk Stocks", "Junk", "Cyclical Stocks",
        "Cyclicals", "Defensive Stocks", "Defensives",

        # 交易时间
        "Open", "Opening Bell", "Close", "Closing Bell",
        "Pre-market Trading", "After-hours Trading",

        # 市场分析
        "Market Trend", "Market Analysis", "Market Forecast",
        "Market Report",

        # 经济数据
        "Employment Data", "Job data", "Interest Rates",
        "GDP", "Gross Domestic Product", "Manufacturing Index",

        # 金融事件
        "IPO", "Initial Public Offering", "Secondary Offering",
        "Stock Buyback", "Buyback", "Dividend", "Stock Split",

        # 监管机构
        "SEC", "Securities and Exchange Commission",
        "FINRA", "Financial Industry Regulatory Authority",

        # 金融产品
        "Stocks", "Shares", "Equities", "Bonds", "Debt instruments",
        "Options", "Futures", "ETFs", "Exchange Traded Funds",
        "Mutual Funds",
    ]
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    # 定义部分函数，固定部分参数
    worker = partial(process_file, terms=terms, input_dir=input_dir, output_dir=output_dir)

    # # 获取CPU核心数，多线程处理内存会爆掉
    # num_processes = cpu_count()
    #
    # # 创建进程池并开始并行处理
    # with Pool(processes=num_processes) as pool:
    #     pool.map(worker, dates)

    # 顺序处理，不使用多线程
    for date in dates:
        worker(date)

    print("所有文件处理完成。")