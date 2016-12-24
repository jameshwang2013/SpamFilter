############################################################
# CIS 521: Homework 5
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

############################################################
# Section 1: Spam Filter
############################################################


def load_tokens(email_path):
    f_obj = open(email_path)
    msg = email.message_from_file(f_obj)
    lines = email.iterators.body_line_iterator(msg)
    return filter(None, " ".join([i.strip() for i in list(lines)]).split())


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

    def __init__(self, spam_dir, ham_dir, smoothing):
        spams = ["{}/{}".format(spam_dir, i) for i in os.listdir(spam_dir)]
        hams = ["{}/{}".format(ham_dir, i) for i in os.listdir(ham_dir)]
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
        if pr_1spam_w > pc_0spam_w:
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        V = set(self.spam_dir.keys()) & set(self.ham_dir.keys())
        spam_iv = {i: math.log(math.exp(self.spam_dir[i]) /
                               (math.exp(self.spam_dir[i]) +
                                math.exp(self.ham_dir[i]))) for i in V}
        ord_spam_iv = sorted([(i, spam_iv[i]) for i in spam_iv],
                             key=lambda x: x[1],
                             reverse=True)
        return [i[0] for i in ord_spam_iv[:n]]

    def most_indicative_ham(self, n):
        V = set(self.spam_dir.keys()) & set(self.ham_dir.keys())
        ham_iv = {i: math.log(math.exp(self.ham_dir[i]) /
                              (math.exp(self.spam_dir[i]) +
                               math.exp(self.ham_dir[i]))) for i in V}
        ord_ham_iv = sorted([(i, ham_iv[i]) for i in ham_iv],
                            key=lambda x: x[1],
                            reverse=True)
        return [i[0] for i in ord_ham_iv[:n]]

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
6 hours
"""

feedback_question_2 = """
Took me awhile to remember this key probability property:
P(w) = P(w | spam) + P(w | ham); given that ham = not spam

I also think there could've been more pre-processing steps to remove
punctuation.
"""

feedback_question_3 = """
Overall, assignment was pretty fun!
"""
