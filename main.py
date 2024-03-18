from scraper import EscapeRoom

ESCAPE_ROOM_URLS = [
    'trivium-games-emeryville',
    'omescape-san-jose-san-jose',
    'paniq-escape-room-san-jose-san-jose',
    'breakout-studios-san-jose',
    'the-escape-game-santa-clara',
    'edscapade-games-san-jose-2',
    'omescape-sunnyvale-sunnyvale-3',
    'ryptic-room-escape-mountain-view',
    'limitless-escape-games-pleasanton',
    'clockwise-escape-room-pleasanton-pleasanton',
    'heist-escape-room-fremont',
    'off-the-couch-fremont',
    'xcapade-immersive-escape-room-newark',
    'quantum-escapes-danville',
    'zscape-games-san-ramon',
    'red-door-escape-room-san-mateo',
    'ryptic-room-escape-b-street-san-mateo',
    'diablo-escapes-walnut-creek',
    'ryptic-room-escape-san-mateo-3',
    'palace-games-san-francisco',
    'escapology-sf-san-francisco-2',
    'escapesf-san-francisco',
    'the-escape-game-san-francisco-san-francisco-5',
    'reason-san-francisco',
    'pacifica-escape-zone-pacifica'
]

def main():
    test = EscapeRoom('ryptic-room-escape-san-mateo-3')
    print(len(test.all_reviews))
    print(len(test.sentiment_scores))

main()
