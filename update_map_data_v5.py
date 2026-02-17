
import re
import json
import random

# --- CONFIG ---
MD_FILE = '/Users/dxx/Coding/travelling/美食.md'
HTML_FILE = '/Users/dxx/Coding/travelling/food_map.html'

# --- DATA ---
# This dictionary maps specific keywords (Shop Name or key part) to PRECISE [Lat, Lng]
# Google Maps / Amap High Precision Data
PREDEFINED_LOCATIONS = {
    # --- Hong Kong (Central/Sheung Wan) ---
    "兰芳园": [22.2828, 114.1540], # Central Gage St
    "泰昌饼家": [22.2825, 114.1539], # Lyndhurst Terrace
    "瑞记": [22.2858, 114.1502], # Sheung Wan Market
    "科记咖啡餐厅": [22.2868, 114.1486], # Hollywood Rd
    "莲香楼": [22.2842, 114.1538], # Wellington St
    "莲香居": [22.2882, 114.1448], # Des Voeux Rd West
    "沾仔記": [22.2818, 114.1552], # Wellington St (Tsim Chai Kee)
    "水记": [22.2841, 114.1538], # Gilman's Bazaar
    "生记粥品": [22.2863, 114.1512], # Burd Street
    "卖奀记": [22.2838, 114.1542], # Mak Item
    "蛇王芬": [22.2824, 114.1540], # Cochrane St
    "一乐": [22.2824, 114.1558], # Stanley St
    "鏞記": [22.2818, 114.1552], # Wellington St
    "Vission Bakery": [22.2820, 114.1545], # Staunton St
    "九记牛腩": [22.2841, 114.1528], # Gough St
    "Shari Shari": [22.2820, 114.1545], # Central/Soho

    # --- Hong Kong (Wan Chai / Causeway Bay) ---
    "华星冰室": [22.2775, 114.1782], # Heard St
    "金凤茶餐厅": [22.2751, 114.1728], # Spring Garden Ln
    "利苑酒家": [22.2798, 114.1789], # Hennessy Rd
    "荣记饭店": [22.2783, 114.1802], # Bowrington Rd Market
    "甘堂": [22.2783, 114.1758], # Kam's Roast Goose (Wan Chai)
    "再兴": [22.2780, 114.1765], # Joy Hing (Wan Chai)
    "荣记粉面": [22.2804, 114.1857], # Jardine's Bazaar
    "面尊": [22.2800, 114.1850], # CWB
    "乐园鱼蛋粉": [22.2804, 114.1857], # CWB
    "喜记": [22.2805, 114.1820], # Jaffe Rd
    "驹记": [22.2810, 114.1810], # Wan Chai
    "妈咪鸡蛋仔": [22.2800, 114.1830], # CWB Store
    "Hashtag B": [22.2798, 114.1820], # CWB (Lee Garden)

    # --- Hong Kong (TST / Jordan / Mong Kok / SSP) ---
    "翠华餐厅": [22.2982, 114.1738], # Carnarvon Rd (TST)
    "源记": [22.2988, 114.1722], # Granville Rd (TST)
    "佳记": [22.2988, 114.1722], # TST
    "华香园": [22.2974, 114.1691], # Haiphong Rd Temp Market
    "德发牛丸": [22.2974, 114.1691], # Haiphong Rd Temp Market
    "Bakehouse": [22.2985, 114.1735], # Hankow Rd (TST)
    "Owls Choux": [22.2980, 114.1720], # TST
    "Tokachi": [22.2980, 114.1720], # TST
    "兴记": [22.2980, 114.1720], # TST Typhoon Shelter Style
    "海港荟": [22.2950, 114.1700], # Peking Rd
    "国金轩": [22.2950, 114.1700], # The Mira
    "佳佳甜品": [22.3056, 114.1690], # Ning Po St (Jordan)
    "澳洲牛奶公司": [22.3045, 114.1705], # Parkes St (Jordan)
    "庙街兴记": [22.3094, 114.1702], # Temple St Claypot
    "庙街牛什": [22.3094, 114.1702], # Temple St
    "金华冰厅": [22.3228, 114.1691], # Bute St (Mong Kok)
    "食光荣": [22.3180, 114.1700], # Fa Yuen St (Mong Kok)
    "旺角果栏": [22.3130, 114.1680], # Yau Ma Tei
    "新香园": [22.3300, 114.1610], # Kweilin St (SSP)
    "Kabo": [22.2980, 114.1720], # TST

    # --- Hong Kong (Others) ---
    "福元汤圆": [22.2885, 114.1932], # North Point
    "北角鸡蛋仔": [22.2918, 114.2008], # North Point
    "华姐清汤腩": [22.2825, 114.1915], # Tin Hau
    "稻香": [22.3956, 114.1963], # Fo Tan
    "文记": [22.3032, 114.1856], # Hung Hom
    "红磡鸡蛋仔": [22.3032, 114.1856], # Hung Hom
    "新桂香": [22.2700, 114.2380], # Chai Wan

    # --- Guangzhou (Liwan / Xiguan) ---
    "糊天甜品": [23.1285, 113.2458], # He'an St 78
    "一品为先": [23.1288, 113.2455], # He'an St 67
    "兰芳园": [23.1310, 113.2450], # Xihua Rd 402
    "沙湾甜品": [23.1315, 113.2455], # Xihua Rd
    "合兴小食店": [23.1315, 113.2455], # Xihua Rd
    "顺势牛杂汤": [23.1330, 113.2460], # Sima Fang
    "西关牛杂": [23.1315, 113.2455], # Jinhua Zhijie
    "合众肠粉店": [23.1250, 113.2440], # Longjin Rd
    "炜明肠粉店": [23.1280, 113.2480], # Chen Clan
    "源记肠粉": [23.1250, 113.2400], # Huagui Rd
    "伍湛记": [23.1200, 113.2400], # Longjin
    "文记壹心鸡": [23.1180, 113.2430], # Baohua Rd
    "顺记冰室": [23.1190, 113.2430], # Baohua Rd
    "吴财记": [23.1150, 113.2450], # Dadong Rd
    "恩宁刘福记": [23.1150, 113.2360], # Enning Rd
    "旺记烧腊": [23.1220, 113.2380], # Fengyuan Rd
    "白天鹅": [23.1075, 113.2386], # Shamian
    "宝汉酒家": [23.1260, 113.2320], # Zhongshan 8

    # --- Guangzhou (Yuexiu) ---
    "南信": [23.1165, 113.2483], # Shangxiajiu (Actually Liwan, but listed here)
    "开记": [23.1165, 113.2483], # Shangxiajiu
    "百花甜品": [23.1256, 113.2750], # Wenming Rd
    "玫瑰甜品": [23.1256, 113.2752], # Wenming Rd
    "达扬炖品": [23.1256, 113.2750], # Wenming Rd
    "穗银肠粉": [23.1240, 113.2840], # Dongchuan Rd
    "信记": [23.1130, 113.2600], # Changdi
    "广州酒家": [23.1168, 113.2460], # Wenchang South
    "广州宾馆": [23.1180, 113.2630], # Haizhu Square
    "点都德": [23.1250, 113.2700], # Beijing Rd
    "陶陶居": [23.1160, 113.2480], # Dishifu Rd
    "惠食佳": [23.1070, 113.2650], # Binjiang (Haizhu) but iconic
    "众源美食": [23.1260, 113.2480], # Guangfu North

    # --- Guangzhou (Haizhu / Others) ---
    "森焱食馆": [23.0950, 113.2550], # Tongfu Middle
    "肥姐美食": [23.0950, 113.2550], # Tongfu
    "贰少品味": [23.0950, 113.2550], # Tongfu Middle
    "金辉食馆": [23.1000, 113.2600], # Tongfu
    "森成美食店": [23.1050, 113.2500], # Nanhua West
    "炳胜品味": [23.1182, 113.3256], # Zhujiang New Town
    "陶然轩": [23.1090, 113.2980], # Ersha Island
    "御宝轩": [23.1170, 113.3280], # igc
    "旺金鸽": [23.1200, 113.3200], # Tianhe

    # --- Manual Fixes from User ---
    "对面的糊天甜品": [23.1285, 113.2458], # Force mapping to Hutian
    "一品为先食得好": [23.1288, 113.2455],
    "同发号": [23.1200, 113.2500],
}

DISTRICT_COORDS = {
    # HK defaults
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
    # GZ defaults
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

def get_location_info(name, text, city):
    # Cleaning name for lookup (Remove common prefixes)
    clean_name = name.replace("对面的", "").replace("香港", "").strip()
    
    # 1. PREDEFINED LOOKUP
    # Check exact match or substring
    for k, v in PREDEFINED_LOCATIONS.items():
        if k in clean_name or clean_name in k:
            # Map region name based on coords roughly
            region = "香港" if city == "hk" else "广州"
            if city == "hk":
                if v[1] < 114.16: region = "中环/上环"
                elif v[1] < 114.175: region = "尖沙咀/佐敦"
                elif v[1] < 114.19: region = "湾仔/铜锣湾"
                elif v[0] > 22.30: region = "旺角/深水埗"
            else:
                if v[0] > 23.13: region = "西华路/越秀"
                elif v[0] < 23.11: region = "海珠/沙面"
                elif v[1] > 113.30: region = "天河/珠江新城"
                else: region = "荔湾/上下九"
                
            return v[0], v[1], region
            
    # 2. DISTRICT LOOKUP
    base = DEFAULT_HK if city == "hk" else DEFAULT_GZ
    region = "香港" if city == "hk" else "广州"
    
    for d, c in DISTRICT_COORDS.items():
        if d in text:
            base = c
            region = d
            break
            
    # Random Jitter (approx 50m)
    lat = base[0] + (random.random() - 0.5) * 0.002
    lng = base[1] + (random.random() - 0.5) * 0.002
    return round(lat, 5), round(lng, 5), region

def parse_line_improved(line):
    # Remove leading numbering
    clean = re.sub(r'^\d+\.\s*', '', line).strip()
    if not clean: return None, None, None
    
    name, loc, rest = "", "", ""
    
    # Check for brackets
    match_br = re.match(r"^([^\(（]+)[\(（]([^\)）]+)[\)）](.*)", clean)
    
    if match_br:
        name = match_br.group(1).strip()
        loc = match_br.group(2).strip()
        rest = match_br.group(3).strip()
    else:
        # Split by comma or space
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
            
    # Cleaning special prefixes in GZ list
    if name.startswith("对面的"):
        name = name.replace("对面的", "")
        
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
        
        # Location Logic
        text_for_search = name + " " + loc + " " + rest
        lat, lng, region = get_location_info(name, text_for_search, mode)
        
        items.append({
            "name": name,
            "type": current_cat,
            "lat": lat,
            "lng": lng,
            "address": region, # Using Region as Address for map display
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
        a = item['address'].replace('"', '\\"') # This is now the specific region e.g. "Central"
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
