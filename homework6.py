############################################################
# CIS 521: Homework 6
############################################################

student_name = "James Wang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
from collections import defaultdict
import math
import os
import re

############################################################
# Section 1: Probability
############################################################

# Set the following variables to True or False.
section_1_problem_1a = True
section_1_problem_1b = True
section_1_problem_1c = False

# Set the following variables to True or False.
section_1_problem_2a = True
section_1_problem_2b = False
section_1_problem_2c = False
section_1_problem_2d = False
section_1_problem_2e = False
section_1_problem_2f = True
section_1_problem_2g = False
section_1_problem_2h = True

# Set the following variables to probabilities, expressed as decimals between 0
# and 1.
section_1_problem_3a = 0.01162455
section_1_problem_3b = 0.98837545
section_1_problem_3c = None
section_1_problem_3d = 0.10211147958415595
section_1_problem_3e = 0.0499
section_1_problem_3f = 7.4251875e-08
section_1_problem_3g = None


############################################################
# Section 2: Spam Filter
############################################################

def load_tokens(email_path):
    f_obj = open(email_path)
    msg = email.message_from_file(f_obj)
    lines = email.iterators.body_line_iterator(msg)
    one_gram = filter(None, " ".join([i.strip() for i in lines]).split())
    two_gram = [i + " " + j for i, j in zip(one_gram[:-1], one_gram[1:])]
    other_features = ["new_feature_length" for i in one_gram if len(i) > 20]
    # if i.isupper():
    #     other_features.append("new_feature_caps")
    # if any(j.isdigit() for j in i):
    #     other_features.append("new_feature_numbers")
    # if any(j for j in i if j == "!"):
    #     other_features.append("new_feature_exclamation")
    # if re.search("</font>", i) is not None:
    #     other_features.append("new_feature_tag")
    return one_gram + two_gram + other_features


def log_probs(email_paths, smoothing):
    dd = defaultdict(int)
    for i in email_paths:
        tokens = load_tokens(i)
        for j in tokens:
            dd[j] += 1
    w_ = sum([i for i in dd.values()])
    V = abs(len(dd.keys()))
    dd = {w: math.log((float(dd[w]) + smoothing) / (w_ + smoothing * (V + 1)))
          for w in dd}
    dd["<UNK>"] = math.log((smoothing) / (w_ + smoothing * (V + 1)))
    return dd


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir):
        spams = ["{}/{}".format(spam_dir, i) for i in os.listdir(spam_dir)]
        hams = ["{}/{}".format(ham_dir, i) for i in os.listdir(ham_dir)]
        smoothing = 1e-10
        self.spam_dir = log_probs(spams, smoothing)
        self.ham_dir = log_probs(hams, smoothing)
        self.alpha = smoothing
        self.p_spam = float(len(spams)) / (len(spams) + len(hams))
        self.p_ham = float(len(hams)) / (len(spams) + len(hams))

    def is_spam(self, email_path):
        doc_1spam = []
        doc_0spam = []
        for i in load_tokens(email_path):
            if i not in self.spam_dir:
                doc_1spam.append(self.spam_dir["<UNK>"])
            else:
                doc_1spam.append(self.spam_dir[i])
            if i not in self.ham_dir:
                doc_0spam.append(self.ham_dir["<UNK>"])
            else:
                doc_0spam.append(self.ham_dir[i])
        pr_1spam_w = math.log(self.p_spam) + sum(doc_1spam)
        pc_0spam_w = math.log(self.p_ham) + sum(doc_0spam)
        print("Prob Spam", pr_1spam_w)
        print("Prob Ham", pc_0spam_w)
        if pr_1spam_w > pc_0spam_w:
            # print(email_path)
            return True
        else:
            # print(email_path)
            return False
