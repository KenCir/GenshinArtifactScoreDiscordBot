from PIL import Image
from pyocr import pyocr


class ArtifactScore:
    def __init__(self):
        # 会心率
        self.satisfaction_score = 0
        # 会心率DMG
        self.satisfaction_dmg_score = 0
        # 元素チャージ効率
        self.charge_score = 0
        # 攻撃力%
        self.atk_score = 0
        # 攻撃力実数値
        self.atk_real_score = 0
        # 防御力%
        self.defense_score = 0
        # 防御力実数値
        self.defense_real_score = 0
        # HP%
        self.hp_score = 0
        # HP実数値
        self.hp_real_score = 0
        # 元素熟知
        self.familiarity_score = 0

        # OCRエンジンを取得
        engines = pyocr.get_available_tools()
        self.engine = engines[0]

    def calculation_score(self, score_type: str):
        if score_type == "attack":
            return self.satisfaction_score * 2 + self.satisfaction_dmg_score + self.atk_score
        elif score_type == "charge":
            return self.satisfaction_score * 2 + self.satisfaction_dmg_score + self.charge_score
        elif score_type == "defense":
            return self.satisfaction_score * 2 + self.satisfaction_dmg_score + self.charge_score
        elif score_type == "hp":
            return self.satisfaction_score * 2 + self.satisfaction_dmg_score + self.hp_score
        elif score_type == "familiarity":
            return self.satisfaction_score * 2 + self.satisfaction_dmg_score + self.familiarity_score
        else:
            return "Unknown Score"

    def comprehensive_evaluation(self, score: int, artifact_type: str):
        if artifact_type == "clock" or artifact_type == "crown":
            if score >= 30:
                return "S"
            elif score >= 20:
                return "A"
            elif score >= 10:
                return "B"
            else:
                return "C"
        else:
            if score >= 45:
                return "S"
            elif score >= 35:
                return "A"
            elif score >= 25:
                return "B"
            else:
                return "C"

    def check(self, score_type, artifact_type):
        txt = self.engine.image_to_string(Image.open('img.png'), lang="jpn")
        fields = []

        for txt_ in txt.replace(' ', '').splitlines():
            if txt_.find("・" + "会心率") != -1:
                self.satisfaction_score = float("".join(filter(lambda x: x.isdigit() or x == '.', txt_)))
                fields.append(["会心率", f"+{self.satisfaction_score}%"])
            elif txt_.find("・" + "会心ダメージ") != -1:
                self.satisfaction_dmg_score = float("".join(filter(lambda x: x.isdigit() or x == '.', txt_)))
                fields.append(["会心ダメージ", f"+{self.satisfaction_dmg_score}%"])
            elif txt_.find("・" + "攻撃力") != -1:
                if txt_.find("%") != -1:
                    self.atk_score = float("".join(filter(lambda x: x.isdigit() or x == '.', txt_)))
                    fields.append(["攻撃力", f"+{self.atk_score}%"])
                else:
                    self.atk_real_score = int("".join(filter(lambda x: x.isdigit(), txt_)))
                    fields.append(["攻撃力", f"+{self.atk_real_score}"])
            elif txt_.find("・" + "防御力") != -1:
                if txt_.find("%") != -1:
                    self.defense_score = float("".join(filter(lambda x: x.isdigit() or x == '.', txt_)))
                    fields.append(["防御力", f"+{self.defense_score}%"])
                else:
                    self.defense_real_score = int("".join(filter(lambda x: x.isdigit(), txt_)))
                    fields.append(["防御力", f"+{self.defense_real_score}"])
            elif txt_.find("・" + "HP") != -1:
                if txt_.find("%") != -1:
                    self.hp_score = float("".join(filter(lambda x: x.isdigit() or x == '.', txt_)))
                    fields.append(["HP", f"+{self.hp_score}%"])
                else:
                    self.hp_real_score = int("".join(filter(lambda x: x.isdigit(), txt_)))
                    fields.append(["HP", f"+{self.hp_real_score}"])
            elif txt_.find("・" + "元素チャージ効率") != -1:
                self.charge_score = float("".join(filter(lambda x: x.isdigit() or x == '.', txt_)))
                fields.append(["元素チャージ効率", f"+{self.charge_score}%"])
            elif txt_.find("・" + "元素熟知") != -1:
                self.familiarity_score = int("".join(filter(lambda x: x.isdigit(), txt_)))
                fields.append(["元素熟知", f"+{self.familiarity_score}"])

        all_score = round(self.calculation_score(score_type))
        comprehensive = self.comprehensive_evaluation(all_score, artifact_type)

        score_type_str = ""
        if score_type == "attack":
            score_type_str = "火力型"
        elif score_type == "defense":
            score_type_str = "防御型"
        elif score_type == "hp":
            score_type_str = "HP型"
        elif score_type == "charge":
            score_type_str = "元素チャージ効率型"
        elif score_type == "familiarity":
            score_type_str = "元素熟知型"
        else:
            score_type_str = "不明"

        artifact_type_str = ""
        if artifact_type == "flower":
            artifact_type_str = "花"
        elif artifact_type == "wing":
            artifact_type_str = "羽"
        elif artifact_type == "clock":
            artifact_type_str = "時計"
        elif artifact_type == "cup":
            artifact_type_str = "杯"
        elif artifact_type == "crown":
            artifact_type_str = "冠"
        else:
            artifact_type_str = "不明"

        return all_score, comprehensive, score_type_str, artifact_type_str, fields
