
class ScenarioFilterFactory:
    def get_filters(self, df):
        filters = df['question'].str.contains(', CFA,')
        return filters
