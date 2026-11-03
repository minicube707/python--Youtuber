"""
UUID (Universally Unique Identifier) AND PANDAS DATAFRAME EXAMPLE

UUIDs are 128-bit identifiers designed to provide unique identifiers
across systems, applications, and datasets.

Python provides the following UUID generation methods:

UUID1 - Time-based UUID
-----------------------
Generated using the current timestamp and a node identifier,
typically derived from the machine's MAC address.

Advantages:
- Time-based generation.
- Useful when timestamp-related ordering is desirable.

Disadvantages:
- Can expose information about the machine.
- May reveal approximate generation time.
- Not recommended when MAC address privacy is important.


UUID2 - DCE Security UUID
------------------------
Based on a modified time-based UUID design intended for DCE
(Distributed Computing Environment) Security.

This version replaces part of the timestamp information with
local domain information.

Note:
Python's standard uuid module does not implement UUID2.


UUID3 - Name-based UUID (MD5)
-----------------------------
Generated deterministically using:
- A namespace UUID.
- A name (string).
- The MD5 hashing algorithm.

The same namespace and name always produce the same UUID.

Advantages:
- Deterministic generation.
- Useful when the same logical object must always receive
  the same identifier.

Disadvantages:
- Uses MD5, which is cryptographically broken.
- Not recommended for security-sensitive applications.


UUID4 - Random UUID
------------------
Generated using random values.

UUID4 contains 122 random bits, with the remaining bits
reserved for version and variant information.

Advantages:
- Extremely low probability of collision.
- Does not expose machine-specific information.
- Suitable for distributed systems and independently
  generated database identifiers.

Disadvantages:
- Does not contain meaningful information.
- Does not provide chronological ordering.

This is generally a good choice for generating independent
identifiers across multiple datasets.


UUID5 - Name-based UUID (SHA-1)
-------------------------------
Generated deterministically using:
- A namespace UUID.
- A name (string).
- The SHA-1 hashing algorithm.

The same namespace and name always produce the same UUID.

Advantages:
- Deterministic generation.
- More suitable than UUID3 for new name-based UUID use cases.
- Useful for reproducible identifiers.

Disadvantages:
- Not intended for cryptographic security.
- Does not provide random identifiers.

Recommended when an identifier must be reproducible from
a known namespace and name.


PANDAS DATAFRAME AND UUID USAGE
-------------------------------
This example demonstrates how UUIDs can be used as DataFrame
indexes to avoid collisions when combining datasets.

Integer identifiers (1, 2, 3, 4, 5, etc.) can overlap when
multiple datasets are generated independently.

UUID4 identifiers significantly reduce this risk because
they are independently generated and practically unique.

When concatenating DataFrames, Pandas' verify_integrity=True
option checks whether the resulting index contains duplicates.

Note that UUID uniqueness is probabilistic, not mathematically
guaranteed.
"""

import uuid
import pandas as pd

# UUID1: Time-based
id1 = uuid.uuid1()

# UUID3: Deterministic, using MD5
id3 = uuid.uuid3(uuid.NAMESPACE_DNS, "example.com")

# UUID4: Random
id4 = uuid.uuid4()

# UUID5: Deterministic, using SHA-1
id5 = uuid.uuid5(uuid.NAMESPACE_DNS, "example.com")

print("\nUUID1:", id1)
print("UUID3:", id3)
print("UUID4:", id4)
print("UUID5:", id5)



# ============================================================
# 1. DATASETS WITH INTEGER IDENTIFIERS
# ============================================================

# Create a DataFrame with sequential integer IDs.
data = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6],
    'value': [40, 20, 10, 20, 30, 30],
    'value2': [1, 1, 1, 0, 0, 1],
})

# Use the ID column as the DataFrame index.
data = data.set_index("id")

print("\nDATA")
print(data)


# Load an existing dataset from a CSV file.
existing = pd.read_csv("existing_data.csv")

# Set the ID column as the index.
existing = existing.set_index("id")


print("\nEXISTING DATA")
print(existing)


# Concatenate both datasets.
# By default, Pandas allows duplicate index values.
combined = pd.concat([existing, data])

print("\nCOMBINED DATA (INTEGER IDS)")
print(combined)


# ============================================================
# 2. DATASETS WITH UUID IDENTIFIERS
# ============================================================

# Generate a new UUID for each row.
# Unlike sequential integer IDs, UUIDs can be generated
# independently without requiring a central ID counter.
new_data = pd.DataFrame({
    "id": [uuid.uuid4() for _ in range(6)],
    "value": [40, 20, 10, 20, 30, 30],
    "value2": [1, 1, 1, 0, 0, 1],
})

# Use UUIDs as the DataFrame index.
new_data = new_data.set_index("id")

print("\nNEW DATA (UUID IDS)")
print(new_data)


# Concatenate the existing dataset with the new dataset.
# verify_integrity=True raises a ValueError if duplicate
# index values are found.
combined = pd.concat(
    [existing, new_data],
    verify_integrity=True,
)

print("\nCOMBINED DATA (UUID IDS)")
print(combined)


# ============================================================
# 3. UUID COLLISION EXPERIMENT
# ============================================================

# Generate a reference UUID.
reference_uuid = uuid.uuid4()

print("\nUUID COLLISION EXPERIMENT")
print(f"Reference UUID: {reference_uuid}")

# Generate 9 million UUIDs and check whether any matches
# the reference UUID.
#
# UUID collisions are theoretically possible, but extremely
# unlikely when using UUID version 4.
for i in range(9_000_000):
    generated_uuid = uuid.uuid4()

    if generated_uuid == reference_uuid:
        print(f"Collision detected at iteration {i}!")
        break
else:
    print("No collision detected after 9 million UUID generations.")
