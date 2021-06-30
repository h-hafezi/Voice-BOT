from Controller import Server

# telegram = 'https://api.telegram.org/bot{}/'.format('1874388872:AAGzHFqo1dxCSBvUko-BppLWVgSewFT57Po')
# bale = 'https://tapi.bale.ai/bot{}/'.format('184065011:e7534e857e575748594532f6712a124e5a2b957a')
URL = 'https://api.telegram.org/bot{}/'.format('1874388872:AAGzHFqo1dxCSBvUko-BppLWVgSewFT57Po')

if __name__ == '__main__':
    server = Server.server(token='1874388872:AAGzHFqo1dxCSBvUko-BppLWVgSewFT57Po')
    server.start()

