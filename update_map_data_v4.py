
import re
import json
import random

# --- CONFIG ---
MD_FILE = '/Users/dxx/Coding/travelling/美食.md'
HTML_FILE = '/Users/dxx/Coding/travelling/food_map.html'

# --- DATA ---
DISTRICT_COORDS = {
    # HK
    "尖沙咀": [22.2988, 114.1722],
    "旺角": [22.3193, 114.1694],
    "中环": [22.2819, 114.1581],
    "铜锣湾": [22.2804, 114.1857],
    "湾仔": [22.2760, 114.1751],
    "油麻地": [22.3134, 114.1705],
    "庙街": [22.3094, 114.1702],
    "深水埗": [22.3307, 114.1622],
    "沙田": [22.3813, 114.1945],
    "红磡": [22.3032, 114.1856],
    "上环": [22.2867, 114.1508],
    "佐敦": [22.3040, 114.1712],
    "西营盘": [22.2858, 114.1428],
    "北角": [22.2922, 114.2005],
    "天后": [22.2825, 114.1915],
    "大角咀": [22.3214, 114.1614],
    "西环": [22.2858, 114.1428],
    "火炭": [22.3956, 114.1963],
    # GZ
    "西华路": [23.1315, 113.2455],
    "上下九": [23.1165, 113.2483],
    "文明路": [23.1256, 113.2750],
    "珠江新城": [23.1182, 113.3256],
    "天河": [23.1248, 113.3600],
    "越秀": [23.1310, 113.2700],
    "海珠": [23.0900, 113.2700],
    "荔湾": [23.1100, 113.2300],
    "番禺": [22.9500, 113.3500],
}
DEFAULT_HK = [22.3193, 114.1694]
DEFAULT_GZ = [23.1291, 113.2644]

# --- PREDEFINED LOCATIONS (Best Branches) ---
# Coordinates from Google Maps / Amap
PREDEFINED_LOCATIONS = {
    # --- Hong Kong ---
    "华星冰室": [22.2775, 114.1782], # 湾仔总店
    "金华冰厅": [22.3228, 114.1691], # 旺角
    "翠华餐厅": [22.2818, 114.1555], # 中环威灵顿街 (Flagship used to be there, now use TST?) Use Central or TST. Let's use Causeway Bay (Sugar St) or TST. Let's use TST Carnarvon Rd: [22.2982, 114.1738]
    "食光榮": [22.3180, 114.1700], # Mong Kok approximate
    "金禾阁": [22.3813, 114.1945], # Sha Tin
    "美好快餐": [22.3813, 114.1945], # Sha Tin
    "源记": [22.2988, 114.1722], # TST
    "佳记餐厅": [22.2988, 114.1722], # TST approximate
    "泰昌饼家": [22.2825, 114.1539], # Central, Lyndhurst Terrace
    "瑞记": [22.2850, 114.1500], # Sheung Wan Market?
    "科记咖啡餐厅": [22.2868, 114.1486], # Sheung Wan
    "金凤茶餐厅": [22.2751, 114.1728], # Wan Chai, Spring Garden Lane
    "兰芳园": [22.2828, 114.1540], # Central, Gage St (Original)
    "新香园": [22.3300, 114.1610], # Sham Shui Po, Kweilin St
    "利苑酒家": [22.2798, 114.1789], # Wan Chai (Example)
    "荣记饭店": [22.2783, 114.1802], # Bowrington Road Market
    "莲香居": [22.2882, 114.1448], # Sheung Wan
    "稻香": [22.3956, 114.1963], # Fo Tan
    "端记茶楼": [22.3900, 114.1100], # Tai Mo Shan (approx)
    "莲香楼": [22.2842, 114.1538], # Central (Closed? Reopened?) Use approx
    "牛阵": [22.2800, 114.1800], # Generic
    "源記甜品": [22.2861, 114.1408], # Sai Ying Pun
    "佳佳甜品": [22.3056, 114.1690], # Jordan, Ning Po St
    "福元湯圓": [22.2885, 114.1932], # North Point
    "北角雞蛋仔": [22.2918, 114.2008], # North Point
    "沾仔記雲吞麵": [22.3214, 114.1614], # Tai Kok Tsui (or Central)
    "廟街興記": [22.3094, 114.1702], # Temple St
    "華香園": [22.2974, 114.1691], # Haiphong Rd, TST
    "媽咪雞蛋仔": [22.2980, 114.1730], # TST (Chain)
    "合香園": [22.2800, 114.1500], # Central?
    "德發牛丸": [22.2980, 114.1720], # TST
    "水記牛腩": [22.2840, 114.1540], # Central
    "生记": [22.2860, 114.1510], # Sheung Wan
    "荣记粉面": [22.2804, 114.1857], # CWB
    "文记": [22.3032, 114.1856], # Hung Hom
    "kabo": [22.2980, 114.1720], # TST
    "英记面家": [22.2858, 114.1428], # Sai Ying Pun
    "达濠仔": [22.3200, 114.1600], # GZ or HK?
    "卖奀记忠记": [22.2820, 114.1550], # Central
    "生记粥铺": [22.2860, 114.1510], # Sheung Wan
    "蛇王芬": [22.2840, 114.1540], # Central
    "面尊": [22.2804, 114.1857], # CWB
    "华姐清汤腩": [22.2825, 114.1915], # Tin Hau
    "乐园鱼蛋粉": [22.2804, 114.1857], # CWB?
    "庙街牛什": [22.3094, 114.1702], # Temple St
    "红磡鸡蛋仔": [22.3032, 114.1856], # Hung Hom
    "兴记": [22.3094, 114.1702],
    "新兴食家": [22.2858, 114.1428], # Sai Ying Pun
    "bakehouse": [22.2985, 114.1735], # TST (Hankow Rd)
    "vission bakery": [22.2820, 114.1545], # Central (Staunton St)
    "owls choux": [22.2980, 114.1720], # TST
    "shari shari kakigori house冰屋": [22.2804, 114.1857], # CWB / Central
    "tokachi-milky": [22.2980, 114.1720],
    "棋哥": [22.2800, 114.1800],
    "翠园": [22.2950, 114.1690],
    "甘堂": [22.2820, 114.1550], # Yung Kee branch? Kam's Roast is 22.2783, 114.1758 (Wan Chai)
    "一乐": [22.2824, 114.1558], # Central, Stanley St
    "鏞記酒家": [22.2818, 114.1552], # Central, Wellington St
    "新桂香": [22.2700, 114.2380], # Chai Wan
    "香港避风塘兴记": [22.2980, 114.1720], # TST
    "国金轩": [22.2950, 114.1700], # TST / Central
    "疍家菜": [22.2800, 114.1800],
    "海港荟": [22.2950, 114.1700], # Peking Rd, TST
    "驹记海鲜大排档": [22.2810, 114.1810], # Wan Chai
    "喜记避风塘炒蟹": [22.2805, 114.1820], # Wan Chai / CWB
    "旺角果栏": [22.3130, 114.1680], # Yau Ma Tei
    
    # --- Guangzhou ---
    "对面的糊天甜品": [23.1315, 113.2455],
    "兰芳园(GZ)": [23.1310, 113.2450],
    "沙湾甜品": [23.1315, 113.2455],
    "南信": [23.1165, 113.2483], # Shangxiajiu
    "开记": [23.1165, 113.2483], # Shangxiajiu
    "百花甜品": [23.1256, 113.2750], # Wenming Rd
    "玫瑰甜品": [23.1256, 113.2752], # Wenming Rd
    "梁阿珍": [23.1250, 113.2750],
    "清润坊": [23.1250, 113.2750],
    "合众肠粉店": [23.1250, 113.2440], # Longjin Rd
    "炜明肠粉店": [23.1280, 113.2480], # Chen Clan Academy
    "合兴小食店": [23.1315, 113.2455], # Xihua Rd
    "德记": [23.1200, 113.2500],
    "源记肠粉": [23.1250, 113.2400], # Huagui Rd
    "穗银肠粉": [23.1240, 113.2840], # Dongchuan Rd
    "顺势牛杂汤": [23.1330, 113.2460],
    "一品为先食得好": [23.1315, 113.2455],
    "西关牛杂": [23.1315, 113.2455],
    "南信(GZ)": [23.1165, 113.2483],
    "达扬炖品": [23.1256, 113.2750], # Wenming Rd
    "炳胜品味": [23.1182, 113.3256], # Zhujiang New Town
    "同发号百年老店": [23.1200, 113.2500],
    "万年胜记酒楼": [23.1200, 113.2500],
    "信记": [23.1130, 113.2600], # Changdi
    "森焱食馆": [23.0950, 113.2550], # Tongfu West
    "广州酒家": [23.1168, 113.2460], # Wenchang South
    "梁家菜馆": [23.1200, 113.2500],
    "壹厨饭店": [23.1250, 113.2780], # Dezheng Middle
    "醉贤居": [23.1250, 113.2780],
    "肥姐美食": [23.0950, 113.2550], # Tongfu
    "多福美食馆": [23.1350, 113.2800], # Sima St
    "贰少品味": [23.0950, 113.2550], # Tongfu Middle
    "众源美食": [23.1260, 113.2480], # Guangfu North
    "同乐居菜馆": [23.1250, 113.2550], # Huifu West
    "惠食佳": [23.1070, 113.2650], # Binjiang
    "白天鹅玉堂春暖": [23.1075, 113.2386], # Shamian
    "广州宾馆": [23.1180, 113.2630], # Haizhu Square
    "宝汉酒家": [23.1260, 113.2320], # Zhongshan 8
    "荣华楼": [23.1210, 113.2430], # Longjin East
    "陶然轩": [23.1090, 113.2980], # Ersha Island
    "御宝轩": [23.1170, 113.3280], # igc
    "喜势点茶居": [23.1200, 113.2600],
    "新文记": [23.1050, 113.2660], # Shi Er Gong
    "煲笼兴": [23.1050, 113.2660],
    "丽的面家": [23.1250, 113.2800], # Xiaobei? No, Duobao Rd
    "吴财记": [23.1150, 113.2450], # Dadong Rd
    "恩宁刘福记": [23.1150, 113.2360], # Enning Rd
    "旺记烧腊": [23.1220, 113.2380], # Fengyuan Rd
    "永兴烧腊": [23.1100, 113.2500],
    "立庆坊": [23.1200, 113.2500],
    "惠来": [23.1300, 113.2400], # Longgang Rd
    "云浮烧鸭": [23.1400, 113.2300], # E Zhang Tan
    "森成美食店": [23.1050, 113.2500], # Nanhua West
    "金辉食馆": [23.1000, 113.2600], # Tongfu Middle
    "喜盈酒家": [23.1000, 113.2600],
    "旺金鸽": [23.1200, 113.3200],
    "鸽皇农庄": [23.1800, 113.3400], # Changban
    "悦宴酒家": [23.1900, 113.3500], # Longdong
    "顺得来": [23.1270, 113.2680], # Mayflower
    "伍湛记粥品专家": [23.1200, 113.2400],
    "标记美食": [23.1200, 113.2400],
    "德记猪肝粥": [23.1200, 113.2400],
    "御手信": [23.1280, 113.2780], # China Plaza
}

# --- SUPPLEMENTARY DATA (Merged) ---
SUPPLEMENTS = {
    # HK
    "华星冰室": {"dishes": "炒蛋多士, 奶茶", "note": "陈奕迅常去"},
    "金华冰厅": {"dishes": "菠萝油(必点), 冻奶茶", "note": "菠萝油全港第一"},
    "翠华餐厅": {"dishes": "奶油猪, 鱼蛋粉, 咖喱牛腩", "note": "连锁店, 品质稳定"},
    "兰芳园": {"dishes": "丝袜奶茶, 猪扒包", "note": "丝袜奶茶始祖"},
    "澳洲牛奶公司": {"dishes": "炒蛋, 炖奶", "note": "翻台快, 服务有特色"},
    "九记牛腩": {"dishes": "上汤牛腩", "note": "常年排队, 只收现金"},
    "Bakehouse": {"dishes": "Sourdough Egg Tart (酸种蛋挞)", "note": "需早去"},
    "Vission Bakery": {"dishes": "Matcha Mochi, Tiramisu Danish", "note": "排队王"},
    "Hashtag B": {"dishes": "拿破仑蛋挞", "note": "热门打卡"},
    # GZ
    "白天鹅玉堂春暖": {"dishes": "虾饺, 萨其马", "note": "米其林一星"},
    "广州酒家": {"dishes": "文昌鸡, 虾饺", "note": "老字号"},
    "广州宾馆": {"dishes": "得云宫早茶", "note": "视野好"},
    "陶然轩": {"dishes": "手工点心", "note": "二沙岛风景好"},
    "御宝轩": {"dishes": "糯米饭, 金网脆皮虾肠", "note": "米其林二星, 需预约"},
    "荣华楼": {"dishes": "虾饺, 凤爪", "note": "百年老字号, 有粤剧听"},
    "点都德": {"dishes": "金莎红米肠", "note": "连锁很多"},
    "炳胜品味": {"dishes": "脆皮叉烧, 菠萝包", "note": "黑珍珠"},
    "惠食佳": {"dishes": "啫啫煲, 皇上皇腊味饭", "note": "谢霆锋推荐"},
}

def get_coord(name, text, city):
    # 1. Check Predefined
    key = name.lower()
    for k, v in PREDEFINED_LOCATIONS.items():
        if k.lower() in key or key in k.lower():
            return v
            
    # 2. Check District
    base = DEFAULT_HK if city == "hk" else DEFAULT_GZ
    for d, c in DISTRICT_COORDS.items():
        if d in text:
            base = c
            break
            
    # Random Jitter (approx 50-100m)
    lat = base[0] + (random.random() - 0.5) * 0.003
    lng = base[1] + (random.random() - 0.5) * 0.003
    return round(lat, 5), round(lng, 5)

def parse_line_improved(line):
    # Rule: 1. Name (Location) Rest OR 1. Name, Rest OR 1. Name Space Rest
    clean = re.sub(r'^\d+\.\s*', '', line).strip()
    if not clean: return None, None, None
    
    name, loc, rest = "", "", ""
    
    match_br = re.match(r"^([^\(（]+)[\(（]([^\)）]+)[\)）](.*)", clean)
    
    if match_br:
        name = match_br.group(1).strip()
        loc = match_br.group(2).strip()
        rest = match_br.group(3).strip()
    else:
        if '，' in clean:
            parts = clean.split('，', 1)
            name = parts[0].strip()
            rest = parts[1].strip()
        elif ',' in clean:
            parts = clean.split(',', 1)
            name = parts[0].strip()
            rest = parts[1].strip()
        elif ' ' in clean:
            parts = clean.split(' ', 1)
            name = parts[0].strip()
            rest = parts[1].strip()
        else:
            name = clean
            
    return name, loc, rest

def parse_hk_baking(line):
    clean = re.sub(r'^\d+\.\s*', '', line).strip()
    match = re.match(r"^([a-zA-Z\s\-\.]+)(.*)", clean)
    if match:
        name = match.group(1).strip()
        rest = match.group(2).strip()
        return name, "", rest
    
    return parse_line_improved(line)

def determine_type_hk(title):
    m = {
        "茶餐厅": "茶餐厅", "家常": "正餐", "糖水": "糖水", "小吃": "小吃",
        "烘焙": "烘焙", "烧味": "烧腊", "海鲜等": "海鲜"
    }
    return m.get(title, "其他")

def process_md():
    with open(MD_FILE, 'r', encoding='utf-8') as f: lines = f.readlines()
    
    items = []
    mode = None 
    current_cat = "其他"
    WARNINGS = ["只收现金", "现金", "排队", "服务", "态度", "预约", "开门", "黑脸", "难吃", "贵", "低消"]
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if "### **广州**" in line: mode = 'gz'; continue
        if "### **香港**" in line: mode = 'hk'; continue
        
        if line.startswith("####"):
            current_cat_raw = line.replace("####", "").replace("**", "").strip()
            if mode == 'hk': current_cat = determine_type_hk(current_cat_raw)
            else: current_cat = current_cat_raw
            continue
            
        if not line[0].isdigit(): continue 
        
        # Parse
        if mode == 'hk' and current_cat == '烘焙':
            name, loc, rest = parse_hk_baking(line)
        else:
            name, loc, rest = parse_line_improved(line)
            
        if not name: continue
        
        dishes = rest
        note_parts = []
        
        for w in WARNINGS:
            if w in rest:
                if "服务" in rest or "态度" in rest: 
                    if "差" in rest: note_parts.append("服务态度差")
                    else: note_parts.append("注意服务")
                if "排队" in rest: note_parts.append("可能排队")
                if "现金" in rest: note_parts.append("只收现金")
                if "预约" in rest: note_parts.append("需要预约")
                break 
        
        supp = SUPPLEMENTS.get(name) or {}
        if supp:
            if not dishes or len(dishes) < 2: 
                dishes = supp.get("dishes", dishes)
            if supp.get("note"):
                note_parts.append(supp.get("note"))
        
        note_str = " ".join(list(set(note_parts))) 
        
        # Coords Logic
        text_for_search = name + " " + loc + " " + rest
        lat, lng = get_coord(name, text_for_search, mode)
        
        if not loc:
            if mode == 'hk': loc = "香港"
            else: loc = "广州"
            
        items.append({
            "name": name,
            "type": current_cat,
            "lat": lat,
            "lng": lng,
            "address": loc,
            "note": note_str,
            "dishes": dishes,
            "city": mode
        })

    return items

def generate_js():
    items = process_md()
    js_data = "const placemarks = [\n"
    for item in items:
        n = item['name'].replace('"', '\\"')
        t = item['type']
        a = item['address'].replace('"', '\\"')
        nt = item['note'].replace('"', '\\"')
        d = item['dishes'].replace('"', '\\"')
        c = item['city']
        js_data += f'    {{ name: "{n}", type: "{t}", lat: {item['lat']}, lng: {item["lng"]}, address: "{a}", note: "{nt}", dishes: "{d}", city: "{c}" }},\n'
    js_data += "];"
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f: content = f.read()
    pattern = r"const placemarks = \[.*?\];"
    new_content = re.sub(pattern, js_data, content, flags=re.DOTALL)
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f: f.write(new_content)
    print(f"Updated {len(items)} items.")

if __name__ == "__main__":
    generate_js()
