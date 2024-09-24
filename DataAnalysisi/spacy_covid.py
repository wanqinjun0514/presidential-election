import spacy
from spacy.matcher import PhraseMatcher
import csv

import pandas as pd
import os

def spacy_too_slow():
    terms_old = [
        # 病毒和疾病
        "Coronavirus", "COVID-19", "SARS-CoV-2", "Pandemic", "Epidemic", "Epi",
        "Outbreak", "Infection", "Virus", "Variant", "Variants", "Strain", "Coronavirus", "CDC",
        "Ncov", "covid-19", "covid 19", "covid19", "corona virus", "corona", "covd", "covid", "covid19vaccine",
        "covid19 pfizer", "covid19 moderna", "covid19 astrazeneca", "covid19 biontech",
        "pfizercovidvaccine", "covidvaccine pfizer", "modernacovidvaccine",
        "astrazenecacovidvaccine", "biontechcovidvaccine", "covidvaccine",
        "notocoronavirusvaccines", "coronavirusvaccine", "coronavaccine", "vaccinessavelives",
        "pfizervaccine", "modernavaccine", "oxfordvaccine", "astrazenecavaccine",
        "biontechvaccine", "vaccineworks", "azvaccine", "vaccine", "vaccines", "covidiots",
        "covid_19 pfizer", "Pfizer", "covid Pfizer", "covid-19 moderna", "covid moderna",
        "coronavirusupdates astrazeneca", "coronavirusupdates biontech", "coronavirus astrazeneca",
        "coronavirus biontech", "covid-19 astrazeneca", "covid astrazeneca", "covid biontech",
        "covid-19 biontech", "vaccination", "corona Pfizer", "pfizerbiontech", "corona moderna",
        "endthelockdown", "greatreset", "corona astrazeneca", "corona biontech", "plandemic",
        "iwillgetvaccinated", "getvaccinated", "mrna", "eugenics", "thisisourshot", "vaccinate",
        "sputnikv", "covax", "kungflu", "rna", "gavi", "depopulation", "peoplesbodyyourchoice",
        "iwillnotcomply", "mybodymychoice", "pharmagreed", "glyphosate", "vaxxx", "vaxx", "vax",
        "cepi", "nvic", "sars-cov-2", "COVID", "Corona", "Virus", "C19", "Vaccine", "Vax",
        "Jab", "Vaxx", "Coronavirus disease", "C19", "Corona", "Virus", "SARS", "CoV2",
        "Global outbreak", "Local outbreak", "Breakout", "Infection", "Infect", "virus",
        "Mutation",
        # 症状
        "Fever", "Cough", "Fatigue", "Loss of taste", "Loss of smell", "Shortness of breath",
        "Muscle or body aches", "Headache", "Sore throat", "Congestion", "Nausea", "Vomiting",
        "Diarrhea", "Symptoms", "Asymptomatic", "Symptomatic",
        # 检测和诊断
        "PCR test", "Antigen test", "Antibody test", "Rapid test", "Test kit", "Diagnosis",
        "Quarantine", "Isolation", "PCR", "Rapid test",
        # 防疫措施
        "Social distancing", "SD", "S. Distancing", "Soc Dist", "Social Dist", "Physical Distancing",
        "Physical Dist", "Phy Dist", "P. Distancing", "Keep Distance", "Stay Away", "Avoid Crowds",
        "No Crowds", "Safe Distance", "Safety Space", "Limit Gatherings", "No Gatherings",
        "Avoid Gatherings", "Distanc", "Distancing", "Distance", "Social Distancing", "Distancing",
        "Socialdistancing", "Hand washing", "Sanitizer", "Disinfection", "Lockdown", "lock down",
        "lockdown", "Isolation", "Iso", "Curfew", "Contact tracing", "Travel ban", "Vaccine",
        "Vaccination", "Booster shot", "Immunity", "Herd immunity", "Mask", "mask", "Mask wearing",
        "wear a mask", "wearamask", "maskup", "Wearamask", "Wearadamnmask", "NoMasks", "masksoff",
        "MasksOffAmerica", "face cover", "facecover", "PPE", "Sanitizer", "Ventilator", "Quarantine",
        "stayathome", "stay at home", "stay-at-home", "social distanc",
        # 医疗设备
        "Ventilator", "PPE", "ICU", "Oxygen", "Respirator",
        # 其他常见词汇
        "Flatten the curve", "Super spreader", "Hotspot", "Wave", "Asymptomatic", "Symptomatic",
        "Transmission", "Incubation period", "Mortality rate", "Recovery rate"
    ]
    terms = ["Coronavirus", "Coronaviruses",
    "COVID-19", "Covid-19", "covid 19", "covid19", "covid-19", "COVID", "Covid",
    "SARS-CoV-2", "SARS", "CoV2", "sars-cov-2",
    "Pandemic", "Pandemics",
    "Epidemic", "Epidemics",
    "Epi",
    "Outbreak", "Outbreaks",
    "Infection", "Infections", "Infect", "Infected", "Infecting",
    "Virus", "Viruses", "Viral",
    "Variant", "Variants",
    "Strain", "Strains",
    "CDC","CDCgov",
    "Ncov",
    "Corona", "coronas", "corona virus",
    "Covd",
    "COVID19vaccine", "covid19vaccine",
    "COVID19 Pfizer", "covid19 Pfizer", "covid-19 Pfizer", "covid Pfizer",
    "COVID19 Moderna", "covid19 Moderna", "covid-19 Moderna", "covid Moderna",
    "COVID19 AstraZeneca", "covid19 AstraZeneca", "covid-19 AstraZeneca", "covid AstraZeneca",
    "COVID19 BioNTech", "covid19 BioNTech", "covid-19 BioNTech", "covid BioNTech",
    "PfizerCOVIDvaccine", "pfizercovidvaccine",
    "ModernaCOVIDvaccine", "modernacovidvaccine",
    "AstraZenecaCOVIDvaccine", "astrazenecacovidvaccine",
    "BioNTechCOVIDvaccine", "biontechcovidvaccine",
    "COVIDvaccine", "covidvaccine",
    "Coronavirusvaccine", "coronavirusvaccine",
    "Coronavaccine", "coronavaccine",
    "VaccinesSaveLives", "vaccinessavelives",
    "PfizerVaccine", "pfizervaccine",
    "ModernaVaccine", "modernavaccine",
    "OxfordVaccine", "oxfordvaccine",
    "AstraZenecaVaccine", "astrazenecavaccine",
    "BioNTechVaccine", "biontechvaccine",
    "VaccineWorks", "vaccineworks",
    "AZVaccine", "azvaccine",
    "Vaccine", "Vaccines",
    "COVIDiots", "covidiots",
    "Vaccination", "Vaccinations", "Vaccinate", "Vaccinated", "Vaccinating",
    "EndTheLockdown", "endthelockdown",
    "GreatReset", "greatreset",
    "Plandemic", "plandemic",
    "IWillGetVaccinated", "iwillgetvaccinated",
    "GetVaccinated", "getvaccinated",
    "mRNA", "mrna",
    "Eugenics",
    "ThisIsOurShot", "thisisourshot",
    "SputnikV", "sputnikv",
    "COVAX", "covax",
    "KungFlu", "kungflu",
    "RNA", "rna",
    "GAVI", "gavi",
    "Depopulation",
    "PeoplesBodyYourChoice", "peoplesbodyyourchoice",
    "IWillNotComply", "iwillnotcomply",
    "MyBodyMyChoice", "mybodymychoice",
    "PharmaGreed", "pharmagreed",
    "Glyphosate",
    "Vaxxx", "Vaxx", "Vax",
    "CEPI", "cepi",
    "NVIC", "nvic",
    "Jab", "Jabs",
    "Fever", "Fevers",
    "Cough", "Coughs", "Coughing", "Coughed",
    "Fatigue",
    "Loss of taste",
    "Loss of smell",
    "Shortness of breath",
    "Muscle or body ache", "Muscle or body aches",
    "Headache", "Headaches",
    "Sore throat", "Sore throats",
    "Congestion",
    "Nausea",
    "Vomiting",
    "Diarrhea",
    "Symptom", "Symptoms",
    "Asymptomatic",
    "Symptomatic",
    "PCR test", "PCR tests",
    "Antigen test", "Antigen tests",
    "Antibody test", "Antibody tests",
    "Rapid test", "Rapid tests",
    "Test kit", "Test kits",
    "Diagnosis", "Diagnoses", "Diagnose", "Diagnosed", "Diagnosing",
    "Quarantine", "Quarantines", "Quarantined", "Quarantining",
    "Isolation", "Isolations", "Isolated", "Isolating", "Isolate",
    "Social distancing", "S. Distancing", "Soc Dist", "Social Dist", "Phy Dist", "P. Distancing", "Distance", "Distances", "Distancing", "Socialdistancing",
    "Hand washing", "Hand washes", "Hand washed", "Hand washing",
    "Sanitizer", "Sanitizers", "Sanitizing"]
    # 加载模型
    nlp = spacy.load("en_core_web_lg")

    # 创建匹配器函数，忽略大小写
    def case_insensitive_matcher(nlp, terms):
        patterns = [nlp.make_doc(text.lower()) for text in terms]
        return patterns
    dates = ['2020_02','2020_03','2020_04','2020_05','2020_06','2020_08','2020_09','2020_10','2020_11','2020_12','2021_01','2021_02']
    for date in dates:
        orign_filepath = rf'H:\original_fulltext_and_tweet_id\original_fulltext_and_tweet_id_with_languages\drop_duplicate\combined_original_fulltext_and_tweet_id_{date}_with_languages.csv'
        result_filepath = rf'H:\original_fulltext_and_tweet_id\original_fulltext_and_tweet_id_with_languages\drop_duplicate\spacy_convid\fulltext_and_tweet_id_with_convid_{date}.csv'

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


# #word_tokenize使用的是Punkt分词算法，这是一个基于机器学习的分词器。对于每个文本的处理时间通常是线性的，即时间复杂度是 O(n)，其中 n 是文本中的字符数
# #NLTK的word_tokenize可以帮助处理单词的标点和变体形式，提高分词的准确性
# def nltk_test_convid():
#     # 确保已经安装并下载了punkt tokenizer
#     nltk.download('punkt')
#     nltk.download('wordnet')
#
#     date = '2019_12'
#     orign_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\combined_original_fulltext_and_tweet_id_{date}_with_languages.csv'
#     result_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\nltk_convid\fulltext_and_tweet_id_with_convid_{date}.csv'
#     lemmatizer = WordNetLemmatizer()
#     def process_text(text, terms):
#         # 使用NLTK的word_tokenize进行分词
#         words = word_tokenize(text.lower())
#         # 使用词形还原
#         lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
#         # 查找并返回匹配的关键词
#         return '/'.join(set(word for word in lemmatized_words if word in terms))
#
#
#     # 假设terms是你的关键词列表
#     # 将词表转换为集合
#     terms = {"Coronavirus", "COVID-19", "SARS-CoV-2", "Pandemic", "Epidemic", "Epi", "Outbreak", "Infection",
#              "Virus",
#              "Variant", "Strain", "Coronavirus", "CDC", "Ncov", "covid-19", "covid 19", "covid19", "corona virus",
#              "corona", "covd", "covid", "covid19vaccine", "covid19 pfizer", "covid19 moderna",
#              "covid19 astrazeneca",
#              "covid19 biontech", "pfizercovidvaccine", "covidvaccine pfizer", "modernacovidvaccine",
#              "astrazenecacovidvaccine", "biontechcovidvaccine", "covidvaccine", "notocoronavirusvaccines",
#              "coronavirusvaccine", "coronavaccine", "vaccinessavelives", "pfizervaccine", "modernavaccine",
#              "oxfordvaccine", "astrazenecavaccine", "biontechvaccine", "vaccineworks", "azvaccine", "vaccine",
#              "covidiots", "covid_19 pfizer", "Pfizer", "covid Pfizer", "covid-19 moderna", "covid moderna",
#              "coronavirusupdates astrazeneca", "coronavirusupdates biontech", "coronavirus astrazeneca",
#              "coronavirus biontech", "covid-19 astrazeneca", "covid astrazeneca", "covid biontech",
#              "covid-19 biontech",
#              "vaccination", "corona Pfizer", "pfizerbiontech", "corona moderna", "endthelockdown", "greatreset",
#              "corona astrazeneca", "corona biontech", "plandemic", "iwillgetvaccinated", "getvaccinated", "mrna",
#              "eugenics", "thisisourshot", "vaccinate", "sputnikv", "covax", "kungflu", "rna", "gavi",
#              "depopulation",
#              "peoplesbodyyourchoice", "iwillnotcomply", "mybodymychoice", "pharmagreed", "glyphosate", "vaxxx",
#              "vaxx",
#              "vax", "cepi", "nvic", "sars-cov-2", "COVID", "Corona", "Virus", "C19", "Vaccine", "Vax", "Jab",
#              "Vaxx",
#              "Coronavirus disease", "C19", "Corona", "Virus", "SARS", "CoV2", "Global outbreak", "Local outbreak",
#              "Breakout", "Infection", "Infect", "virus", "Mutation", "Fever", "Cough", "Fatigue", "Loss of taste",
#              "Loss of smell", "Shortness of breath", "Muscle or body aches", "Headache", "Sore throat",
#              "Congestion",
#              "Nausea", "Vomiting", "Diarrhea", "Symptoms", "Asymptomatic", "Symptomatic", "PCR test",
#              "Antigen test",
#              "Antibody test", "Rapid test", "Test kit", "Diagnosis", "Quarantine", "Isolation", "PCR", "Rapid test",
#              "Social distancing", "SD", "S. Distancing", "Soc Dist", "Social Dist", "Physical Distancing",
#              "Physical Dist", "Phy Dist", "P. Distancing", "Keep Distance", "Stay Away", "Avoid Crowds",
#              "No Crowds",
#              "Safe Distance", "Safety Space", "Limit Gatherings", "No Gatherings", "Avoid Gatherings", "Distanc",
#              "Distancing", "Distance", "Social Distancing", "Distancing", "Socialdistancing", "Hand washing",
#              "Sanitizer", "Disinfection", "Lockdown", "lock down", "lockdown", "Isolation", "Iso", "Curfew",
#              "Contact tracing", "Travel ban", "Vaccine", "Vaccination", "Booster shot", "Immunity", "Herd immunity",
#              "Mask", "mask", "Mask wearing", "wear a mask", "wearamask", "maskup", "Wearamask", "Wearadamnmask",
#              "NoMasks", "masksoff", "MasksOffAmerica", "face cover", "facecover", "PPE", "Sanitizer", "Ventilator",
#              "Quarantine", "stayathome", "stay at home", "stay-at-home", "social distanc", "Ventilator", "PPE",
#              "ICU",
#              "Oxygen", "Respirator", "Flatten the curve", "Super spreader", "Hotspot", "Wave", "Asymptomatic",
#              "Symptomatic", "Transmission", "Incubation period", "Mortality rate", "Recovery rate"}
#     terms = set(lemmatizer.lemmatize(term) for term in terms)  # 词形还原处理
#
#     # 读取CSV文件中的待匹配文本
#     matches_output = []
#     processed_count = 0
#     with open(orign_filepath, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         header = next(reader)  # Skip header
#         for row in reader:
#             id, text, language = row  # Assuming the order is id, text, language
#             matched_terms = process_text(text, terms)
#             if matched_terms:
#                 matches_output.append([id, text, language, matched_terms])
#             processed_count += 1
#             if processed_count % 10000 == 0:
#                 print(f"Processed {processed_count} rows.")
#
#     # 将匹配结果保存到新文件
#     with open(result_filepath, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['ID', 'Text', 'Language', 'Matched Phrases'])
#         writer.writerows(matches_output)
#
# def drop_duplicate():
#     # 指定文件夹路径
#     directory = r'G:\original_fulltext_and_tweet_id_with_languages'
#     # 输出文件夹路径
#     output_directory = r'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate'
#     os.makedirs(output_directory, exist_ok=True)
#
#     # 遍历文件夹下所有文件
#     for filename in os.listdir(directory):
#         if filename.startswith("combined_original_fulltext_and_tweet_id_") and filename.endswith(".csv"):
#             # 构建完整的文件路径
#             file_path = os.path.join(directory, filename)
#             # 读取CSV文件
#             df = pd.read_csv(file_path, dtype=str)
#
#             # 去重，保留第一个出现的retweet_id
#             df.drop_duplicates(subset=['retweet_id'], keep='first', inplace=True)
#
#             # 构建输出文件路径
#             output_file_path = os.path.join(output_directory, filename)
#             # 保存处理后的数据到新文件
#             df.to_csv(output_file_path, index=False)
#             print("新文件保存在：",output_file_path)
#
#     print("所有文件已处理并保存在新的文件夹中。")
#
#
# # 使用WordNet词形还原器进行词形还原。词形还原通常比词干提取更为准确
# def nltk_WordNetLemmatizer():
#     # 确保已经安装并下载了punkt和wordnet
#     nltk.download('punkt')
#     nltk.download('wordnet')
#     nltk.download('averaged_perceptron_tagger')  # 用于词性标注
#     date = '2019_12'
#     orign_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\nltk_convid\combined_original_fulltext_and_tweet_id_{date}_with_languages - 副本.csv'
#     result_filepath = rf'G:\original_fulltext_and_tweet_id_with_languages\drop_duplicate\nltk_convid\fulltext_and_tweet_id_with_convid_{date}.csv'
#
#     lemmatizer = WordNetLemmatizer()
#     stemmer = PorterStemmer()  # 使用Porter词干提取器
#
#     def clean_text(text):
#         # 替换掉特殊字符与数字组合，使关键词与特殊符号分隔
#         text = text.replace('@', ' @')
#         return text
#
#     def process_text(text, terms):
#         text = clean_text(text)  # 清理文本
#         words = word_tokenize(text.lower())
#         tagged_words = nltk.pos_tag(words)  # 获取词性标注
#         lemmatized_words = [lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag)) if pos else stemmer.stem(word) for
#                             word, tag in tagged_words]
#         return '/'.join(set(word for word in lemmatized_words if word in terms))
#
#     def get_wordnet_pos(treebank_tag):
#         """转换treebank标签到wordnet标签"""
#         if treebank_tag.startswith('J'):
#             return 'a'
#         elif treebank_tag.startswith('V'):
#             return 'v'
#         elif treebank_tag.startswith('N'):
#             return 'n'
#         elif treebank_tag.startswith('R'):
#             return 'r'
#         else:
#             return None
#
#     terms = {"variant"}  # 使用集合存储基本形式
#     terms = set(lemmatizer.lemmatize(term) for term in terms)  # 词形还原处理
#
#     matches_output = []
#     processed_count = 0
#     with open(orign_filepath, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         header = next(reader)  # Skip header
#         for row in reader:
#             id, text, language = row
#             matched_terms = process_text(text, terms)
#             if matched_terms:
#                 matches_output.append([id, text, language, matched_terms])
#             processed_count += 1
#             if processed_count % 10000 == 0:
#                 print(f"Processed {processed_count} rows.")
#
#     with open(result_filepath, 'w', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['ID', 'Text', 'Language', 'Matched Phrases'])
#         writer.writerows(matches_output)

if __name__ == "__main__":
    spacy_too_slow()
    # drop_duplicate()
    # nltk_test_convid()