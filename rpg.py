import random
# 資料設定
skills = {
    "火球術": {"mp_cost": 10, "damage": 30, "branch": "火焰"}
}

shop_items = {
    "1": {"name": "回復藥", "type": "item", "price": 20},
    "2": {"name": "鋼劍", "type": "weapon", "atk": 5, "price": 50},
    "3": {"name": "皮甲", "type": "armor", "def": 4, "price": 40}
}

enemy_drops = {
    "惡魔": ["回復藥", "強化材料"]
}

base_quests = {
    "討伐惡魔任務": {"target": "惡魔", "count": 1, "reward": 100}
}

# 類別定義

class Equipment:
    def __init__(self, name, atk=0, defense=0):
        self.name = name
        self.atk = atk
        self.defense = defense

class Character:
    def __init__(self, name, hp, atk, defense, mp, job="冒險者"):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_atk = atk
        self.base_def = defense
        self.mp = mp
        self.gold = 100
        self.skills = ["火球術"]
        self.weapon = None
        self.armor = None
        self.bag = []
        self.str = 5
        self.vit = 5
        self.enemy_kills = {}

    def is_alive(self):
        return self.hp > 0

    def calculate_atk(self):
        w_atk = self.weapon.atk if self.weapon else 0
        return self.base_atk + w_atk + self.str

    def calculate_defense(self):
        a_def = self.armor.defense if self.armor else 0
        return self.base_def + a_def + self.vit

# 戰鬥系統

def attack(attacker, defender):
    dmg = max(attacker.calculate_atk() - defender.calculate_defense(), 1)
    defender.hp -= dmg
    print(f"{attacker.name} 攻擊 {defender.name}，造成 {dmg} 點傷害")

def use_skill(user, target, skill_name):
    skill = skills.get(skill_name)
    if not skill:
        print("技能不存在")
        return

    if user.mp >= skill["mp_cost"]:
        user.mp -= skill["mp_cost"]
        target.hp -= skill["damage"]
        print(f"{user.name} 使用 {skill_name}，對 {target.name} 造成 {skill['damage']} 點傷害")
    else:
        print("MP 不足")

def battle(player, enemy):
    print(f"\n遭遇敵人：{enemy.name}")

    while player.is_alive() and enemy.is_alive():
        print(f"\n{player.name} HP: {player.hp}/{player.max_hp} | MP: {player.mp}")
        print(f"{enemy.name} HP: {enemy.hp}")
        action = input("選擇動作 (1. 普通攻擊 2. 火球術): ")

        if action == "1":
            attack(player, enemy)
        elif action == "2":
            use_skill(player, enemy, "火球術")
        else:
            print("無效輸入，跳過回合")

        if enemy.is_alive():
            attack(enemy, player)

    if player.is_alive():
        print(f"\n戰鬥勝利！你擊敗了 {enemy.name}")
        loot = random.choice(enemy_drops.get(enemy.name, ["無"]))
        if loot != "無":
            player.bag.append(loot)
            print(f"獲得物品：{loot}")
        player.enemy_kills[enemy.name] = player.enemy_kills.get(enemy.name, 0) + 1
    else:
        print("你被打敗了，遊戲結束")

# 設施功能

def open_shop(player):
    print("\n--- 商店清單 ---")
    for k, v in shop_items.items():
        print(f"{k}. {v['name']} - 價格: {v['price']} G")

    choice = input("輸入編號購買 (輸入 q 離開): ")
    if choice in shop_items:
        item = shop_items[choice]
        if player.gold >= item["price"]:
            player.gold -= item["price"]
            if item["type"] == "weapon":
                player.weapon = Equipment(item["name"], atk=item["atk"])
            elif item["type"] == "armor":
                player.armor = Equipment(item["name"], defense=item["def"])
            else:
                player.bag.append(item["name"])
            print(f"已購買 {item['name']}")
        else:
            print("金幣不足")

def forge(player):
    if "強化材料" in player.bag:
        if player.weapon:
            player.bag.remove("強化材料")
            player.weapon.atk += 2
            print(f"強化成功！{player.weapon.name} 攻擊力 +2")
        else:
            print("你目前沒有裝備武器")
    else:
        print("背包裡沒有強化材料")

# 主程式

def main():
    player_name = input("請輸入勇者名字: ")
    if not player_name:
        player_name = "勇者"

    player = Character(player_name, hp=100, atk=10, defense=5, mp=30)

    while player.is_alive():
        print(f"\n--- 選單 (金幣: {player.gold}G) ---")
        print("1. 進入戰鬥")
        print("2. 進入商店")
        print("3. 鍛造強化")
        print("4. 查看狀態與背包")
        print("q. 結束遊戲")

        choice = input("請選擇指令: ")

        if choice == "1":
            enemy = Character("惡魔", hp=50, atk=8, defense=2, mp=0)
            battle(player, enemy)
        elif choice == "2":
            open_shop(player)
        elif choice == "3":
            forge(player)
        elif choice == "4":
            print(f"\n--- {player.name} 狀態 ---")
            print(f"HP: {player.hp}/{player.max_hp}")
            print(f"攻擊力: {player.calculate_atk()}")
            print(f"防禦力: {player.calculate_defense()}")
            print(f"背包內容: {player.bag}")
        elif choice == "q":
            print("感謝遊玩！")
            break
        else:
            print("無效指令")

if __name__ == "__main__":
    main()
