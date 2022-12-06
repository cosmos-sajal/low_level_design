class ReactionTableSequenceIdGenerator:
    def __init__(self):
        self.id_seq_no = 0

    def get_id(self):
        self.id_seq_no += 1

        return self.id_seq_no


class Reaction:
    # This is one of the row in the reactions table
    def __init__(self, user_id, match_id, emoticon_type, timestamp, **kwargs):
        id_seq_generator = kwargs.get('id_seq_generator')
        self.id = id_seq_generator.get_id()
        self.user_id = user_id
        self.match_id = match_id
        self.emoticon_type = emoticon_type
        self.timestamp = timestamp

    def print_row(self):
        string_to_be_printed = "id: " + str(self.id) + " | " + \
            "user_id: " + str(self.user_id) + \
            " | " + "match_id: " + str(self.match_id) + " | " + \
            "emoticon_type: " + self.emoticon_type + " | " + \
            "timestamp: " + str(self.timestamp)
        print(string_to_be_printed)


class ReactionsTable:
    def __init__(self):
        self.reaction_list = []
        self.id_seq_generator = \
            ReactionTableSequenceIdGenerator()

    def insert_into_table(self, *args, **kwargs):
        reaction = Reaction(
            *args,
            **kwargs,
            id_seq_generator=self.id_seq_generator
        )
        self.reaction_list.append(reaction)

    def print_table(self):
        for reaction in self.reaction_list:
            reaction.print_row()
