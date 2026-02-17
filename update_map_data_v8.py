
import re
import json
import random

# --- CONFIG ---
MD_FILE = '/Users/dxx/Coding/travelling/美食.md'
HTML_FILE = '/Users/dxx/Coding/travelling/food_map.html'

# --- DATA ---
# Manual Fixes for Names
NAME_FIXES = {
    "对面的糊天甜品": "糊天甜品",
    "中华广场的御手信": "御手信",
    "顺势牛杂汤•30年老字号": "顺势牛杂汤",
    "同发号百年老店": "同发号",
    "沾仔記雲吞麵": "沾仔記",
    "水記牛腩": "水記",
    "英记面家 叉烧牛腩面": "英记面家",
    "悦宴酒家·红烧乳鸽": "悦宴酒家",
    "金华冰厅 菠萝包": "金华冰厅",
    "伍湛记粥品专家": "伍湛记",
    "标记美食新鲜猪杂": "标记美食",
    "德记猪肝粥": "德记",
    "永兴烧腊 叉烧好吃": "永兴烧腊",
    "恩宁刘福记 竹升面": "恩宁刘福记",
    "佳佳甜品 芝麻糊": "佳佳甜品",
    "shari shari kakigori house": "Shari Shari",
    "tokachi-milky": "Tokachi",
    "owls choux": "Owls Choux",
    "vission bakery": "Vission Bakery",
    "bakehouse": "Bakehouse",
    "甘堂 烧鹅": "甘堂",
    "一乐 便宜": "一乐",
    "食光榮": "食光荣",
    "kabo": "Kabo"
}

# --- CHAINS LIST ---
# Shops known to have branches. We will tag them.
CHAINS = [
    "华星冰室", "翠华餐厅", "兰芳园", "Bakehouse", "达扬炖品", "点都德", "炳胜品味", 
    "惠食佳", "陶然轩", "义顺牛奶公司", "澳洲牛奶公司", "何洪记", "池记", "再兴烧腊",
    "妈咪鸡蛋仔", "敏华冰厅", "棋哥", "泰昌饼家", "利苑酒家", "稻香", "佳佳甜品",
    "许留山", "满记甜品", "海皇粥店", "一粥面", "太兴", "大快活", "大家乐", "美心",
    "东海堂", "奇华", "荣华", "恒香", "鉅记", "Vission Bakery"
]

# Extensive Coordinates Database (Curated for priority: Document Specific > Tourist Hubs > Popularity)
PREDEFINED_LOCATIONS = {
    # --- Guangzhou ---
    "糊天甜品": [23.1285, 113.2458], # 荔湾区和安街78号
    "一品为先食得好": [23.1288, 113.2455], # 和安街67号
    "兰芳园": [23.1310, 113.2450], # 广州西华路店 (Specific in MD)
    "沙湾甜品": [23.1315, 113.2455], # 西华路第一津
    "合兴小食店": [23.1315, 113.2455], # 西华路第一津
    "顺势牛杂汤": [23.1330, 113.2460], # 司马坊
    "西关牛杂": [23.1315, 113.2455],
    "合众肠粉店": [23.1250, 113.2440], # 龙津路
    "炜明肠粉店": [23.1280, 113.2480], # 中山七路紫贵坊
    "源记肠粉": [23.1250, 113.2400], # 华贵路93号
    "穗银肠粉": [23.1240, 113.2840], # 东川路94号
    "达扬炖品": [23.1256, 113.2750], # 文明路 (Classic)
    "信记": [23.1130, 113.2600], # 长堤大马路270号
    "森焱食馆": [23.0950, 113.2550], # 同福中路龙福西二巷
    "肥姐美食": [23.0950, 113.2550], # 环珠直街
    "贰少品味": [23.0960, 113.2540], # 同福中路
    "众源美食": [23.1260, 113.2480], # 光复北路555号
    "同乐居菜馆": [23.1250, 113.2520], # 惠福西路
    "惠食佳": [23.1070, 113.2650], # 滨江西路172号 (Popular)
    "陶然轩": [23.1090, 113.2980], # 二沙岛
    "喜势点茶居": [23.1290, 113.2640], 
    "新文记": [23.1050, 113.2680], # 市二宫附近
    "煲笼兴": [23.1110, 113.2620], 
    "丽的面家": [23.1250, 113.2700], 
    "吴财记": [23.1150, 113.2450], # 大同路
    "恩宁刘福记": [23.1250, 113.2860], # 东华东路 (Michelin)
    "旺记烧腊": [23.1220, 113.2380], # 逢源路
    "永兴烧腊": [23.1140, 113.2440], # 梯云东路21号
    "惠来": [23.1280, 113.3500], # 惠来饭店
    "云浮烧鸭": [23.1417, 113.2307], # 鹅掌坦
    "森成美食店": [23.1050, 113.2500], # 南华西路73号
    "金辉食馆": [23.1017, 113.2642], # 同福中路金粟园12号
    "旺金鸽": [23.1200, 113.3200], 
    "鸽皇农庄": [23.1800, 113.3500],
    "悦宴酒家": [23.1800, 113.3500],
    "顺得来": [23.1270, 113.2700], # Beijing Rd
    "伍湛记": [23.1190, 113.2400], # Longjin
    "标记美食": [23.0135, 113.3361], # Panyu
    "御手信": [23.1280, 113.2750], # Zhonghua Plaza
    "德记": [23.1360, 113.2400], # Xicha / Bailing - Using Bailing Rd [23.132, 113.260]? Let's stick to Xicha for strict match if needed, but Bailing is better location. Let's use Bailing for "Deji".
    
    # --- Hong Kong (Prioritize TST, Wan Chai, Central, CWB) ---
    "华星冰室": [22.2775, 114.1782], # Wan Chai (Original/Popular)
    "金华冰厅": [22.3228, 114.1691], # Prince Edward (Main)
    "翠华餐厅": [22.2819, 114.1555], # Central (Wellington) - Classic tourist spot (or TST Carnarvon [22.298, 114.173])
    "食光荣": [22.3180, 114.1700], 
    "金禾阁": [22.3800, 114.1950], # Sha Tin (Explicit in MD)
    "美好快餐": [22.3800, 114.1950], # Sha Tin (Explicit in MD)
    "源记": [22.2988, 114.1722], # TST (Granville Rd)
    "佳记餐厅": [22.2988, 114.1722], # TST (Generic placement for "Kai Kee")
    "泰昌饼家": [22.2825, 114.1539], # Central (Lyndhurst Terrace) - The most famous one
    "瑞记": [22.2858, 114.1502], # Sheung Wan Market
    "科记咖啡餐厅": [22.2868, 114.1486], # Sheung Wan
    "金凤茶餐厅": [22.2751, 114.1728], # Wan Chai
    "新香园": [22.3300, 114.1610], # Sham Shui Po (Iconic)
    "利苑酒家": [22.2798, 114.1789], # Wan Chai
    "荣记饭店": [22.2783, 114.1802], # Wan Chai (Explicit in MD)
    "莲香居": [22.2882, 114.1448], # Sheung Wan
    "稻香": [22.3956, 114.1963], # Fo Tan (Explicit in MD)
    "端记茶楼": [22.3193, 114.1694], 
    "莲香楼": [22.2842, 114.1538], # Central (Wellington)
    "牛阵": [22.2970, 114.1720], # TST (iSquare) - Tourist hub
    "源記甜品": [22.2860, 114.1400], # Sai Ying Pun
    "佳佳甜品": [22.3056, 114.1690], # Jordan
    "福元湯圓": [22.2885, 114.1932], # North Point
    "北角雞蛋仔": [22.2918, 114.2008], # North Point
    "沾仔記": [22.2818, 114.1552], # Central (Wellington/Queen's Rd)
    "廟街興記": [22.3094, 114.1702], # Yau Ma Tei
    "華香園": [22.2974, 114.1691], # TST (Haiphong Rd) - Explicit in MD
    "媽咪雞蛋仔": [22.2980, 114.1725], # TST (Carnarvon/Star Ferry). Picking TST.
    "合香園": [22.2900, 114.1500], 
    "德發牛丸": [22.2974, 114.1691], # TST (Haiphong Rd Market)
    "水記": [22.2841, 114.1538], # Central (Gage St)
    "生记": [22.2863, 114.1512], # Sheung Wan (Burd Street)
    "荣记粉面": [22.2804, 114.1857], # Causeway Bay (Explicit in MD)
    "文记": [22.3032, 114.1856], # Hung Hom (Explicit in MD)
    "Kabo": [22.2980, 114.1720], # TST logic
    "英记面家": [22.2850, 114.1400], # Sai Ying Pun
    "达濠仔": [22.3100, 114.1700],
    "卖奀记忠记": [22.2838, 114.1542], # Central (Wellington)
    "蛇王芬": [22.2824, 114.1540], # Central (Explicit in MD)
    "面尊": [22.2820, 114.1550], # Central (Or CWB). MD says both. Pick Central.
    "华姐清汤腩": [22.2825, 114.1915], # Tin Hau
    "乐园鱼蛋粉": [22.2804, 114.1857], # Causeway Bay (Explicit)
    "庙街牛什": [22.3094, 114.1702], # Temple St
    "红磡鸡蛋仔": [22.3032, 114.1856], # Hung Hom
    "兴记": [22.2980, 114.1720], 
    "新兴食家": [22.2850, 114.1400], # Sai Ying Pun
    "Bakehouse": [22.2820, 114.1530], # Central (Staunton St/Soho) - Very iconic/central
    "Vission Bakery": [22.2820, 114.1535], # Central (Soho)
    "Owls Choux": [22.2980, 114.1720], # TST
    "Shari Shari": [22.2820, 114.1545], # Central/Soho or CWB. 
    "Tokachi": [22.2980, 114.1720], 
    "棋哥": [22.2780, 114.1800], # Wan Chai
    "甘堂": [22.2783, 114.1758], # Wan Chai
    "一乐": [22.2824, 114.1558], # Central (Stanley St)
    "鏞記酒家": [22.2818, 114.1552], # Central
    "新桂香": [22.2700, 114.2380], # Chai Wan (Far but famous)
    "国金轩": [22.2950, 114.1700], # TST (The Mira) or Central (IFC)
}

DISTRICT_COORDS = {
    "尖沙咀": [22.2988, 114.1722], "旺角": [22.3193, 114.1694],
    "中环": [22.2819, 114.1581], "铜锣湾": [22.2804, 114.1857],
    "湾仔": [22.2760, 114.1751], "深水埗": [22.3307, 114.1622],
    "沙田": [22.3813, 114.1945], "红磡": [22.3032, 114.1856],
    "上环": [22.2867, 114.1508], "佐敦": [22.3040, 114.1712],
    "北角": [22.2922, 114.2005], "天后": [22.2825, 114.1915],
    "西环": [22.2858, 114.1428], "西华路": [23.1315, 113.2455],
    "上下九": [23.1165, 113.2483], "文明路": [23.1256, 113.2750],
    "珠江新城": [23.1182, 113.3256], "海珠": [23.0900, 113.2700],
    "荔湾": [23.1100, 113.2300]
}

DEFAULT_LOCS = { 'gz': [23.1291, 113.2644], 'hk': [22.3193, 114.1694] }
CAT_TIPS = {}

def get_coords_and_address(name, raw_line, city):
    # 1. Predefined Exact
    if name in PREDEFINED_LOCATIONS:
        c = PREDEFINED_LOCATIONS[name]
        return c[0], c[1], clean_address_from_line(raw_line) or get_district_from_coords(c, city)

    # 2. Fuzzy
    for k, v in PREDEFINED_LOCATIONS.items():
        if k in name or name in k:
            return v[0], v[1], clean_address_from_line(raw_line) or get_district_from_coords(v, city)
            
    # 3. District Fallback (Read district from line content logic)
    base = DEFAULT_LOCS[city]
    region = "广州" if city == "gz" else "香港"
    found_dist = False
    for d, c in DISTRICT_COORDS.items():
        if d in raw_line:
            base = c; region = d; found_dist = True; break
            
    # Jitter
    lat = base[0] + (random.random() - 0.5) * 0.003
    lng = base[1] + (random.random() - 0.5) * 0.003
    return round(lat, 5), round(lng, 5), region

def get_district_from_coords(coords, city):
    if city == 'hk':
        if coords[1] < 114.15: return "上环/西环"
        if 114.15 <= coords[1] < 114.165: return "中环/金钟"
        if 114.165 <= coords[1] < 114.18: return "湾仔/尖沙咀"
        if 114.18 <= coords[1] < 114.19: return "铜锣湾/红磡"
        return "北角/其他"
    else:
        if coords[0] < 23.11: return "海珠"
        if coords[1] > 113.30: return "天河"
        return "越秀/荔湾"

def clean_address_from_line(line):
    # Aggressive address extraction
    # Anything inside parens is likely address or notes
    m = re.search(r'[（\(](.*?)[）\)]', line)
    if m:
        content = m.group(1).strip()
        return content
    return None

def clean_extracted_name(name):
    name = name.strip()
    if name in NAME_FIXES: return NAME_FIXES[name]
    name = re.sub(r'^[\d\.]+', '', name).strip()
    # Strip brackets for name
    if '（' in name: name = name.split('（')[0]
    if '(' in name: name = name.split('(')[0]
    name = name.strip()
    if name in NAME_FIXES: return NAME_FIXES[name]
    return name

def process_md():
    with open(MD_FILE, 'r', encoding='utf-8') as f: lines = f.readlines()
    
    items = []
    mode = None 
    current_cat = "其他"
    CAT_MAP = {
        "茶餐厅": "茶餐厅", "家常": "正餐", "糖水": "糖水", "小吃": "小吃",
        "烘焙": "烘焙", "烧味": "烧腊", "海鲜等": "海鲜", 
        "家常菜、酒楼": "家常菜", "早茶": "早茶", "云吞面": "云吞面", 
        "烧腊": "烧腊", "乳鸽": "乳鸽", "脆皖": "脆皖", "粥": "粥", 
        "伴手礼": "伴手礼", "下水": "牛杂/下水"
    }

    for line in lines:
        line = line.strip()
        if not line: continue
        if "### **广州**" in line: mode = 'gz'; continue
        if "### **香港**" in line: mode = 'hk'; continue
        
        # Category
        if line.startswith("####"):
            raw_cat = line.replace("####", "").replace("**", "").strip()
            match_cat = "其他"
            for k, v in CAT_MAP.items():
                if k in raw_cat: match_cat = v; break
            current_cat = match_cat
            if current_cat not in CAT_TIPS: CAT_TIPS[current_cat] = []
            continue
            
        # Parse
        if line[0].isdigit():
            item = process_item_line(line, current_cat, mode)
            if item: items.append(item)
        else:
            # Knowledge
            if mode and current_cat != "其他" and len(line) > 4:
                 # Heuristic: Filter out garbage
                 if "时间" in line or "要吃" in line or "推荐" in line or "需要" in line:
                    info = line.replace("**", "")
                    if current_cat in CAT_TIPS: CAT_TIPS[current_cat].append(info)
                    else: CAT_TIPS[current_cat] = [info]

    return items

def process_item_line(line, current_cat, city):
    line = re.sub(r'^\d+\.\s*', '', line).strip()
    if not line: return None
    
    # Separation
    separators = ['（', '(', '，', ',', ' ']
    first_sep_idx = 9999
    sep_char = None
    for sep in separators:
        idx = line.find(sep)
        if idx != -1 and idx < first_sep_idx: first_sep_idx = idx; sep_char = sep
            
    if sep_char:
        name = line[:first_sep_idx].strip()
        dishes_raw = line[first_sep_idx+1:].strip()
        if sep_char in ['（', '(']: 
             dishes_raw = line[first_sep_idx:].strip() 
             # Check if the content inside parens is a DISTRICT hint we should respect
             # e.g. "荣记粉面（铜锣湾）"
             paren_content = re.search(r'[（\(](.*?)[）\)]', line)
             # (Logic handled in address cleaner or manual coordinate validation, 
             # but here we rely on PREDEFINED map which I already curated based on MD content)
    else:
        name = line
        dishes_raw = ""

    clean_name = clean_extracted_name(name)
    if not clean_name: return None
    lat, lng, address = get_coords_and_address(clean_name, line, city)
    
    # Process Rest
    rest = dishes_raw
    rest = re.sub(r'[（\(].*?[）\)]', ' ', rest)
    rest = rest.replace('）', ' ').replace(')', ' ').replace('，', ' ').replace(',', ' ')
    rest = rest.replace('推荐', '')
    
    warnings = ["现金", "排队", "服务", "态度", "预约", "黑脸", "难吃", "贵", "低消", "开门"]
    my_notes = []
    my_dishes = []
    
    # Check Chain
    is_chain = False
    for c in CHAINS:
        if c in clean_name or clean_name in c:
            is_chain = True; break
    if is_chain:
        my_notes.append("(有分店)")
    
    for p in rest.split():
        p = p.strip()
        if not p or len(p)==1: continue
        is_warn = False
        for w in warnings:
            if w in p: my_notes.append(p); is_warn = True; break
        if not is_warn: my_dishes.append(p)
    
    # Add explicit warning if in MD line
    if "分店" in line and "(有分店)" not in my_notes:
        my_notes.append("(有分店)")
            
    return {"name": clean_name, "type": current_cat, "lat": lat, "lng": lng, "address": address, "note": " ".join(my_notes), "dishes": " ".join(my_dishes), "city": city}

def generate_js():
    items = process_md()
    
    # 1. Placemarks
    js_data = "const placemarks = [\n"
    for item in items:
        n = item['name'].replace('"', '\\"')
        t = item['type']
        a = (item['address'] or "").replace('"', '\\"')
        nt = item['note'].replace('"', '\\"')
        d = item['dishes'].replace('"', '\\"')
        c = item['city']
        js_data += f'    {{ name: "{n}", type: "{t}", lat: {item['lat']}, lng: {item["lng"]}, address: "{a}", note: "{nt}", dishes: "{d}", city: "{c}" }},\n'
    js_data += "];"
    
    # 2. Category Info
    CAT_TIPS["早茶"].append("技巧: 盖子揭开挂在壶边表示需要加水。")
    CAT_TIPS["烧腊"].append("烧鹅左腿最尊贵。")
    CAT_TIPS["茶餐厅"].append("行话: '走冰'去冰, '少甜'半糖。")
    
    tips_json = json.dumps({k: " | ".join(v[:3]) for k, v in CAT_TIPS.items() if v}, ensure_ascii=False)
    js_tips = f"const categoryInfo = {tips_json};"
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f: content = f.read()
    content = re.sub(r"const placemarks = \[.*?\];", js_data, content, flags=re.DOTALL)
    content = re.sub(r"const categoryInfo = \{.*?\};", js_tips, content, flags=re.DOTALL)
    with open(HTML_FILE, 'w', encoding='utf-8') as f: f.write(content)
    print(f"Updated {len(items)} items.")

if __name__ == "__main__":
    generate_js()
