world_cup = {
    'stages' : {
        'F': 1,
        'S': 2,
        'Q': 3,
        'O': 4,
    },
    'group_matches': {
        'fifa': [
            (1, 2),
            (3, 4),
            (4, 2),
            (1, 3),
            (2, 3),
            (4, 1),
        ],
    },
    'groups': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    'rounds': [
        # (round, competing, visiting)
        ( 'O1', ('A', 1), ('B', 2) ),
        ( 'O2', ('C', 1), ('D', 2) ),
        ( 'O3', ('E', 1), ('F', 2) ),
        ( 'O4', ('G', 1), ('H', 2) ),
        ( 'O5', ('B', 1), ('A', 2) ),
        ( 'O6', ('D', 1), ('C', 2) ),
        ( 'O7', ('F', 1), ('E', 2) ),
        ( 'O8', ('H', 1), ('G', 2) ),

        ( 'Q1', 'O1', 'O2'),
        ( 'Q2', 'O3', 'O4'),
        ( 'Q3', 'O5', 'O6'),
        ( 'Q4', 'O7', 'O8'),

        ( 'S1', 'Q1', 'Q2'),
        ( 'S2', 'Q3', 'Q4'),

        ( 'F1', 'S1', 'S2'), # Final
        ( 'F2', ('S1', 2), ('S2', 2)), # 3rd and 4th
    ]
}
