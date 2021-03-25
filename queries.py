"""
All queries go here.
Query API usage:

some_query = Query(
    keyword_whitelist=[...],
    store_whitelist=[...],
    keyword_blacklist=[...],
    store_blacklist=[...],
    max_distance=<number>
)

Add any queries that should be used to filter the results to the
`ACTIVE_QUERIES` array at the bottom of the file. For a notification
to be sent, the item must match at least one of the queries.
"""

from lib import Query

meat = Query(
    keyword_whitelist=["Kød"],
    store_blacklist=["Lyngby", "Tingbjerg", "LIDL - Dyssegaard"]
)

favourite = Query(
    store_whitelist=[
    "LIDL - Bagsværd",
    "LIDL - Kbh. Brønshøj",
    "Netto - Sydfrontvej 2",
    "Det Grønne Køkken",
    "Wiloo",
    "Frederiksdal - Virum",
    ]
)

nearby = Query(
    store_whitelist=["Netto", "LIDL", ],
    keyword_blacklist=["Blandede"],
    max_distance=3
)

ACTIVE_QUERIES = [meat, favourite]
