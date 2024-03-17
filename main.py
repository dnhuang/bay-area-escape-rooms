from scraper import EscapeRoom

def main():
    test = EscapeRoom('ryptic-room-escape-san-mateo-3')
    print(len(test.all_reviews))
    print(len(test.sentiment_scores))

main()
