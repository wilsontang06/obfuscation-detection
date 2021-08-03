# 
# Authors: Security Intelligence Team within the Security Coordination Center
# 
# Copyright 2021 Adobe. All rights reserved.
# This file is licensed to you under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. You may obtain a copy
# of the License at http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR REPRESENTATIONS 
# OF ANY KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#

import pandas as pd
import torch

DATA_DIR = '../data/processed_csv/'

all_rows = []
all_rows += pd.read_csv(DATA_DIR + 'ps-data.csv').values.tolist()
all_rows += pd.read_csv(DATA_DIR + 'dos-data.csv').values.tolist()
all_rows += pd.read_csv(DATA_DIR + 'hubble-data.csv').values.tolist()
all_rows += pd.read_csv(DATA_DIR + 'cb-data.csv').values.tolist()
all_rows += pd.read_csv(DATA_DIR + 'obf-data.csv').values.tolist()
print(len(all_rows))
print(all_rows[0])

# split all data into train, val, test
train = []
val = []
test = []
train_idx, val_idx, test_idx = torch.utils.data.random_split(range(len(all_rows)), 
                                                            # hard-calculated 80-15-5 split
                                                            # [64000, 12000, 4000], # 80k samples
                                                            # [32000, 6000, 2000], # 40k samples
                                                            # [40000, 7500, 2500], # 50k samples
                                                            [80000, 15000, 5000], #100k samples]
                                                            generator=torch.Generator().manual_seed(42))
for i in train_idx:
    train.append(all_rows[i])
for i in val_idx:
    val.append(all_rows[i])
for i in test_idx:
    test.append(all_rows[i])

train_df = pd.DataFrame(train, columns=['label', 'command'])
val_df = pd.DataFrame(val, columns=['label', 'command'])
test_df = pd.DataFrame(test, columns=['label', 'command'])

train_df.to_csv(DATA_DIR + 'train-data.csv', index=False)
val_df.to_csv(DATA_DIR + 'val-data.csv', index=False)
test_df.to_csv(DATA_DIR + 'test-data.csv', index=False)

# sanity checks
print(len(train_df), len(val_df), len(test_df))
