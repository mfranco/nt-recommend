from app.predictors.collaborative import (
    CollaborativePredictor, ResnickPredictor)


class BaseRecommender(object):
    """
    Take the union all the items that have been rated by the active user’s
    neighbours.

    Exclude items that have been rated for the active user.

    Rank remaining set by one of the folowing parameters:

    Frequent Item: Number of ratings by item
    Liked Item: Mean of the ratings across neighbours
    Predicted Rating: Make a prediction for each of the candidate items

    The top-N items with the highest scores are returned as
    recommendations
    """

    def __init__(
            self, db, predictor='collaborative',
            neighbourhood_size=10, **kwargs):

        predictor_ditc = {
            'collaborative': CollaborativePredictor,
            'resnik': ResnickPredictor
        }

        if 'init_predictor_params' in kwargs:
            init_predictor_params = kwargs['init_predictor_params']
        else:
            init_predictor_params = {}

        self.db = db
        init_predictor_params['db'] = self.db

        self._predictor = predictor_ditc[predictor](**init_predictor_params)

    def rank_recommendations(self):
        """
        Ranks recommendation based in some criteria
        """
        raise NotImplementedError

    def get_user_recommendations(self, user_id):
        """
        Returns a list of recommendations for a given user.
        """
