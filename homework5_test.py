
### TEST load_tokens()

load_tokens("data/train/ham/ham1")[200:204]
load_tokens("data/train/ham/ham2")[110:114]
load_tokens("data/train/spam/spam1")[1:5]
load_tokens("data/train/spam/spam2")[:4]

### TEST log_probs()

paths1 = ["data/train/ham/ham%d" % i for i in range(1, 11)]
test1 = log_probs(paths1, 1e-5)
print(test1["the"])
print(-3.6080194731874062)
print(test1["line"])
print(-4.272995709320345)


paths2 = ["data/train/spam/spam%d" % i for i in range(1, 11)]
test2 = log_probs(paths2, 1e-5)
print(test2["Credit"])
print(-5.837004641921745)
print(test2["<UNK>"])
print(-20.34566288044584)

### TEST init(self,...)

import time
time1 = time.time()
sf = SpamFilter("data/train/spam", "data/train/ham", 1e-5)
time.time() - time1

### TEST is_spam()

sf.is_spam("data/train/ham/ham2")

### TEST accuracy

train_spams = ["{}/{}".format("data/train/spam", i) for i in os.listdir("data/train/spam")]
train_hams = ["{}/{}".format("data/train/ham", i) for i in os.listdir("data/train/ham")]
test_spams = ["{}/{}".format("data/dev/spam", i) for i in os.listdir("data/dev/spam")]
test_hams = ["{}/{}".format("data/dev/ham", i) for i in os.listdir("data/dev/ham")]

train_spams_acc = [sf.is_spam(i) for i in train_spams]
train_hams_acc = [sf.is_spam(i) for i in train_hams]
test_spams_acc = [sf.is_spam(i) for i in test_spams]
test_hams_acc = [sf.is_spam(i) for i in test_hams]

print("train/spam", float(sum(train_spams_acc)) / len(train_spams))
print("train/ham", float(train_hams_acc.count(False)) / len(train_hams_acc))
print("dev/spam", float(sum(test_spams_acc)) / len(test_spams))
print("dev/ham", float(test_hams_acc.count(False)) / len(test_hams_acc))

### TEST most_indicative

sf.most_indicative_spam(100)
['<a', '<input', '<html>', '<meta', '</head>']

sf.most_indicative_ham(5)
['Aug', 'ilug@linux.ie', 'install', 'spam.', 'Group:']
