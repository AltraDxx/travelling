
import re
import json
import random

# --- CONFIG ---
MD_FILE = '/Users/dxx/Coding/travelling/美食.md'
HTML_FILE = '/Users/dxx/Coding/travelling/food_map.html'

# --- CLEANING & MAPPING ---
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

# Extensive Coordinates Database (Aggregated from search)
PREDEFINED_LOCATIONS = {
    # --- Guangzhou ---
    "糊天甜品": [23.1285, 113.2458], # 荔湾区和安街78号
    "一品为先食得好": [23.1288, 113.2455], # 和安街67号
    "兰芳园": [23.1310, 113.2450], # 西华路402号
    "沙湾甜品": [23.1315, 113.2455], # 西华路第一津
    "合兴小食店": [23.1315, 113.2455], # 西华路第一津
    "顺势牛杂汤": [23.1330, 113.2460], # 司马坊
    "西关牛杂": [23.1315, 113.2455],
    "合众肠粉店": [23.1250, 113.2440], # 龙津路
    "炜明肠粉店": [23.1280, 113.2480], # 中山七路紫贵坊
    "源记肠粉": [23.1250, 113.2400], # 华贵路93号
    "穗银肠粉": [23.1240, 113.2840], # 东川路94号
    "达扬炖品": [23.1256, 113.2750], # 文明路
    "信记": [23.1130, 113.2600], # 长堤大马路270号
    "森焱食馆": [23.0950, 113.2550], # 同福中路龙福西二巷
    "肥姐美食": [23.0950, 113.2550], # 环珠直街
    "贰少品味": [23.0960, 113.2540], # 同福中路
    "众源美食": [23.1260, 113.2480], # 光复北路555号
    "同乐居菜馆": [23.1250, 113.2520], # 惠福西路
    "惠食佳": [23.1070, 113.2650], # 滨江西路172号
    "陶然轩": [23.1090, 113.2980], # 二沙岛
    "喜势点茶居": [23.1290, 113.2640], 
    "新文记": [23.1050, 113.2680], # 市二宫附近
    "煲笼兴": [23.1110, 113.2620], # 海珠? Assumed
    "丽的面家": [23.1250, 113.2700], # Duofu nearby?
    "吴财记": [23.1150, 113.2450], # 大同路
    "恩宁刘福记": [23.1250, 113.2860], # 东华东路547号 / Or Enning Rd original site [23.115, 113.236] - MD title says Enning
    "旺记烧腊": [23.1220, 113.2380], # 逢源路
    "永兴烧腊": [23.1140, 113.2440], # 梯云东路21号
    "惠来": [23.1280, 113.3500], # 惠来饭店 TANGXIA or Generic? MD: "Longgang cross". Mapping to Longgang Rd area.
    "云浮烧鸭": [23.1417, 113.2307], # 鹅掌坦
    "森成美食店": [23.1050, 113.2500], # 南华西路73号
    "金辉食馆": [23.1017, 113.2642], # 同福中路金粟园12号
    "旺金鸽": [23.1200, 113.3200], # Tianhe
    "鸽皇农庄": [23.1800, 113.3500], # Longdong
    "悦宴酒家": [23.1800, 113.3500], # Longdong
    "顺得来": [23.1270, 113.2700], # Beijing Rd, Guangda Lane 31
    "伍湛记": [23.1190, 113.2400], # Longjin
    "标记美食": [23.0135, 113.3361], # Panyu, Xinnan Ave 829
    "御手信": [23.1280, 113.2750], # Zhonghua Plaza
    "德记": [23.1400, 113.2360], # Bailng Rd or Xicha. Using Baining Rd for Porridge.
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
    if name in PREDEFINED_LOCATIONS:
        c = PREDEFINED_LOCATIONS[name]
        return c[0], c[1], clean_address_from_line(raw_line) or get_district_from_coords(c, city)

    for k, v in PREDEFINED_LOCATIONS.items():
        if k in name or name in k:
            return v[0], v[1], clean_address_from_line(raw_line) or get_district_from_coords(v, city)
            
    base = DEFAULT_LOCS[city]
    region = "广州" if city == "gz" else "香港"
    for d, c in DISTRICT_COORDS.items():
        if d in raw_line:
            base = c; region = d; break
            
    lat = base[0] + (random.random() - 0.5) * 0.003
    lng = base[1] + (random.random() - 0.5) * 0.003
    return round(lat, 5), round(lng, 5), region

def get_district_from_coords(coords, city):
    if city == 'hk':
        if coords[1] < 114.16: return "中环/上环"
        if coords[1] < 114.18: return "湾仔/尖沙咀"
        return "铜锣湾/北角"
    else:
        if coords[0] < 23.11: return "海珠"
        if coords[1] > 113.30: return "天河"
        return "老城区/荔湾" # Better generic name

def clean_address_from_line(line):
    m = re.search(r'[（\(](.*?)[）\)]', line)
    if m:
        content = m.group(1).strip()
        # Filter out obvious category texts inside brackets if any
        if len(content) > 1: return content
    return None

def clean_extracted_name(name):
    name = name.strip()
    if name in NAME_FIXES: return NAME_FIXES[name]
    name = re.sub(r'^[\d\.]+', '', name).strip()
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
        
        # Category Detect
        if line.startswith("####"):
            raw_cat = line.replace("####", "").replace("**", "").strip()
            match_cat = "其他"
            for k, v in CAT_MAP.items():
                if k in raw_cat: match_cat = v; break
            current_cat = match_cat
            # Reset tips for this cat if not exists
            if current_cat not in CAT_TIPS: CAT_TIPS[current_cat] = []
            continue
            
        # Parse Line
        if line[0].isdigit():
            # Item
            item = process_item_line(line, current_cat, mode)
            if item: items.append(item)
        else:
            # Knowledge/Info line (if we are in a mode)
            if mode and current_cat != "其他" and len(line) > 4:
                # Heuristic: exclude short lines or headers
                # Clean up
                info = line.replace("**", "")
                if current_cat in CAT_TIPS:
                    CAT_TIPS[current_cat].append(info)
                else:
                    CAT_TIPS[current_cat] = [info]

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
        if sep_char in ['（', '(']: # Bracket means address usually, keep full line processing logic
             dishes_raw = line[first_sep_idx:].strip() 
    else:
        name = line
        dishes_raw = ""

    clean_name = clean_extracted_name(name)
    if not clean_name: return None
    lat, lng, address = get_coords_and_address(clean_name, line, city)
    
    # Process Rest
    rest = dishes_raw
    rest = re.sub(r'[（\(].*?[）\)]', ' ', rest) # Remove address part
    rest = rest.replace('）', ' ').replace(')', ' ').replace('，', ' ').replace(',', ' ')
    rest = rest.replace('推荐', '')
    
    warnings = ["现金", "排队", "服务", "态度", "预约", "黑脸", "难吃", "贵", "低消", "开门"]
    my_notes = []
    my_dishes = []
    
    for p in rest.split():
        p = p.strip()
        if not p or len(p)==1: continue
        is_warn = False
        for w in warnings:
            if w in p: my_notes.append(p); is_warn = True; break
        if not is_warn: my_dishes.append(p)
            
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
    # Add Manual Internet Knowledge supplements
    CAT_TIPS["早茶"].append("技巧: 盖子揭开挂在壶边表示需要加水。")
    CAT_TIPS["烧腊"].append("烧鹅左腿最尊贵(也最贵)。")
    CAT_TIPS["茶餐厅"].append("行话: '走冰'去冰, '少甜'半糖。")
    
    tips_json = json.dumps({k: " | ".join(v[:2]) for k, v in CAT_TIPS.items() if v}, ensure_ascii=False)
    js_tips = f"const categoryInfo = {tips_json};"
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f: content = f.read()
    
    # Replace Placemarks
    content = re.sub(r"const placemarks = \[.*?\];", js_data, content, flags=re.DOTALL)
    # Replace Category Info
    content = re.sub(r"const categoryInfo = \{.*?\};", js_tips, content, flags=re.DOTALL)
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f: f.write(content)
    print(f"Updated {len(items)} items and category tips.")

if __name__ == "__main__":
    generate_js()
