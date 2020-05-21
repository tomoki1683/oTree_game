from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class SubmitPreferences(Page):
    form_model = "player"
    form_fields = ["preference_sub"]

    def vars_for_template(self):
        index_p = self.session.vars["for_playerRole"].index(self.player.id_in_group)
        if index_p < Constants.num:
            your_original_preference = self.session.vars["preference_m"][index_p]
            return dict(
                your_role = "男性" + str(index_p + 1),
                your_true_preference = ["女性" + str(i + 1) for i in your_original_preference]
            )
        else:
            your_original_preference = self.session.vars["preference_w"][index_p - Constants.num]
            return dict(
                your_role = "女性" + str(index_p - Constants.num + 1),
                your_true_preference = ["男性" + str(i + 1) for i in your_original_preference]
            )

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = "set_payoff"


class Results(Page):
    def vars_for_template(self):
        index_p = self.session.vars["for_playerRole"].index(self.player.id_in_group)
        if index_p < Constants.num:
            your_original_preference = self.session.vars["preference_m"][index_p - Constants.num]
            return dict(
                your_role = "男性" + str(index_p + 1),
                your_true_preference = ["女性" + str(i + 1) for i in your_original_preference],
                your_match = self.player.match
            )
        else:
            your_original_preference = self.session.vars["preference_w"][index_p - Constants.num]
            return dict(
                your_role = "女性" + str(index_p - Constants.num + 1),
                your_true_preference = ["男性" + str(i + 1) for i in your_original_preference],
                your_match = self.player.match
            )

page_sequence = [SubmitPreferences, ResultsWaitPage, Results]
