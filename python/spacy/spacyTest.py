import spacy

# 언어 모델 로드
nlp = spacy.load('en_core_web_sm')

# 텍스트 처리
doc = nlp("This is a sentence.")

# 문장 분리
for sent in doc.sents:
    print(sent)

# 토큰 출력
for token in doc:
    print(token.text, token.pos_)
