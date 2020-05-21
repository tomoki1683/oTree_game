from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'matching'
    players_per_group = 4
    num = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars["preference_m"] = [random.sample([i for i in range(Constants.num)], Constants.num) for j in range(Constants.num)]
        self.session.vars["preference_w"] = [random.sample([i for i in range(Constants.num)], Constants.num) for j in range(Constants.num)]
        self.session.vars["for_playerRole"] = random.sample([i + 1 for i in range(Constants.players_per_group)], Constants.players_per_group)

class Group(BaseGroup):
    def set_payoff(self):
        # 申告された選好をまとめる
        m_sub = []
        w_sub = []
        for man in range(Constants.num):
            man_pre = self.get_player_by_role("m" + str(man + 1)).preference_sub.split(' ')
            man_int = [int(i) - 1 for i in man_pre]
            m_sub.append(man_int)
        for woman in range(Constants.num):
            woman_pre = self.get_player_by_role("w" + str(woman + 1)).preference_sub.split(' ')
            woman_int = [int(i) - 1 for i in woman_pre]
            w_sub.append(woman_int)
        # マッチング結果を求める
        result = [[Constants.num + 1 for j in range(Constants.num)] for i in range(2)] # change value to index of the partner when mathing happens
        m_decided = [0 for i in range(Constants.num)] # indices of the man who decided to match will be 1
        m_stage = [0 for i in range(Constants.num)] # indices of men's preferences in stage by stage
        while 0 in m_decided:
            for m_person in range(Constants.num):
                if m_decided[m_person] < 1:
                    w_target = m_sub[m_person][m_stage[m_person]]
                    m_stage[m_person] += 1 # this man will attack to woman of this stage, so stage number increases
                    if result[1][w_target] > Constants.num:
                        result[0][m_person] = w_target
                        result[1][w_target] = m_person
                        m_decided[m_person] = 1
                    elif w_sub[w_target].index(m_person) < w_sub[w_target].index(result[1][w_target]):
                        m_decided[result[1][w_target]] = 0
                        result[0][m_person] = w_target
                        result[1][w_target] = m_person
                        m_decided[m_person] = 1
        # 各プレイヤーの利得を求める
        for man in range(Constants.num):
            man_pre = self.get_player_by_role("m" + str(man + 1)).preference_sub.split(' ')
            man_str = [str(int(i) - 1) for i in man_pre]
            priority = man_str.index(str(result[0][man]))
            self.get_player_by_role("m" + str(man + 1)).match = "女性" + str(result[0][man] + 1)
            self.get_player_by_role("m" + str(man + 1)).payoff = Constants.num - priority
        for woman in range(Constants.num):
            woman_pre = self.get_player_by_role("w" + str(woman + 1)).preference_sub.split(' ')
            woman_str = [str(int(i) - 1) for i in woman_pre]
            priority = woman_str.index(str(result[1][woman]))
            self.get_player_by_role("w" + str(woman + 1)).match = "男性" + str(result[1][woman] + 1)
            self.get_player_by_role("w" + str(woman + 1)).payoff = Constants.num - priority

class Player(BasePlayer):
    preference_sub = models.StringField(
        label = "1 4 2 3 6 5のように、半角英数字と半角スペースを用いてください。\nカンマや全角スペースは記入しないでください。\n一番左が第一志望となるように、重複無しで順に番号を記入してください。"
    )
    match = models.StringField()
    def preference_sub_error_message(self, value):
        print("入力された値は", value, "です")
        split_value = value.split(' ')
        if set(split_value) != set([str(i + 1) for i in range(Constants.num)]):
            return "入力エラーです。正しいフォーマットに従ってください。"

    def role(self):
        index_p = self.session.vars["for_playerRole"].index(self.id_in_group)
        if index_p < Constants.num:
            return "m" + str(index_p + 1)
        else:
            return "w" + str(index_p - Constants.num + 1)
