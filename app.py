"""Fridge Recipe Adventure - Flask Backend"""
from flask import Flask, render_template, request
from datetime import date, timedelta
import random

app = Flask(__name__)

# ── Recipe Database ────────────────────────────────────────────────────
MEATS = {
    "drumstick":   {"name": "닭다리", "emoji": "🍗", "color": "#ffd8a8"},
    "breast":      {"name": "닭가슴살", "emoji": "🍗", "color": "#ffd8a8"},
    "beef":        {"name": "소고기", "emoji": "🥩", "color": "#ffd8a8"},
    "pork":        {"name": "돼지고기", "emoji": "🥩", "color": "#ffd8a8"},
    "shrimp":      {"name": "새우", "emoji": "🦐", "color": "#a5d8ff"},
    "fish":        {"name": "생선", "emoji": "🐟", "color": "#a5d8ff"},
}

SPICES = {
    "basil":       {"name": "바질", "emoji": "🌿", "color": "#b2f2bb"},
    "oregano":     {"name": "오레가노", "emoji": "🌿", "color": "#b2f2bb"},
    "thyme":       {"name": "타임", "emoji": "🌿", "color": "#b2f2bb"},
    "paprika":     {"name": "파프리카 가루", "emoji": "🌶️", "color": "#b2f2bb"},
    "cumin":       {"name": "큐민", "emoji": "🌱", "color": "#b2f2bb"},
    "coriander":   {"name": "고수", "emoji": "🌿", "color": "#b2f2bb"},
}

RECIPES = {
    "drumstick": {
        "basil":     {"name": "바질 닭다리 구이", "cuisine": "지중해", "country": "그리스", "image": "🍗", "ingredients": [{"name": "닭다리", "amount": "2개", "owned": True}, {"name": "바질", "amount": "1줌", "owned": True}, {"name": "올리브오일", "amount": "2T", "owned": False}, {"name": "레몬", "amount": "1개", "owned": True}, {"name": "마늘", "amount": "3쪽", "owned": True}], "steps": ["닭다리에 소금, 후추로 밑간한다", "올리브오일, 레몬즙, 다진 마늘, 바질을 섞어 마리네이드 만든다", "닭다리를 마리네이드에 30분 재운다", "오븐 200°C에서 35분간 굽는다", "접시에 담아 완성"], "buy_link": "https://www.coupang.com/np/search?q=올리브오일+레몬"},
        "oregano":   {"name": "오레가노 닭다리 스튜", "cuisine": "이탈리아", "country": "이탈리아", "image": "🍲", "ingredients": [{"name": "닭다리", "amount": "2개", "owned": True}, {"name": "오레가노", "amount": "1T", "owned": True}, {"name": "토마토소스", "amount": "1컵", "owned": False}, {"name": "양파", "amount": "1개", "owned": True}, {"name": "올리브", "amount": "8개", "owned": False}], "steps": ["닭다리를 팬에 노릇하게 굽는다", "양파를 채썰어 볶는다", "토마토소스와 오레가노를 넣는다", "뚜껑 덮고 약불에서 30분 끓인다", "올리브를 올려 완성"], "buy_link": "https://www.coupang.com/np/search?q=토마토소스+올리브"},
        "thyme":     {"name": "타임 닭다리 로스트", "cuisine": "프랑스", "country": "프랑스", "image": "🍗", "ingredients": [{"name": "닭다리", "amount": "2개", "owned": True}, {"name": "타임", "amount": "3줄기", "owned": True}, {"name": "버터", "amount": "30g", "owned": True}, {"name": "감자", "amount": "2개", "owned": False}, {"name": "양송이", "amount": "6개", "owned": False}], "steps": ["닭다리에 소금, 후추, 타임을 뿌린다", "팬에 버터를 녹여 닭다리 겉면을 굽는다", "감자와 양송이를 넣는다", "오븐 190°C에서 30분간 굽는다", "접시에 담아 완성"], "buy_link": "https://www.coupang.com/np/search?q=감자+양송이버섯"},
        "paprika":   {"name": "파프리카 닭다리 스튜", "cuisine": "헝가리", "country": "헝가리", "image": "🍛", "ingredients": [{"name": "닭다리", "amount": "2개", "owned": True}, {"name": "파프리카 가루", "amount": "2T", "owned": True}, {"name": "사워크림", "amount": "3T", "owned": False}, {"name": "양파", "amount": "1개", "owned": True}, {"name": "파프리카", "amount": "1개", "owned": True}], "steps": ["닭다리를 한입 크기로 자른다", "양파와 파프리카를 볶는다", "닭다리와 파프리카 가루를 넣는다", "물 1컵을 붓고 25분간 끓인다", "사워크림을 올려 완성"], "buy_link": "https://www.coupang.com/np/search?q=사워크림"},
        "cumin":     {"name": "큐민 닭다리 탄두리", "cuisine": "인도", "country": "인도", "image": "🍗", "ingredients": [{"name": "닭다리", "amount": "2개", "owned": True}, {"name": "큐민", "amount": "1t", "owned": True}, {"name": "요거트", "amount": "1컵", "owned": True}, {"name": "강황", "amount": "1t", "owned": False}, {"name": "마늘", "amount": "3쪽", "owned": True}], "steps": ["요거트, 큐민, 강황, 다진 마늘을 섞는다", "닭다리를 소스에 1시간 재운다", "오븐 200°C에서 30분간 굽는다", "접시에 담고 레몬을 곁들인다"], "buy_link": "https://www.coupang.com/np/search?q=강황가루"},
        "coriander": {"name": "고수 닭다리 샐러드", "cuisine": "태국", "country": "태국", "image": "🥗", "ingredients": [{"name": "닭다리", "amount": "1개", "owned": True}, {"name": "고수", "amount": "1줌", "owned": True}, {"name": "라임", "amount": "1개", "owned": False}, {"name": "어장", "amount": "1T", "owned": False}, {"name": "청양고추", "amount": "2개", "owned": True}], "steps": ["닭다리를 삶아 찢는다", "라임즙, 어장, 다진 고추를 섞어 드레싱 만든다", "찢은 닭고기와 고수를 버무린다", "접시에 담아 완성"], "buy_link": "https://www.coupang.com/np/search?q=라임+어장"},
    },
    "breast": {
        "basil":     {"name": "바질 닭가슴살 샐러드", "cuisine": "지중해", "country": "그리스", "image": "🥗", "ingredients": [{"name": "닭가슴살", "amount": "200g", "owned": True}, {"name": "바질", "amount": "1줌", "owned": True}, {"name": "올리브오일", "amount": "2T", "owned": False}, {"name": "방울토마토", "amount": "5개", "owned": False}, {"name": "페타치즈", "amount": "50g", "owned": False}], "steps": ["닭가슴살을 소금, 후추로 밑간하여 굽는다", "구운 닭가슴살을 한입 크기로 썬다", "방울토마토를 반으로 자른다", "올리브오일, 바질로 드레싱을 만든다", "모든 재료를 버무려 완성"], "buy_link": "https://www.coupang.com/np/search?q=올리브오일+방울토마토+페타치즈"},
        "oregano":   {"name": "오레가노 치킨 파스타", "cuisine": "이탈리아", "country": "이탈리아", "image": "🍝", "ingredients": [{"name": "닭가슴살", "amount": "200g", "owned": True}, {"name": "오레가노", "amount": "1t", "owned": True}, {"name": "파스타면", "amount": "200g", "owned": True}, {"name": "토마토소스", "amount": "1컵", "owned": False}, {"name": "파마산 치즈", "amount": "30g", "owned": False}], "steps": ["파스타면을 삶는다", "닭가슴살을 팬에 굽는다", "토마토소스와 오레가노를 넣고 5분간 끓인다", "파스타를 소스에 버무린다", "파마산 치즈를 뿌려 완성"], "buy_link": "https://www.coupang.com/np/search?q=토마토소스+파마산치즈"},
        "thyme":     {"name": "타임 치킨 스테이크", "cuisine": "프랑스", "country": "프랑스", "image": "🍗", "ingredients": [{"name": "닭가슴살", "amount": "200g", "owned": True}, {"name": "타임", "amount": "2줄기", "owned": True}, {"name": "버터", "amount": "20g", "owned": True}, {"name": "레몬", "amount": "1/2개", "owned": True}, {"name": "아스파라거스", "amount": "4대", "owned": False}], "steps": ["닭가슴살에 소금, 후추, 타임을 뿌린다", "팬에 버터를 녹여 닭가슴살을 굽는다", "레몬즙을 뿌린다", "아스파라거스를 함께 구워 곁들인다"], "buy_link": "https://www.coupang.com/np/search?q=아스파라거스"},
        "paprika":   {"name": "파프리카 치킨 카츠", "cuisine": "일본", "country": "일본", "image": "🍖", "ingredients": [{"name": "닭가슴살", "amount": "200g", "owned": True}, {"name": "파프리카 가루", "amount": "1T", "owned": True}, {"name": "빵가루", "amount": "1컵", "owned": False}, {"name": "계란", "amount": "1개", "owned": True}, {"name": "돈까스소스", "amount": "3T", "owned": False}], "steps": ["닭가슴살을 얇게 편다", "소금, 후추, 파프리카 가루로 밑간한다", "밀가루 → 계란 → 빵가루 순으로 튀김옷을 입힌다", "170°C 기름에서 노릇하게 튀긴다", "돈까스소스를 뿌려 완성"], "buy_link": "https://www.coupang.com/np/search?q=빵가루+돈까스소스"},
        "cumin":     {"name": "큐민 치킨 커리", "cuisine": "인도", "country": "인도", "image": "🍛", "ingredients": [{"name": "닭가슴살", "amount": "200g", "owned": True}, {"name": "큐민", "amount": "1t", "owned": True}, {"name": "카레가루", "amount": "2T", "owned": True}, {"name": "코코넛밀크", "amount": "1캔", "owned": False}, {"name": "양파", "amount": "1개", "owned": True}], "steps": ["양파를 다져 볶는다", "닭가슴살을 넣고 볶는다", "카레가루와 큐민을 넣는다", "코코넛밀크를 붓고 15분간 끓인다", "밥과 함께 서브"], "buy_link": "https://www.coupang.com/np/search?q=코코넛밀크"},
        "coriander": {"name": "고수 치킨 라이스", "cuisine": "베트남", "country": "베트남", "image": "🍚", "ingredients": [{"name": "닭가슴살", "amount": "150g", "owned": True}, {"name": "고수", "amount": "1줌", "owned": True}, {"name": "쌀", "amount": "1컵", "owned": True}, {"name": "누크맘", "amount": "2T", "owned": False}, {"name": "오이", "amount": "1/2개", "owned": False}], "steps": ["쌀을 지어 밥을 만든다", "닭가슴살을 삶아 찢는다", "누크맘 소스를 만든다", "밥 위에 닭고기, 오이, 고수를 올린다", "소스를 뿌려 완성"], "buy_link": "https://www.coupang.com/np/search?q=누크맘+오이"},
    },
    "beef": {
        "basil":     {"name": "바질 비프 스테이크", "cuisine": "이탈리아", "country": "이탈리아", "image": "🥩", "ingredients": [{"name": "소고기 등심", "amount": "200g", "owned": True}, {"name": "바질", "amount": "5잎", "owned": True}, {"name": "버터", "amount": "20g", "owned": True}, {"name": "마늘", "amount": "3쪽", "owned": True}, {"name": "발사믹 식초", "amount": "1T", "owned": False}], "steps": ["소고기를 실온에 30분 둔다", "팬을 강불로 달구고 버터를 녹인다", "스테이크를 앞뒤 3분씩 굽는다", "마늘과 바질을 넣어 향을 입힌다", "발사믹 식초를 뿌려 완성"], "buy_link": "https://www.coupang.com/np/search?q=발사믹식초"},
        "oregano":   {"name": "오레가노 비프 타코", "cuisine": "멕시코", "country": "멕시코", "image": "🌮", "ingredients": [{"name": "소고기", "amount": "200g", "owned": True}, {"name": "오레가노", "amount": "1t", "owned": True}, {"name": "타코 쉘", "amount": "4개", "owned": False}, {"name": "아보카도", "amount": "1개", "owned": False}, {"name": "라임", "amount": "1개", "owned": True}], "steps": ["소고기를 얇게 썰어 양념한다", "팬에 볶는다", "타코 쉘을 데운다", "아보카도를 으깬다", "쉘에 고기, 과카몰리, 라임을 올린다"], "buy_link": "https://www.coupang.com/np/search?q=타코쉘+아보카도"},
        "thyme":     {"name": "타임 비프 스튜", "cuisine": "프랑스", "country": "프랑스", "image": "🍲", "ingredients": [{"name": "소고기", "amount": "300g", "owned": True}, {"name": "타임", "amount": "3줄기", "owned": True}, {"name": "레드와인", "amount": "1컵", "owned": False}, {"name": "당근", "amount": "1개", "owned": True}, {"name": "양송이", "amount": "6개", "owned": False}], "steps": ["소고기를 큼직하게 썬다", "고기 겉면을 굽는다", "레드와인, 물, 타임을 넣는다", "약불에서 1시간 끓인다", "당근, 양송이를 넣고 20분 더 끓인다"], "buy_link": "https://www.coupang.com/np/search?q=레드와인+양송이"},
        "paprika":   {"name": "파프리카 비프 스트로가노프", "cuisine": "러시아", "country": "러시아", "image": "🍛", "ingredients": [{"name": "소고기", "amount": "200g", "owned": True}, {"name": "파프리카 가루", "amount": "1T", "owned": True}, {"name": "생크림", "amount": "1/2컵", "owned": False}, {"name": "양파", "amount": "1개", "owned": True}, {"name": "버섯", "amount": "100g", "owned": False}], "steps": ["소고기를 채썬다", "양파와 버섯을 볶는다", "파프리카 가루를 넣는다", "생크림을 붓고 5분간 졸인다", "밥과 함께 서브"], "buy_link": "https://www.coupang.com/np/search?q=생크림+버섯"},
        "cumin":     {"name": "큐민 비프 케밥", "cuisine": "터키", "country": "터키", "image": "🥙", "ingredients": [{"name": "소고기", "amount": "250g", "owned": True}, {"name": "큐민", "amount": "1t", "owned": True}, {"name": "또띠아", "amount": "4장", "owned": False}, {"name": "요거트", "amount": "1/2컵", "owned": True}, {"name": "양상추", "amount": "4장", "owned": False}], "steps": ["소고기를 얇게 썬다", "큐민, 소금, 후추로 밑간한다", "센 불에 고기를 굽는다", "또띠아에 양상추, 고기, 요거트를 올린다", "돌돌 말아 완성"], "buy_link": "https://www.coupang.com/np/search?q=또띠아+양상추"},
        "coriander": {"name": "고수 비프 쌀국수", "cuisine": "베트남", "country": "베트남", "image": "🍜", "ingredients": [{"name": "소고기", "amount": "150g", "owned": True}, {"name": "고수", "amount": "1줌", "owned": True}, {"name": "쌀국수", "amount": "200g", "owned": False}, {"name": "숙주", "amount": "100g", "owned": False}, {"name": "라임", "amount": "1개", "owned": True}], "steps": ["쌀국수를 삶는다", "소고기를 얇게 썬다", "육수를 끓인다", "그릇에 쌀국수, 고기, 숙주, 고수를 담는다", "뜨거운 육수를 붓고 라임을 짠다"], "buy_link": "https://www.coupang.com/np/search?q=쌀국수+숙주"},
    },
    "pork": {
        "basil":     {"name": "바질 돼지고기 케밥", "cuisine": "터키", "country": "터키", "image": "🥙", "ingredients": [{"name": "돼지고기", "amount": "300g", "owned": True}, {"name": "바질", "amount": "1줌", "owned": True}, {"name": "또띠아", "amount": "4장", "owned": False}, {"name": "요거트", "amount": "1/2컵", "owned": True}, {"name": "양상추", "amount": "4장", "owned": False}], "steps": ["돼지고기를 얇게 썰어 밑간한다", "센 불로 고기를 익힌다", "또띠아를 데운다", "또띠아에 양상추, 고기, 요거트를 올린다", "돌돌 말아 완성"], "buy_link": "https://www.coupang.com/np/search?q=또띠아+양상추"},
        "oregano":   {"name": "오레가노 포크 스튜", "cuisine": "이탈리아", "country": "이탈리아", "image": "🍲", "ingredients": [{"name": "돼지고기", "amount": "400g", "owned": True}, {"name": "오레가노", "amount": "1T", "owned": True}, {"name": "토마토캔", "amount": "1캔", "owned": False}, {"name": "당근", "amount": "1개", "owned": True}, {"name": "셀러리", "amount": "1대", "owned": False}], "steps": ["돼지고기를 큼직하게 썬다", "냄비에 올리브오일을 두르고 고기를 굽는다", "당근, 셀러리를 넣고 볶는다", "토마토캔과 오레가노를 넣고 40분간 끓인다", "소금, 후추로 간을 맞춘다"], "buy_link": "https://www.coupang.com/np/search?q=토마토캔+셀러리"},
        "thyme":     {"name": "타임 돼지고기 구이", "cuisine": "프랑스", "country": "프랑스", "image": "🥩", "ingredients": [{"name": "돼지목살", "amount": "2장", "owned": True}, {"name": "타임", "amount": "3줄기", "owned": True}, {"name": "꿀", "amount": "1T", "owned": True}, {"name": "디종 머스타드", "amount": "1T", "owned": False}, {"name": "아스파라거스", "amount": "6대", "owned": False}], "steps": ["꿀, 머스타드, 타임을 섞는다", "돼지목살에 소스를 바른다", "그릴 팬에 앞뒤 4분씩 굽는다", "아스파라거스를 함께 굽는다", "접시에 담아 완성"], "buy_link": "https://www.coupang.com/np/search?q=디종머스타드+아스파라거스"},
        "paprika":   {"name": "파프리카 제육볶음", "cuisine": "한국", "country": "한국", "image": "🥘", "ingredients": [{"name": "돼지고기", "amount": "300g", "owned": True}, {"name": "파프리카 가루", "amount": "1T", "owned": True}, {"name": "고추장", "amount": "2T", "owned": True}, {"name": "양파", "amount": "1개", "owned": True}, {"name": "대파", "amount": "1대", "owned": True}], "steps": ["돼지고기를 얇게 썬다", "고추장, 파프리카 가루, 다진 마늘로 양념한다", "팬에 양파와 함께 볶는다", "대파를 넣고 마무리", "밥과 함께 서브"], "buy_link": "https://www.coupang.com/np/search?q=고추장+대파"},
        "cumin":     {"name": "큐민 돼지고기 볶음", "cuisine": "중국", "country": "중국", "image": "🥘", "ingredients": [{"name": "돼지고기", "amount": "250g", "owned": True}, {"name": "큐민", "amount": "1T", "owned": True}, {"name": "굴소스", "amount": "1T", "owned": False}, {"name": "청양고추", "amount": "3개", "owned": True}, {"name": "마늘", "amount": "4쪽", "owned": True}], "steps": ["돼지고기를 얇게 썬다", "팬에 기름을 두르고 마늘을 볶는다", "돼지고기를 넣고 센 불로 볶는다", "큐민, 굴소스를 넣는다", "청양고추를 넣고 마무리"], "buy_link": "https://www.coupang.com/np/search?q=굴소스"},
        "coriander": {"name": "고수 돼지고기 완자", "cuisine": "베트남", "country": "베트남", "image": "🧆", "ingredients": [{"name": "돼지고기 다짐", "amount": "300g", "owned": True}, {"name": "고수", "amount": "1줌", "owned": True}, {"name": "어장", "amount": "1T", "owned": False}, {"name": "마늘", "amount": "3쪽", "owned": True}, {"name": "양파", "amount": "1/2개", "owned": True}], "steps": ["양파를 다진다", "다짐육, 고수, 어장, 마늘을 섞는다", "완자를 빚는다", "팬에 노릇하게 굽는다", "접시에 담아 완성"], "buy_link": "https://www.coupang.com/np/search?q=어장"},
    },
    "shrimp": {
        "basil":     {"name": "바질 새우 빠에야", "cuisine": "스페인", "country": "스페인", "image": "🥘", "ingredients": [{"name": "새우", "amount": "8마리", "owned": True}, {"name": "바질", "amount": "1줌", "owned": True}, {"name": "쌀", "amount": "1컵", "owned": True}, {"name": "사프란", "amount": "1꼬집", "owned": False}, {"name": "홍합", "amount": "10개", "owned": False}], "steps": ["팬에 올리브오일을 두르고 새우를 익힌다", "쌀을 넣고 투명해질 때까지 볶는다", "물 2컵과 사프란을 넣는다", "뚜껑을 덮고 20분간 익힌다", "홍합과 바질을 올린다"], "buy_link": "https://www.coupang.com/np/search?q=사프란+홍합"},
        "oregano":   {"name": "오레가노 새우 파스타", "cuisine": "이탈리아", "country": "이탈리아", "image": "🍝", "ingredients": [{"name": "새우", "amount": "10마리", "owned": True}, {"name": "오레가노", "amount": "1T", "owned": True}, {"name": "스파게티면", "amount": "200g", "owned": True}, {"name": "화이트와인", "amount": "1/2컵", "owned": False}, {"name": "마늘", "amount": "4쪽", "owned": True}], "steps": ["스파게티면을 삶는다", "팬에 올리브오일과 마늘을 볶는다", "새우를 넣고 익힌다", "화이트와인과 오레가노를 넣는다", "면을 버무려 완성"], "buy_link": "https://www.coupang.com/np/search?q=화이트와인"},
        "thyme":     {"name": "타임 새우 구이", "cuisine": "프랑스", "country": "프랑스", "image": "🦐", "ingredients": [{"name": "새우", "amount": "12마리", "owned": True}, {"name": "타임", "amount": "2줄기", "owned": True}, {"name": "레몬", "amount": "1개", "owned": True}, {"name": "버터", "amount": "20g", "owned": True}, {"name": "마늘", "amount": "3쪽", "owned": True}], "steps": ["새우를 손질한다", "버터, 다진 마늘, 타임을 팬에 녹인다", "새우를 넣고 2분간 굽는다", "레몬즙을 뿌린다", "접시에 담아 완성"], "buy_link": "https://www.coupang.com/np/search?q=레몬"},
        "paprika":   {"name": "파프리카 새우 커리", "cuisine": "인도", "country": "인도", "image": "🍛", "ingredients": [{"name": "새우", "amount": "10마리", "owned": True}, {"name": "파프리카 가루", "amount": "1T", "owned": True}, {"name": "코코넛밀크", "amount": "1캔", "owned": False}, {"name": "카레가루", "amount": "2T", "owned": True}, {"name": "양파", "amount": "1개", "owned": True}], "steps": ["양파를 다져 볶는다", "카레가루와 파프리카를 넣는다", "코코넛밀크를 붓고 10분간 끓인다", "새우를 넣고 3분간 익힌다", "밥과 함께 서브"], "buy_link": "https://www.coupang.com/np/search?q=코코넛밀크"},
        "cumin":     {"name": "큐민 새우 꼬치", "cuisine": "중동", "country": "모로코", "image": "🦐", "ingredients": [{"name": "새우", "amount": "12마리", "owned": True}, {"name": "큐민", "amount": "1t", "owned": True}, {"name": "올리브오일", "amount": "2T", "owned": False}, {"name": "레몬", "amount": "1개", "owned": True}, {"name": "파프리카", "amount": "1개", "owned": True}], "steps": ["새우를 손질한다", "올리브오일, 큐민, 레몬즙을 섞어 마리네이드 만든다", "새우를 15분 재운다", "꼬치에 새우와 파프리카를 끼운다", "그릴에 구워 완성"], "buy_link": "https://www.coupang.com/np/search?q=올리브오일"},
        "coriander": {"name": "고수 새우 샐러드", "cuisine": "태국", "country": "태국", "image": "🥗", "ingredients": [{"name": "새우", "amount": "10마리", "owned": True}, {"name": "고수", "amount": "1줌", "owned": True}, {"name": "라임", "amount": "1개", "owned": False}, {"name": "어장", "amount": "1T", "owned": False}, {"name": "청양고추", "amount": "2개", "owned": True}], "steps": ["새우를 삶는다", "라임즙, 어장, 다진 고추로 드레싱 만든다", "새우, 고수, 드레싱을 버무린다", "접시에 담아 완성"], "buy_link": "https://www.coupang.com/np/search?q=라임+어장"},
    },
    "fish": {
        "basil":     {"name": "바질 생선 구이", "cuisine": "지중해", "country": "그리스", "image": "🐟", "ingredients": [{"name": "생선", "amount": "1마리", "owned": True}, {"name": "바질", "amount": "1줌", "owned": True}, {"name": "올리브오일", "amount": "2T", "owned": False}, {"name": "레몬", "amount": "1개", "owned": True}, {"name": "방울토마토", "amount": "6개", "owned": False}], "steps": ["생선을 손질한다", "올리브오일, 레몬즙, 바질을 뿌린다", "오븐 180°C에서 20분간 굽는다", "방울토마토를 곁들인다"], "buy_link": "https://www.coupang.com/np/search?q=올리브오일+방울토마토"},
        "oregano":   {"name": "오레가노 생선 스테이크", "cuisine": "이탈리아", "country": "이탈리아", "image": "🐟", "ingredients": [{"name": "생선", "amount": "1마리", "owned": True}, {"name": "오레가노", "amount": "1T", "owned": True}, {"name": "올리브오일", "amount": "2T", "owned": False}, {"name": "마늘", "amount": "3쪽", "owned": True}, {"name": "레몬", "amount": "1/2개", "owned": True}], "steps": ["생선에 소금, 후추, 오레가노를 뿌린다", "팬에 올리브오일과 마늘을 두른다", "생선을 앞뒤로 구워 익힌다", "레몬즙을 뿌려 완성"], "buy_link": "https://www.coupang.com/np/search?q=올리브오일"},
        "thyme":     {"name": "타임 생선 파피요트", "cuisine": "프랑스", "country": "프랑스", "image": "🐟", "ingredients": [{"name": "생선", "amount": "1마리", "owned": True}, {"name": "타임", "amount": "3줄기", "owned": True}, {"name": "버터", "amount": "20g", "owned": True}, {"name": "레몬", "amount": "1/2개", "owned": True}, {"name": "양파", "amount": "1/2개", "owned": True}], "steps": ["생선을 손질한다", "호일 위에 생선, 타임, 버터, 양파를 올린다", "레몬 슬라이스를 올린다", "호일로 감싸 오븐 180°C에서 25분간 굽는다"], "buy_link": "https://www.coupang.com/np/search?q=버터"},
        "paprika":   {"name": "파프리카 생선 튀김", "cuisine": "한국", "country": "한국", "image": "🐟", "ingredients": [{"name": "생선", "amount": "2마리", "owned": True}, {"name": "파프리카 가루", "amount": "1T", "owned": True}, {"name": "튀김가루", "amount": "1컵", "owned": False}, {"name": "레몬", "amount": "1/2개", "owned": True}, {"name": "타르타르소스", "amount": "3T", "owned": False}], "steps": ["생선을 손질한다", "튀김가루에 파프리카 가루를 섞는다", "생선에 튀김옷을 입힌다", "170°C 기름에서 노릇하게 튀긴다", "레몬과 타르타르소스를 곁들인다"], "buy_link": "https://www.coupang.com/np/search?q=튀김가루+타르타르소스"},
        "cumin":     {"name": "큐민 생선 커리", "cuisine": "인도", "country": "인도", "image": "🍛", "ingredients": [{"name": "생선", "amount": "1마리", "owned": True}, {"name": "큐민", "amount": "1t", "owned": True}, {"name": "카레가루", "amount": "2T", "owned": True}, {"name": "코코넛밀크", "amount": "1/2캔", "owned": False}, {"name": "토마토", "amount": "1개", "owned": True}], "steps": ["생선을 큼직하게 썬다", "팬에 양파와 토마토를 볶는다", "카레가루와 큐민을 넣는다", "코코넛밀크를 붓고 10분간 끓인다", "생선을 넣고 5분간 익힌다"], "buy_link": "https://www.coupang.com/np/search?q=코코넛밀크"},
        "coriander": {"name": "고수 생선찜", "cuisine": "중국", "country": "중국", "image": "🐟", "ingredients": [{"name": "생선", "amount": "1마리", "owned": True}, {"name": "고수", "amount": "1줌", "owned": True}, {"name": "간장", "amount": "2T", "owned": True}, {"name": "생강", "amount": "1쪽", "owned": False}, {"name": "대파", "amount": "1대", "owned": True}], "steps": ["생선을 손질한다", "찜기에 생선, 생강, 대파를 올린다", "10분간 찐다", "간장을 끼얹는다", "고수를 올려 완성"], "buy_link": "https://www.coupang.com/np/search?q=생강"},
    },
}


def get_weekdays():
    """Return weekday labels starting from Wednesday."""
    today = date.today()
    # Find the upcoming Wednesday
    days_until_wed = (2 - today.weekday()) % 7
    wed = today + timedelta(days=days_until_wed)
    weekdays = []
    for i in range(5):
        d = wed + timedelta(days=i)
        weekdays.append({
            "day": ["수", "목", "금", "토", "일"][i],
            "date": d.strftime("%m/%d"),
        })
    return weekdays


# ── Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", meats=MEATS, spices=SPICES)


@app.route("/menu")
def menu():
    meat = request.args.get("meat", "drumstick")
    spice = request.args.get("spice", "basil")

    # Get the matching recipe
    main_recipe = RECIPES.get(meat, {}).get(spice)

    if not main_recipe:
        # Fallback
        main_recipe = RECIPES["drumstick"]["basil"]

    # Generate 5 recipes for the week (mix of matching and related)
    all_recipes = []
    for m in MEATS:
        for s in SPICES:
            r = RECIPES[m][s]
            all_recipes.append({"meat_key": m, "spice_key": s, **r})

    # First recipe is always the match, then 4 random others
    random.seed(f"{meat}{spice}")  # deterministic for the same inputs
    others = [r for r in all_recipes if r["meat_key"] != meat or r["spice_key"] != spice]
    random.shuffle(others)
    selected = [{"meat_key": meat, "spice_key": spice, **main_recipe}] + others[:4]

    weekdays = get_weekdays()
    daily_menu = []
    for i, recipe in enumerate(selected):
        daily_menu.append({**weekdays[i], **recipe})

    return render_template(
        "menu.html",
        daily_menu=daily_menu,
        meats=MEATS,
        spices=SPICES,
        selected_meat=meat,
        selected_spice=spice,
    )


@app.route("/recipe/<meat>/<spice>")
def recipe_detail(meat, spice):
    recipe = RECIPES.get(meat, {}).get(spice)

    if not recipe:
        return "Recipe not found", 404

    return render_template(
        "recipe.html",
        recipe=recipe,
        meat=MEATS[meat],
        spice=SPICES[spice],
        meat_key=meat,
        spice_key=spice,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5050)
