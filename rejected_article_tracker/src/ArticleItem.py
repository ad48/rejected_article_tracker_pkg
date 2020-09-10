import pandas as pd
from .AuthorNames import AuthorNames
from .ManuscriptIdRaw import ManuscriptIdRaw


class ArticleItem:

    def __init__(self, items):
        """
        :param items: dict
            manuscript_id: str
            journal_name: str
            manuscript_title: str
            submission_date: str    Most date formats will work.
            decision_date: str      Most date formats will work.
            authors: str            Semi-colon-separated list of names in the format:
                                    "{last name}, {first_names}; {last name}, {first_names}"
                                    e.g.  "De Vries, Ieke; Goggin, Kelly"
            final_decision: str
        """
        submission_date = self.__required(items, 'submission_date')

        if not isinstance(submission_date, pd.Timestamp):
            raise ValueError('"submission_date" needs to be a valid date')

        self.items = {
            'manuscript_id': self.__required(items, 'manuscript_id'),
            'raw_manuscript_id': ManuscriptIdRaw(items['manuscript_id']).id(),
            'journal_name': self.__required(items, 'journal_name'),
            'manuscript_title': self.__required(items, 'manuscript_title'),
            'submission_date': submission_date,
            'decision_date': items['decision_date'],
            'authors': AuthorNames(items['authors']).names(),
            'text_sub_date': items['submission_date'].strftime("%Y-%m-%d"),
            'final_decision': items['final_decision']
        }

    def to_dict(self):
        return self.items

    @staticmethod
    def __required(items, name):
        if not items[name]:
            raise ValueError('field "' + name + '" required')
        return items[name]

