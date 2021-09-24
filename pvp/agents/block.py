from mesa import Agent


class Block(Agent):
    """
    Using Block as an agent instead. Allows for flexibility and can be easily tied in to further strategies without changing much
    """

    def __init__(
        self,
        unique_id,
        model,
        pos,
    ):
        super().__init__(unique_id, model)
        self.pos = pos
        self.breed = "Block"
        self.jail_sentence = None
        self.condition = "Quiescent"

    def step(self):
        """
        This would disable it moving and be fixed
        """
        pass
