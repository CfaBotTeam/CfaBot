from Bot.Classification import ProblemCategory


class FilterFactoryBase:
    def get_filters(self, df):
        # In order for a filter not to over take the filtering of another category
        # we must add this base filter for every filter
        return df['predicted_category'] == ProblemCategory.UNLABELED
