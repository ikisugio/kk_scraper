import url_lists_data
from collections import Counter

test_data = url_lists_data.test_data

# Create a counter of jigyosyo_cd values.
jigyosyo_cd_counter = Counter(item['jigyosyo_cd'] for item in test_data)

# Find values that occur more than once.
duplicates = [item for item, count in jigyosyo_cd_counter.items() if count > 1]

if duplicates:
    print(f"Some jigyosyo_cd values are duplicated. Duplicates are: {duplicates}")
else:
    print("There are no duplicated jigyosyo_cd values.")