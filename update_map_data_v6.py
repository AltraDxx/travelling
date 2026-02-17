
import re
import json
import random

# --- CONFIG ---
MD_FILE = '/Users/dxx/Coding/travelling/美食.md'
HTML_FILE = '/Users/dxx/Coding/travelling/food_map.html'

# --- CLEANING & MAPPING ---
# Specific manual fixes for names that are hard to parse or contain "description" in the name slot
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

# Coordinates Database (Enhanced)
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
    "炜明肠粉店": [23.1280, 113.2480], 
    "源记肠粉": [23.1250, 113.2400], # 华贵路
    "穗银肠粉": [23.1240, 113.2840], # 东川路
    "达扬炖品": [23.1256, 113.2750], # 文明路
    "信记": [23.1130, 113.2600], # 长堤大马路
    "森焱食馆": [23.0950, 113.2550], # 同福中路
    "肥姐美食": [23.0950, 113.2550], # 环珠直街
    "贰少品味": [23.0960, 113.2540], # 同福中路 (Corrected)
    "众源美食": [23.1260, 113.2480], # 光复北路555号
    "同乐居菜馆": [23.1250, 113.2520], # 惠福西路
    "惠食佳": [23.1070, 113.2650], # 滨江
    "陶然轩": [23.1090, 113.2980], # 二沙岛
    "喜势点茶居": [23.1290, 113.2640], # 德政中路
    "新文记": [23.1050, 113.2600], # 市二宫
    "煲笼兴": [23.1050, 113.2600],
    "丽的面家": [23.1280, 113.2650], # 德政中路 ??? Need verify. Assuming duofu nearby. No, Li's Noodle is usually elsewhere. Let's use generic Yuexiu.
    "吴财记": [23.1150, 113.2450], # 大同路
    "恩宁刘福记": [23.1150, 113.2360], # 恩宁路
    "旺记烧腊": [23.1220, 113.2380], # 逢源路
    "永兴烧腊": [23.1280, 113.2640], 
    "惠来": [23.1280, 113.2640],
    "云浮烧鸭": [23.1400, 113.2300], # 鹅掌坦 (Generic)
    "森成美食店": [23.1050, 113.2500], # 南华西路
    "金辉食馆": [23.1000, 113.2600], # 同福中路
    "旺金鸽": [23.1200, 113.3200], # 天河
    "鸽皇农庄": [23.1800, 113.3500], # Longdong (Far)
    "悦宴酒家": [23.1800, 113.3500],
    "顺得来": [23.1270, 113.2700], # Wuyuehua
    "伍湛记": [23.1200, 113.2400],
    "标记美食": [23.1280, 113.2650],
    "御手信": [23.1280, 113.2750], # Zhonghua Plaza
    
    # --- Hong Kong ---
    "华星冰室": [22.2775, 114.1782],
    "金华冰厅": [22.3228, 114.1691],
    "翠华餐厅": [22.2982, 114.1738],
    "食光荣": [22.3180, 114.1700],
    "金禾阁": [22.3800, 114.1950], # Sha Tin
    "美好快餐": [22.3800, 114.1950], # Sha Tin
    "源记": [22.2988, 114.1722], # TST
    "佳记餐厅": [22.2988, 114.1722],
    "泰昌饼家": [22.2825, 114.1539],
    "瑞记": [22.2858, 114.1502],
    "科记咖啡餐厅": [22.2868, 114.1486],
    "金凤茶餐厅": [22.2751, 114.1728],
    "新香园": [22.3300, 114.1610], # SSP
    "利苑酒家": [22.2798, 114.1789],
    "荣记饭店": [22.2783, 114.1802],
    "莲香居": [22.2882, 114.1448],
    "稻香": [22.3956, 114.1963], # Fo Tan
    "端记茶楼": [22.3193, 114.1694], # Usually Tai Mo Shan, but using default if unknown
    "莲香楼": [22.2842, 114.1538],
    "牛阵": [22.3200, 114.1700],
    "源記甜品": [22.2860, 114.1400], # Sai Ying Pun
    "佳佳甜品": [22.3056, 114.1690],
    "福元湯圓": [22.2885, 114.1932], # North Point
    "北角雞蛋仔": [22.2918, 114.2008],
    "沾仔記": [22.2818, 114.1552],
    "廟街興記": [22.3094, 114.1702],
    "華香園": [22.2974, 114.1691],
    "媽咪雞蛋仔": [22.2800, 114.1830],
    "合香園": [22.2900, 114.1500], # ???
    "德發牛丸": [22.2974, 114.1691],
    "水記": [22.2841, 114.1538],
    "生记": [22.2863, 114.1512],
    "荣记粉面": [22.2804, 114.1857],
    "文记": [22.3032, 114.1856],
    "Kabo": [22.2980, 114.1720],
    "英记面家": [22.2850, 114.1400], # Sai Ying Pun
    "达濠仔": [22.3100, 114.1700],
    "卖奀记忠记": [22.2838, 114.1542],
    "蛇王芬": [22.2824, 114.1540],
    "面尊": [22.2800, 114.1850],
    "华姐清汤腩": [22.2825, 114.1915],
    "乐园鱼蛋粉": [22.2804, 114.1857],
    "庙街牛什": [22.3094, 114.1702],
    "红磡鸡蛋仔": [22.3032, 114.1856],
    "兴记": [22.2980, 114.1720],
    "新兴食家": [22.2850, 114.1400], # Sai Ying Pun
    "Bakehouse": [22.2985, 114.1735],
    "Vission Bakery": [22.2820, 114.1545],
    "Owls Choux": [22.2980, 114.1720],
    "Shari Shari": [22.2820, 114.1545],
    "Tokachi": [22.2980, 114.1720],
    "棋哥": [22.2780, 114.1800], # Wan Chai
    "甘堂": [22.2783, 114.1758],
    "一乐": [22.2824, 114.1558],
    "鏞記酒家": [22.2818, 114.1552],
    "新桂香": [22.2700, 114.2380],
    "国金轩": [22.2950, 114.1700],
}

DISTRICT_COORDS = {
    "尖沙咀": [22.2988, 114.1722],
    "旺角": [22.3193, 114.1694],
    "中环": [22.2819, 114.1581],
    "铜锣湾": [22.2804, 114.1857],
    "湾仔": [22.2760, 114.1751],
    "深水埗": [22.3307, 114.1622],
    "沙田": [22.3813, 114.1945],
    "红磡": [22.3032, 114.1856],
    "上环": [22.2867, 114.1508],
    "佐敦": [22.3040, 114.1712],
    "北角": [22.2922, 114.2005],
    "天后": [22.2825, 114.1915],
    "大角咀": [22.3214, 114.1614],
    "西环": [22.2858, 114.1428],
    "西华路": [23.1315, 113.2455],
    "上下九": [23.1165, 113.2483],
    "文明路": [23.1256, 113.2750],
    "珠江新城": [23.1182, 113.3256],
    "天河": [23.1248, 113.3600],
    "越秀": [23.1310, 113.2700],
    "海珠": [23.0900, 113.2700],
    "荔湾": [23.1100, 113.2300],
}

DEFAULT_LOCS = { 'gz': [23.1291, 113.2644], 'hk': [22.3193, 114.1694] }

def clean_extracted_name(name):
    """
    Cleans the name based on the NAME_FIXES map and removing common trash characters.
    """
    name = name.strip()
    
    # 1. Exact fix (fast)
    if name in NAME_FIXES:
        return NAME_FIXES[name]
        
    # 2. Heuristic Cleaning
    # Remove leading dots or numbers if any (should benefit parsing)
    name = re.sub(r'^[\d\.]+', '', name).strip()
    
    # Remove brackets and content strictly if they are at the END
    # But some names have brackets in middle? Usually no.
    # Logic: If name has brackets, take the part BEFORE brackets as name, INSIDE as address/note.
    if '（' in name:
        name = name.split('（')[0]
    if '(' in name:
        name = name.split('(')[0]
        
    # Remove spaces
    name = name.strip()
    
    # Late check if the cleaned name is in FIXES
    if name in NAME_FIXES:
        return NAME_FIXES[name]
        
    return name

def get_coords_and_address(name, raw_line, city):
    """
    Returns [lat, lng, address]
    """
    # 1. Predefined exact match
    if name in PREDEFINED_LOCATIONS:
        c = PREDEFINED_LOCATIONS[name]
        # Return matched coords
        # Address: Try to extract from raw line or use district
        return c[0], c[1], clean_address_from_line(raw_line) or get_district_from_coords(c, city)

    # 2. Fuzzy/Substring match in Predefined
    for k, v in PREDEFINED_LOCATIONS.items():
        if k in name or name in k:
            return v[0], v[1], clean_address_from_line(raw_line) or get_district_from_coords(v, city)
            
    # 3. District Fallback
    base = DEFAULT_LOCS[city]
    region = "广州" if city == "gz" else "香港"
    
    for d, c in DISTRICT_COORDS.items():
        if d in raw_line:
            base = c
            region = d
            break
            
    # Jitter
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
        return "老城区"

def clean_address_from_line(line):
    # Try to extract content inside brackets () or （）
    m = re.search(r'[（\(](.*?)[）\)]', line)
    if m:
        content = m.group(1).strip()
        # If content contains "推荐", "店", "对面", "路", "街" - it's likely address.
        # If it's just "市二宫", it's address.
        return content
    return None

def process_line(line, current_cat, city):
    # Remove ordering "1. "
    line = re.sub(r'^\d+\.\s*', '', line).strip()
    if not line: return None
    
    # 1. Separation Strategy
    # Most lines are: "Name（Loc）Dishes" or "Name Dishes" or "Name, Dishes"
    
    name = ""
    dishes_note_raw = ""
    
    # Detect separator
    separators = ['（', '(', '，', ',', ' ']
    first_sep_idx = 9999
    sep_char = None
    
    for sep in separators:
        idx = line.find(sep)
        if idx != -1 and idx < first_sep_idx:
            first_sep_idx = idx
            sep_char = sep
            
    if sep_char:
        name = line[:first_sep_idx].strip()
        dishes_note_raw = line[first_sep_idx:].strip() # Keep separator for context or strip? 
        # Actually better to strip separator from the rest
        if sep_char in ['（', '(']:
             # Special case: The separator starts a bracket block. 
             # We assume the name is BEFORE. The Rest is (Loc) + Dishes
             pass
        else:
             dishes_note_raw = line[first_sep_idx+1:].strip()
    else:
        name = line
        dishes_note_raw = ""

    # clean name
    clean_name = clean_extracted_name(name)
    if not clean_name: return None
    
    # Get Loc
    lat, lng, address = get_coords_and_address(clean_name, line, city)
    
    # Clean Dishes/Notes (Remove coordinates info from dishes if accidentally captured)
    # also remove single brackets like '）' or ')' 
    rest = dishes_note_raw
    
    # Remove address from rest if it was bracketed
    # pattern: (Loc)
    rest = re.sub(r'[（\(].*?[）\)]', ' ', rest)
    rest = rest.replace('）', ' ').replace(')', ' ').replace('，', ' ').replace(',', ' ')
    
    # Remove duplicates like "推荐"
    rest = rest.replace('推荐', '')
    
    # Split remaining into Note vs Dishes ?
    # Heuristic: Short keywords are notes. Long are dishes. 
    # Or just dump all into dishes/notes.
    
    # Detect "Note" keywords
    warnings = ["现金", "排队", "服务", "态度", "预约", "黑脸", "难吃", "贵", "低消", "开门"]
    my_notes = []
    my_dishes = []
    
    # Split by space
    parts = rest.split()
    for p in parts:
        p = p.strip()
        if not p: continue
        if len(p) == 1: continue # Skip single chars
        
        is_warn = False
        for w in warnings:
            if w in p:
                my_notes.append(p)
                is_warn = True
                break
        if not is_warn:
            my_dishes.append(p)
            
    note_str = " ".join(my_notes)
    dish_str = " ".join(my_dishes)
    
    return {
        "name": clean_name,
        "type": current_cat,
        "lat": lat,
        "lng": lng,
        "address": address,
        "note": note_str,
        "dishes": dish_str,
        "city": city
    }

def process_md():
    with open(MD_FILE, 'r', encoding='utf-8') as f: lines = f.readlines()
    
    items = []
    mode = None 
    current_cat = "其他"
    
    # Mapping for category display names
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
        
        if line.startswith("####"):
            raw_cat = line.replace("####", "").replace("**", "").strip()
            # Normalize cat
            match_cat = "其他"
            for k, v in CAT_MAP.items():
                if k in raw_cat:
                    match_cat = v
                    break
            current_cat = match_cat
            continue
            
        if not line[0].isdigit(): continue 
        
        item = process_line(line, current_cat, mode)
        if item:
            items.append(item)

    return items

def generate_js():
    items = process_md()
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
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f: content = f.read()
    pattern = r"const placemarks = \[.*?\];"
    new_content = re.sub(pattern, js_data, content, flags=re.DOTALL)
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f: f.write(new_content)
    print(f"Updated {len(items)} items.")

if __name__ == "__main__":
    generate_js()
