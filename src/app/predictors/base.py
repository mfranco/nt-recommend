class BasePredictor(object):
    def __init__(self, db):
        """
        Functionally that is common to all predictors
        """
        self.db = db

    def get_user_similarity(self, user_id_1, user_id_2):
        """
        Computes similarity between 2 users
        """
        raise NotImplementedError
