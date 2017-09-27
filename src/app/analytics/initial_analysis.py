from app.models import DB
from prettytable import PrettyTable


def compute():
    """
    Computes different statistics relevant for Task 1
    """
    db = DB()

    print('\nGeneral Statistics:')
    t = PrettyTable([
        'Total Users', 'Total Movies', 'Total Tags', 'Matrix Density',

    ])
    t.align['Total Users'] = 'l'
    t.align['Total Movies'] = 'l'
    t.align['Matrix Density'] = 'l'
    t.padding_width = 1
    t.add_row([
        len(db.users.keys()), len(db.movies.keys()),
        len(db.tags), '{0:.3g}'.format(db.density)
    ])

    print(t)

    print('\nStatistics by User and Ratings:')
    t = PrettyTable([
        'Max Number of Ratings for User', 'Min Number of Ratings for User',
        'Median Ratings for User', 'Mean Ratings for User',
        'Standard Deviation Ratings for User'


    ])
    t.add_row([
        db.stats['users']['max'], db.stats['users']['min'],
        db.stats['users']['median'],
        '{0:.3g}'.format(db.stats['users']['mean']),
        '{0:.3g}'.format(db.stats['users']['sd'])
    ])
    print(t)

    print('\nStatistics by Movie and Ratings:')

    t = PrettyTable([
        'Max Number of Ratings for Movie', 'Min Number of Ratings for Movie',
        'Median Ratings for Movie', 'Mean Ratings for Movie',
        'Standard Deviation Ratings for Movie'


    ])

    t.add_row([
        db.stats['movies']['max'], db.stats['movies']['min'],
        db.stats['movies']['median'],
        '{0:.3g}'.format(db.stats['movies']['mean']),
        '{0:.3g}'.format(db.stats['movies']['sd'])
    ])

    print(t)

    print('\nTotal number of ratings for each of the 5 ratings')

    t = PrettyTable(sorted(db.stats['ratings'].keys()))
    row = [
        db.stats['ratings'][k] for k in sorted(db.stats['ratings'].keys())
    ]
    t.add_row(row)
    print(t)

    print('\nStatistics by Tags and User')
    t = PrettyTable([
        'Max Number of Tags by User', 'Min Number of Tags by User',
        'Median Number of Tags by User', 'Mean Number of Tags by User',
        'Standard Deviation Tags by User'
    ])
    t.add_row([
        db.stats['tags']['by_user']['max'],
        db.stats['tags']['by_user']['min'],
        db.stats['tags']['by_user']['median'],
        '{0:.3g}'.format(db.stats['tags']['by_user']['mean']),
        '{0:.3g}'.format(db.stats['tags']['by_user']['sd'])
    ])
    print(t)

    print('\nStatistics by Tags and Movie')
    t = PrettyTable([
        'Max Number of Tags by Movie', 'Min Number of Tags by Movie',
        'Median Number of Tags by Movie', 'Mean Number of Tags by Movie',
        'Standard Deviation Tags by Movie'
    ])
    t.add_row([
        db.stats['tags']['by_movie']['max'],
        db.stats['tags']['by_movie']['min'],
        db.stats['tags']['by_movie']['median'],
        '{0:.3g}'.format(db.stats['tags']['by_movie']['mean']),
        '{0:.3g}'.format(db.stats['tags']['by_movie']['sd'])
    ])
    print(t)
