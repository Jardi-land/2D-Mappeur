import os
import pygame
from settings import *
from git import Repo
import time
from utils import *


class menu:
    def __init__(self, surface):
        self.display_surface = surface

        self.wk_zone_res = screen_res_array[screen_res_numb + 1]

        self.color_end = pygame.Surface((self.wk_zone_res))

        self.color_end.fill((210, 203, 191))

        self.status = None

        self.news_height = 5

        self.news_space_line = 8 * 1.8

        self.news_text = []

        self.news_text.append(text(surface, "News:", 2, (5, self.news_height)))

        self.news_height += self.news_text[0].get_height() + \
            self.news_space_line

        self.commit_nb = 0

        self.repo = Repo(os.path.dirname(__file__))

        self.commits = self.repo.iter_commits(
            "master", max_count=100, since='30.days.ago')

        self.commit_dict = {}

        for commit_nb, commit in enumerate(self.commits):
            self.commit_dict[commit_nb] = {"author": commit.committer, "message": commit.message, "time": time.strftime(
                "%a, %d %b %Y %H:%M", time.localtime(commit.committed_date))}

        while self.news_height < screen_res[1] - 30:
            self.news_text.append(text(self.display_surface, f"¬{self.commit_dict[self.commit_nb]['message']}", 1.75, (
                5, self.news_height), (98, 86, 96), screen_res[0] - self.wk_zone_res[0] - 40))
            self.news_height += self.news_text[-1].get_height()
            self.news_text.append(text(self.display_surface, f"{self.commit_dict[self.commit_nb]['author']} - {self.commit_dict[self.commit_nb]['time']}", 1.6, (
                5, self.news_height), (147, 131, 119), screen_res[0] - self.wk_zone_res[0] - 40))
            self.news_height += (self.news_text[-1].get_height() +
                                 self.news_space_line)
            self.commit_nb += 1

        self.button_nv = button(surface, screen_res[0] - self.wk_zone_res[0] - 4 + (self.wk_zone_res[0] / 2), screen_res[1] -
                                self.wk_zone_res[1] - 4 + (self.wk_zone_res[1] / 2), 200, 50, "Nouveau projet", 2, "nv_projet")

        self.button_confirme = button(surface, screen_res[0] - self.wk_zone_res[0] - 4 + (
            self.wk_zone_res[0] / 2), screen_res[1] - self.wk_zone_res[1] - 4 + (self.wk_zone_res[1] / 2), 200, 50, "Confirmer", 2, "confirme", 30)

        self.button_quit = button(surface, screen_res[0] - self.wk_zone_res[0] - 4 + (self.wk_zone_res[0] / 2),
                                  screen_res[1] - self.wk_zone_res[1] - 4 + (self.wk_zone_res[1] / 2) + 50, 200, 50, "Quitter", 2, quit, 30)

        self.attention_text = text(surface, f"Attention vous êtes sur le point de crée un projet sur une base {screen_res[0]}x{screen_res[1]} !", 2, (
            screen_res[0] - self.wk_zone_res[0] - 4, screen_res[1] - self.wk_zone_res[1] - 4), (0, 0, 0), self.wk_zone_res[0] / 2)

        self.attention_text = text(surface, f"Attention vous êtes sur le point de crée un projet sur une base {screen_res[0]}x{screen_res[1]} !", 2, (
            screen_res[0] - self.wk_zone_res[0] - 4 + (self.wk_zone_res[0] / 2) - (self.attention_text.get_width() / 2), screen_res[1] - self.wk_zone_res[1] - 4 + (self.wk_zone_res[1] * 1 / 5) - (self.attention_text.get_height() / 2)), (0, 0, 0), self.wk_zone_res[0] / 2)

    def news(self):
        for text in self.news_text:
            text.draw()

    def update(self):
        self.keys = pygame.key.get_pressed()
        self.news()
        self.display_surface.blit(
            self.color_end, (screen_res[0] - self.wk_zone_res[0] - 4, screen_res[1] - self.wk_zone_res[1] - 4))
        if self.keys[pygame.K_ESCAPE]:
            self.status = None
        if self.status is None:
            if self.button_nv.update() is not None:
                self.status = self.button_nv.action
        elif self.status == "nv_projet":
            self.attention_text.draw()
            if self.button_confirme.update() is not None:
                return "confirme"
            elif self.button_quit.update() is not None:
                self.button_quit.update()()
        return None
