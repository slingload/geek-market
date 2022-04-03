"""initial commit, place holder for rest of repository"""

from sys import argv
from libbgg.apiv1 import BGG


def main(username: str) -> None:
    """Look up wanted games for a user and print condition of those games"""
    # connect to BoardGameGeek through its API
    conn = BGG()

    # collect the games the user wants
    wanted_games = (
        conn.get_collection(username, want=1).get('items').get('item')
    )
    game_ids = [game.get('objectid') for game in wanted_games]

    # Look up each of those games
    data = (
        conn.get_game(game_ids=game_ids, marketplace=1)
        .get('boardgames')
        .get('boardgame')
    )
    # If listed for sale on the BGG Marketplace, print cost and condition
    for game in data:
        listings = game.get('marketplacelistings').get('listing')

        if isinstance(game.get('name'), list):
            for gm in game.get('name'):
                if 'primary' in gm.keys():
                    print('\n', gm.get('TEXT'))

        for listing in listings:
            if isinstance(listing, dict):
                price = ' '.join(
                    [
                        listing.get('price').get('TEXT'),
                        listing.get('price').get('currency'),
                    ]
                )
                con = listing.get('condition').get('TEXT')
                print(f'\t {con}: {price}')


if __name__ == '__main__':
    main(argv[1])
