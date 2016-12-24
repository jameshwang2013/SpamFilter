### TEST accuracy
'''
Features tried:
#if i.isupper():
#    other_features.append("new_feature_caps")
#if any(j.isdigit() for j in i):
#    other_features.append("new_feature_numbers")
#if any(j for j in i if j == "!"):
#    other_features.append("new_feature_exclamation")
#if re.search("</font>", i) is not None:
#    other_features.append("new_feature_tag")
'''
import time

time1 = time.time()

sf = SpamFilter("data/train/spam", "data/train/ham")

time2 = time.time()

train_spams = ["{}/{}".format("data/train/spam", i) for i in os.listdir("data/train/spam")]
train_hams = ["{}/{}".format("data/train/ham", i) for i in os.listdir("data/train/ham")]
test_spams = ["{}/{}".format("data/dev/spam", i) for i in os.listdir("data/dev/spam")]
test_hams = ["{}/{}".format("data/dev/ham", i) for i in os.listdir("data/dev/ham")]

train_spams_acc = [sf.is_spam(i) for i in train_spams]
train_hams_acc = [sf.is_spam(i) for i in train_hams]

time3 = time.time()

test_spams_acc = [sf.is_spam(i) for i in test_spams]
test_hams_acc = [sf.is_spam(i) for i in test_hams]

time4 = time.time()

print("train/spam", float(sum(train_spams_acc)) / len(train_spams))
print("train/ham", float(train_hams_acc.count(False)) / len(train_hams_acc))
print("dev/spam", float(sum(test_spams_acc)) / len(test_spams))
print("dev/ham", float(test_hams_acc.count(False)) / len(test_hams_acc))

print(time2 - time1)
print(time4 - time3)


### ANALYSIS of errors

sf = SpamFilter("data/train/spam", "data/train/ham")

test_spams_acc = [sf.is_spam(i) for i in test_spams]
test_hams_acc = [sf.is_spam(i) for i in test_hams]

# misclassified spam
load_tokens("data/dev/spam/dev222")
load_tokens("data/dev/spam/dev283")
sf.is_spam("data/dev/spam/dev222")
sf.is_spam("data/dev/spam/dev283")

# misclassified ham
load_tokens("data/dev/ham/dev118")
sf.is_spam("data/dev/ham/dev118")


# common spam
spam_d = sf.spam_dir
sorted_spam_d = sorted(spam_d.items(), key=lambda x: x[1])
sorted_spam_d[:10]

ham_d = sf.ham_dir
sorted_ham_d = sorted(ham_d.items(), key=lambda x: x[1])
sorted_ham_d[:10]

