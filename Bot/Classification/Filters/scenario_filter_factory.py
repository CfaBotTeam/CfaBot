from Bot.Classification.Filters import FilterFactoryBase


class ScenarioFilterFactory(FilterFactoryBase):
    def get_filters(self, df):
        filters = super().get_filters(df)
        filters &= df['question'].str.contains(', CFA,')
        return filters
